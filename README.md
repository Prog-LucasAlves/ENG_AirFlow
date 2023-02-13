# Projeto AirFlow

Coletando dados de uma API e fazendo a ingestão dos dados em um Banco de Dados.

![ ](https://github.com/Prog-LucasAlves/ENG-AirFlow/blob/main/image/Captura%20de%20tela%202023-02-13%20101542.png)

ENG - Airflow

-Conexões usuários:

1. airflow(postgres-airflow_dl) -> Postegres(BD -> moedas_dl): user: etl_airflow_dl | password: P@ssword21

2. airflow(postgres-airflow_dw) -> Postegres(BD -> moedas_dw): user: etl_airflow_dw | password: P@ssword21
3. power_bi() -> Postegres(BD - moedas_dw): user: etl_powerbi_dw | P@ssword21

![GitHub](https://img.shields.io/github/license/Prog-LucasAlves/ENG-Airflow)

## ![P](https://cdn-icons-png.flaticon.com/24/8422/8422251.png) Pacotes Python utilizados

[![Pandas](https://badge.fury.io/py/pandas.svg)](https://badge.fury.io/py/pandas)
[![PyPI version](https://badge.fury.io/py/Airflow.svg)](https://badge.fury.io/py/Airflow)
