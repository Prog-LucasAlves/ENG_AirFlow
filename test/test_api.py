import requests

def test_api():
    header = {'user-agent':'Mozilla/5.0'}
    url = f'http://economia.awesomeapi.com.br/json/last/USD-BRL'

    response = requests.get(url, headers=header)

    assert response.status_code == 200