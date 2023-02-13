# ![Projeto AirFlow](https://cdn-icons-png.flaticon.com/24/4907/4907848.png) Projeto AirFlow

Coletando dados de uma API e fazendo a ingestão dos dados em um Banco de Dados.

![ ](https://github.com/Prog-LucasAlves/ENG-AirFlow/blob/main/image/Captura%20de%20tela%202023-02-13%20101542.png)

## ![Informações do Projeto](https://cdn-icons-png.flaticon.com/24/8365/8365039.png) Informações do Projeto

1. API Utilizada: *[API](https://docs.awesomeapi.com.br/api-de-moedas)*
2. Banco de Dados*: **Postgres 13** (Via Docker - postgres:13)
3. Airflow: **Airflow 2.5.1** (Via Docker - apache/airflow:2.5.1)

- **Foi Criado dois banco de dados*
- *1. moedas_dl(DataLake) -> Schema(pares_moedas)*
- *2. moedas_dw(DataWarehouse) -> Schema(pares_moedas)*

-Conexões usuários:

1. airflow(postgres-airflow_dl) -> Postegres(BD -> moedas_dl): user: etl_airflow_dl | password: *****
2. airflow(postgres-airflow_dw) -> Postegres(BD -> moedas_dw): user: etl_airflow_dw | password: *****

## ![Planejamento](https://cdn-icons-png.flaticon.com/24/5341/5341024.png) Planejamento

- [x] Coletar os dados da API
    - [x] Data Quality
- [x] Salvando os dados no Datalake
- [x] Filtrando os dados salvos no Datalake
- [x] Salvando os dados no Datawarehouse

## ![CI](https://cdn-icons-png.flaticon.com/24/6577/6577286.png) Github

![GitHub](https://img.shields.io/github/license/Prog-LucasAlves/ENG-Airflow)
![GitHub](https://img.shields.io/github/languages/top/Prog-LucasAlves/ENG-AirFlow)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/Prog-LucasAlves/ENG-AirFlow)

## ![P](https://cdn-icons-png.flaticon.com/24/8422/8422251.png) Pacotes Python utilizados

[![Pandas](https://badge.fury.io/py/pandas.svg)](https://badge.fury.io/py/pandas)
[![Airflow](https://badge.fury.io/py/apache-airflow.svg)](https://badge.fury.io/py/apache-airflow)

ENG - Airflow
