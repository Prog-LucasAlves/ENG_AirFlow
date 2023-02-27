import pandas as pd

def transforma ():
    data = pd.read_csv('/var/transfer/dadosColetados.csv')
    data['name'] = data['name'].str.upper()
    data['high'] = round(data['high'], 3)
    data['low'] = round(data['low'], 3)
    data['varBid'] = round(data['varBid'], 3)
    data['pctChange'] = round(data['pctChange'], 2)
    data['bid'] = round(data['bid'], 3)
    data['ask'] = round(data['ask'], 3)

    data.to_csv('/var/transfer/dadosColetadosT.csv', index=False)

if __name__ == '__main__':
    transforma()
