# ![Projeto AirFlow](https://cdn-icons-png.flaticon.com/24/4907/4907848.png) Projeto AirFlow

Coletando dados de uma API(Pares de Moedas) e fazendo a ingestão dos dados em um Banco de Dados.

![ ](https://github.com/Prog-LucasAlves/ENG-AirFlow/blob/main/image/Captura%20de%20tela%202023-02-13%20101542.png)

## ![Informações do Projeto](https://cdn-icons-png.flaticon.com/24/8365/8365039.png) Informações do Projeto

1. API Utilizada: *[API](https://docs.awesomeapi.com.br/api-de-moedas)*
2. Banco de Dados*: **PostgreSQL 13** (Via Docker - postgres:13)
3. Airflow: **Airflow 2.8.3** (Via Docker - apache/airflow:2.8.3)

- **Foi Criado dois banco de dados*
- *1. moedas_dl(DataLake) -> Schema(moedas)*
- *2. moedas_dw(DataWarehouse) -> Schema(moedas)*

- Conexões aos banco de dados:

1. airflow(postgres-airflow_dl) -> Postegres(BD -> moedas_dl): user: etl_airflow_dl | password: *****
2. airflow(postgres-airflow_dw) -> Postegres(BD -> moedas_dw): user: etl_airflow_dw | password: *****

## ![Planejamento](https://cdn-icons-png.flaticon.com/24/5341/5341024.png) Planejamento

- [x] Coletar os dados da API (Em Produção)
- [ ] Data Quality (Em Desenvolvimento)
- [x] Salvando os dados no Datalake (Em Produção)
- [x] Filtrando os dados salvos no Datalake (Em Produção)
- [x] Salvando os dados no Datawarehouse (Em Produção)
- [ ] Conectando o PowerBI no Datawarehouse - Dashboard (Em Desenvolvimento)
- [ ] Criando aplicação em flask com os dados (Em Desenvolvimento)

## ![CI](https://cdn-icons-png.flaticon.com/24/6577/6577286.png) Github

![GitHub](https://img.shields.io/github/license/Prog-LucasAlves/ENG-Airflow)
![GitHub](https://img.shields.io/github/languages/top/Prog-LucasAlves/ENG-AirFlow)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/Prog-LucasAlves/ENG-AirFlow)

![progress](https://progress-bar.dev/60/?title=completed "progresso")

## ![IESS](https://cdn-icons-png.flaticon.com/24/5109/5109476.png) Itens Essenciais

## Pré-requisitos

- **VSCode**: É o editor de código que irei utilizar [Instruções aqui](https://code.visualstudio.com/download).
- **Pyenv**: É usado para gerenciar versões do Python. [Instruções de instalação do Pyenv aqui](https://github.com/pyenv/pyenv#installation). Vamos usar nesse projeto o Python 3.11.3. Para usuários Windows, é recomendado assistirem esse tutorial [Youtube](https://www.youtube.com/watch?v=TkcqjLu1dgA).
- **Poetry**: Este projeto utiliza Poetry para gerenciamento de dependências. [Instruções de instalação do Poetry aqui](https://python-poetry.org/docs/#installing-with-pipx).
- **Docker**: O Docker é uma plataforma open source que facilita a criação e administração de ambientes isolados. Iremos utilizar o Docker para implantação do AirFlow e do PostgreSQL. [Intruções sobre o Docker Desktop aqui](https://www.docker.com/products/docker-desktop/).

## ![CONFIG](https://cdn-icons-png.flaticon.com/24/4149/4149678.png) Instalação e Configuração

1. Criando o diretório do projeto

```bash
mkdir ENG-AirFlow
cd ENG-AirFlow
```

2. Clone o repositório:

```bash
git clone https://github.com/Prog-LucasAlves/ENG-AirFlow.git
```

3. Configurar a versão do Python com ``pyenv``:

```bash
pyenv install 3.11.3
pyenv local 3.11.3
```

4. Configurar o poetry:

```bash
poetry init
poetry shell
```

5. Instalando as dependências do projeto:

```bash
poetry install
```

6. Executando Docker

```bash
docker-compose up -d
```

## ![CONT](https://cdn-icons-png.flaticon.com/24/6008/6008922.png) Contato

- **ISSUES** [AQUI](https://github.com/Prog-LucasAlves/ENG-AirFlow/issues/new/choose)
- **LinkedIn** [AQUI](https://www.linkedin.com/in/lucasalves-ast/)
