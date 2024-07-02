import pandas as pd
import requests
from datetime import datetime, timedelta

def obter_dados_jogadores(id_equipe):
    url = f'https://api.sofascore.com/api/v1/team/{id_equipe}/players'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    resposta = requests.get(url, headers=headers)
    dados_jogadores = resposta.json()
    return dados_jogadores['players'] if 'players' in dados_jogadores else []

def print_and_convert(x):
    if pd.isnull(x):
        return None
    datetime_obj = datetime(1970, 1, 1) + timedelta(seconds=x)
    return datetime_obj.strftime('%Y-%m-%d %H:%M:%S')


# Passo 2: Leia o CSV como um DataFrame
df = pd.read_csv('detalhes_equipes.csv')

# Passo 4: Itere sobre os valores únicos da coluna "ID da Equipe" e colete os dados dos jogadores
dados_jogadores = []
total = len(df['ID'].unique())

for id_equipe in df['ID'].unique():

    total = total - 1
    print(f"Equipe {id_equipe} - Faltam {total}.")
    jogadores = obter_dados_jogadores(id_equipe)
    dados_jogadores.extend(jogadores)

# Passo 5: Transforme os dados coletados em um DataFrame
df_jogadores = pd.json_normalize(dados_jogadores)

# Passo 6: Converta os timestamps para o formato de data adequado
colunas_timestamp = ['player.dateOfBirthTimestamp', 'player.contractUntilTimestamp']
df_jogadores[colunas_timestamp] = df_jogadores[colunas_timestamp].applymap(print_and_convert)

# Passo 7: Salve o DataFrame resultante em um novo arquivo CSV
df_jogadores.to_csv('jogadores.csv', index=False)
