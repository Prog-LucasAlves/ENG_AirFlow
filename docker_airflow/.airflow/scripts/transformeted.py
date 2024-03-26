import pandas as pd


def transforma():
    """
    Função para transformar os dados coletados em um arquivo .csv
    """
    # Carregando os dados coletados
    data = pd.read_csv("/var/transfer/dadosColetados.csv")

    # Colocando os dados da coluna 'name' em maiúsculo
    data["name"] = data["name"].str.upper()

    # Arredondando os dados da coluna 'high' para 3 casas decimais
    data["high"] = round(data["high"], 3)

    # Arredondando os dados da coluna 'low' para 3 casas decimais
    data["low"] = round(data["low"], 3)

    # Arredondando os dados da coluna 'varBid' para 3 casas decimais
    data["varBid"] = round(data["varBid"], 3)

    # Arredondando os dados da coluna 'pctChange' para 2 casas decimais
    data["pctChange"] = round(data["pctChange"], 2)

    # Arredondando os dados da coluna 'bid' para 3 casas decimais
    data["bid"] = round(data["bid"], 3)

    # Arredondando os dados da coluna 'ask' para 3 casas decimais
    data["ask"] = round(data["ask"], 3)

    # Filtro ask maior bid
    data = data[data["ask"] >= data["bid"]]

    # Salvando os dados
    data.to_csv("/var/transfer/dadosColetadosT.csv", index=False)


if __name__ == "__main__":
    transforma()
