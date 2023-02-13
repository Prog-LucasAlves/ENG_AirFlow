import requests
import json
import pandas as pd

from datetime import datetime, timedelta, timezone
import scripts.list_tikers as tk

MOEDAS = tk.tickers
#MOEDAS = list_tikers.tickers

def captura_dados() -> list:

    result_code : list = []
    result_codein : list = []
    result_name : list = []
    result_high : list = []
    result_low : list = []
    result_varBid : list = []
    result_pctChange : list = []
    result_bid : list = []
    result_ask : list = []
    
    dadosColetados = pd.DataFrame()

    for ticker in MOEDAS:

        header = {'user-agent':'Mozilla/5.0'}
        url = f'http://economia.awesomeapi.com.br/json/last/{ticker}'
        site = requests.get(url, headers=header)
        dados = json.loads(site.text)

        ticker = ticker.replace('-', '')
        code = dados[ticker]['code']
        codein = dados[ticker]['codein']
        name = dados[ticker]['name']
        high = dados[ticker]['high']
        low = dados[ticker]['low']
        varBid = dados[ticker]['varBid']
        pctChange = dados[ticker]['pctChange']
        bid = dados[ticker]['bid']
        ask = dados[ticker]['ask']

        result_code.append(code)
        result_codein.append(codein)
        result_name.append(name)
        result_high.append(high)
        result_low.append(low)
        result_varBid.append(varBid)
        result_pctChange.append(pctChange)
        result_bid.append(bid)
        result_ask.append(ask)
        create_date = datetime.now()
    
    dadosColetados['code'] = result_code
    dadosColetados['codein'] = result_codein
    dadosColetados['name'] = result_name
    dadosColetados['high'] = result_high
    dadosColetados['low'] = result_low
    dadosColetados['varBid'] = result_varBid
    dadosColetados['pctChange'] = result_pctChange
    dadosColetados['bid'] = result_bid
    dadosColetados['ask'] = result_ask
    dadosColetados['create_date'] = create_date
    dadosColetados.to_csv('/var/transfer/dadosColetados.csv', index=False)
        
    return list(result_code), list(result_codein), list(result_name), list(result_high), list(result_low), list(result_varBid), list(result_pctChange), list(result_bid), list(result_ask)

if __name__ == '__main__':
    captura_dados()
