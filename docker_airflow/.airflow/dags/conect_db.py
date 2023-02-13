from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.common.sql.operators.sql import SQLColumnCheckOperator, SQLTableCheckOperator
from airflow.models.baseoperator import chain
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.task_group import TaskGroup
from airflow.models import Variable

from scripts.request_get import captura_dados

from datetime import datetime, timedelta

POSTGRES_TABLE = Variable.get('POSTGRES_TABLE')
POSTGRES_CONN_DL = Variable.get('POSTGRES_CONN_DL')
POSTGRES_CONN_DW = Variable.get('POSTGRES_CONN_DW')

with DAG(
    'dag_executa_etl_sql',
    default_args={
        "depends_on_past": False,
        "up_for_retry": 2,
    },
    description = 'DAG ETL',
    start_date = datetime(2023, 1, 29),
    schedule_interval = timedelta(minutes=5),
    catchup = False,
    template_searchpath = '/opt/airflow/sql',
    tags=["ETL"]
    ) as dag:

    coleta_dados = PythonOperator(
        task_id = 'coleta_dados',
        python_callable = captura_dados
    )

    criar_tabela_dl = PostgresOperator(
        task_id = 'cria_tabela_dl',
        postgres_conn_id = POSTGRES_CONN_DL,
        sql = 'cria_tabela_dl.sql',
        params = {'table': POSTGRES_TABLE}
    )

    inseri_dados_tabela_dl = PostgresOperator(
        task_id = 'insere_dados_dl',
        postgres_conn_id = POSTGRES_CONN_DL,
        sql = 'inseri_dados_tabela_dl.sql',
        params = {'table': POSTGRES_TABLE}
    )
    with TaskGroup(group_id='check', default_args={"conn_id": POSTGRES_CONN_DL}) as quality_check:

        table_checks_dl = SQLTableCheckOperator(
            task_id = 'table_checks',
            table =  POSTGRES_TABLE,
            checks = {
                "code_diff_codein": {"check_statement": "code != codein"},
                "row_count_check": {"check_statement": "COUNT(*) > 0"},
                "high_diff_low": {"check_statement": "high >= low"},
                "code_": {"check_statement": "COUNT(DISTINCT(code)) = 14"},
                "codein_": {"check_statement": "COUNT(DISTINCT(codein)) = 2"},
                "name_": {"check_statement": "COUNT(DISTINCT(name)) = 15"},
            },
        )

        columns_checks_dl = SQLColumnCheckOperator(
            task_id = 'columns_checks',
            table = POSTGRES_TABLE,
            column_mapping = {
                "ID": {"unique_check": {"equal_to": 0}, "null_check": {"equal_to": 0}},
                "code": {"null_check": {"equal_to": 0}},
                "create_date": {"null_check": {"equal_to": 0}}
                }
        )

    deleta_dados_duplicados_tabela_dl = PostgresOperator(
        task_id = 'deleta_dados_duplicados_tabela_dl',
        postgres_conn_id = POSTGRES_CONN_DL,
        sql = 'deleta_dados_duplicados_dl.sql',
        params = {'table': POSTGRES_TABLE}
    )

    query_backup_dl = PostgresOperator(
        task_id = 'query_backup_dl_to_csv',
        postgres_conn_id = POSTGRES_CONN_DL,
        sql = 'backup_to_csv_dl.sql',
        params = {'table': POSTGRES_TABLE}
    )

    select_ultimos_dados_inseridos_dl = PostgresOperator(
        task_id = 'select_ultimos_dados_inseridos_dl',
        postgres_conn_id = POSTGRES_CONN_DL,
        sql = 'ultimos_dados_inseridos_dl.sql',
        params = {'table': POSTGRES_TABLE}
    )

    criar_tabela_dw = PostgresOperator(
        task_id = 'cria_tabela_dw',
        postgres_conn_id = POSTGRES_CONN_DW,
        sql = 'cria_tabela_dw.sql',
        params = {'table': POSTGRES_TABLE}
    )

    deleta_dados_tabela_dw = PostgresOperator(
        task_id = 'deleta_dados_tabela_dw',
        postgres_conn_id = POSTGRES_CONN_DW,
        sql = 'deleta_dados_tabela_dw.sql',
        params = {'table': POSTGRES_TABLE}
    )

    inseri_dados_tabela_dw = PostgresOperator(
        task_id = 'insere_dados_dw',
        postgres_conn_id = POSTGRES_CONN_DW,
        sql = 'inseri_dados_tabela_dw.sql',
        params = {'table': POSTGRES_TABLE}
    )

    begin = EmptyOperator(task_id='begin')
    end = EmptyOperator(task_id='end')

    chain(
        begin,
        coleta_dados,
        criar_tabela_dl,
        inseri_dados_tabela_dl,
        quality_check,
        deleta_dados_duplicados_tabela_dl,
        query_backup_dl,
        select_ultimos_dados_inseridos_dl,
        criar_tabela_dw,
        deleta_dados_tabela_dw,
        inseri_dados_tabela_dw,
        end
    )

# TODO: Estrurar o desenvolvimento
# TODO: Bachup ✅
# TODO: Segurança -> Criar usuários ✅
# TODO: Criar script sql para pegar o ultimo dado de cada par de moeda e inserir no DW ✅
# TODO: Criar insert.sql com os dados a serem inseridos ✅
# TODO: Enviroment nomes de tabelas, conexões
# TODO: Criar script sql separando em arquivos csv por par de moeda

# D:\Prjts\AirFlow\dags\scripts