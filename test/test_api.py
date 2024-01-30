import requests


# Função para testar API
def test_api():
    header = {'user-agent': 'Mozilla/5.0'}
    url = 'http://economia.awesomeapi.com.br/json/last/USD-BRL'

    response = requests.get(url, headers=header)

    assert response.status_code == 200


WITH 
    OWNER = moedas_dl
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.utf8'
    LC_CTYPE = 'en_US.utf8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;