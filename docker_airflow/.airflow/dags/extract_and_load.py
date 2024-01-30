from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.common.sql.operators.sql import SQLColumnCheckOperator, SQLTableCheckOperator
from airflow.models.baseoperator import chain
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.task_group import TaskGroup
from airflow.models import Variable

from scripts.request_get import captura_dados
from scripts.transformeted import transforma

from datetime import datetime, timedelta

PATH_DATA_DL = Variable.get('PATH_DATA_DL')
PATH_DATA_DW = Variable.get('PATH_DATA_DW')
POSTGRES_TABLE = Variable.get('POSTGRES_TABLE')
POSTGRES_CONN_DL = Variable.get('POSTGRES_CONN_DL')
POSTGRES_CONN_DW = Variable.get('POSTGRES_CONN_DW')

with DAG(
    'EXTRACT_AND_LOAD',
    default_args={
        "depends_on_past": False,
        "up_for_retry": 2,
    },
    description='DAG ETL',
    start_date=datetime(2023, 1, 29),
    schedule_interval=timedelta(minutes=5),
    catchup=False,
    template_searchpath='/opt/airflow/sql',
    tags=["ETL"]
) as dag:

    coleta_dados = PythonOperator(
        task_id='coleta_dados',
        python_callable=captura_dados
    )

    transforma_dados = PythonOperator(
        task_id='transforma_dados',
        python_callable=transforma
    )

    criar_tabela_dl = PostgresOperator(
        task_id='cria_tabela_dl',
        postgres_conn_id=POSTGRES_CONN_DL,
        sql='cria_tabela_dl.sql',
        params={'table': POSTGRES_TABLE}
    )

    inseri_dados_tabela_dl = PostgresOperator(
        task_id='insere_dados_dl',
        postgres_conn_id=POSTGRES_CONN_DL,
        sql='inseri_dados_tabela_dl.sql',
        params={'table': POSTGRES_TABLE,
                'path': PATH_DATA_DL}
    )
    with TaskGroup(group_id='check_dl', default_args={"conn_id": POSTGRES_CONN_DL}) as quality_check_dl:

        table_checks_dl = SQLTableCheckOperator(
            task_id = 'table_checks_dl',
            table =  POSTGRES_TABLE,
            checks = {
                "row_count_check": {"check_statement": "COUNT(*) > 0"},
                "code_distinct": {"check_statement": "COUNT(DISTINCT(code)) = 14",
                                  "partition_clause": "code IS NOT NULL"},
                "codein_distinct": {"check_statement": "COUNT(DISTINCT(codein)) = 2",
                                    "partition_clause": "codein IS NOT NULL"},
                "name_distinct": {"check_statement": "COUNT(DISTINCT(name)) = 15",
                                  "partition_clause": "name IS NOT NULL"},
                "code_diff_codein": {"check_statement": "code != codein"},
                "high_greater": {"check_statement": "high > 0",
                                 "partition_clause": "high IS NOT NULL"},
                "low_greater": {"check_statement": "low > 0",
                                "partition_clause": "low IS NOT NULL"},
                "high_diff_low": {"check_statement": "high >= low"},
                "ask_greater": {"check_statement": "ask > 0",
                                "partition_clause": "ask IS NOT NULL"},
                "bid_greater": {"check_statement": "bid > 0",
                                "partition_clause": "bid IS NOT NULL"},
                "ask_diff_bid": {"check_statement": "ask >= bid"}         
                },
        )

        columns_checks_dl = SQLColumnCheckOperator(
            task_id = 'columns_checks_dl',
            table = POSTGRES_TABLE,
            column_mapping = {
                "ID": {"unique_check": {"equal_to": 0}, "null_check": {"equal_to": 0}},
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
        params = {'table': POSTGRES_TABLE,
                'path': PATH_DATA_DW}
    )
    with TaskGroup(group_id='check_dw', default_args={"conn_id": POSTGRES_CONN_DW}) as quality_check_dw:
        
        table_checks_dw = SQLTableCheckOperator(
            task_id = 'table_check_dw',
            table = POSTGRES_TABLE,
            checks = {
                "row_count_check": {"check_statement": "COUNT(*) > 0"},
                "code_distinct": {"check_statement": "COUNT(DISTINCT(code)) = 14",
                                  "partition_clause": "code IS NOT NULL"},
                "codein_distinct": {"check_statement": "COUNT(DISTINCT(codein)) = 2",
                                    "partition_clause": "codein IS NOT NULL"},
                "name_distinct": {"check_statement": "COUNT(DISTINCT(name)) = 15",
                                  "partition_clause": "name IS NOT NULL"},
                "code_diff_codein": {"check_statement": "code != codein"},
            },
        )

        columns_checks_dw = SQLColumnCheckOperator(
            task_id = 'columns_checks_dw',
            table = POSTGRES_TABLE,
            column_mapping = {
                "ID": {"unique_check": {"equal_to": 0}, "null_check": {"equal_to": 0}},
            }
        )

    begin = EmptyOperator(task_id='begin')
    end = EmptyOperator(task_id='end')

    chain(
        begin,
        coleta_dados,
        transforma_dados,
        criar_tabela_dl,
        inseri_dados_tabela_dl,
        quality_check_dl,
        deleta_dados_duplicados_tabela_dl,
        query_backup_dl,
        select_ultimos_dados_inseridos_dl,
        criar_tabela_dw,
        deleta_dados_tabela_dw,
        inseri_dados_tabela_dw,
        quality_check_dw,
        end
    )

# TODO: Estrurar o desenvolvimento
# TODO: Bachup ✅
# TODO: Segurança -> Criar usuários ✅
# TODO: Criar script sql para pegar o ultimo dado de cada par de moeda e inserir no DW ✅
# TODO: Criar insert.sql com os dados a serem inseridos ✅
# TODO: Enviroment nomes de tabelas, conexões ✅
# TODO: Transformando dados coletados ✅
# TODO: Data Quality (Tabela e Colunas) ask não pode ser menor que bid ✅
# TODO: View Materializada por code
# TODO: Média | Mediana ult. 5 dias
# TODO: Criar script sql separando em arquivos csv por par de moeda


