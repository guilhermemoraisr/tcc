import pandas as pd
import requests
from datetime import datetime, timedelta

# Função para obter os detalhes de uma equipe
def obter_detalhes_equipe(id_equipe):
    url = f"https://api.sofascore.com/api/v1/team/{id_equipe}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    resposta = requests.get(url, headers=headers)
    dados = resposta.json()
    return dados

# Função para converter o formato do timestamp Unix para datetime
def converter_timestamp(timestamp):
    if timestamp is None:
        return None
    datetime_obj = datetime(1970, 1, 1) + timedelta(seconds=timestamp)
    return datetime_obj.strftime('%Y-%m-%d %H:%M:%S')

# Função principal
def obter_detalhes_equipes_e_salvar_csv(input_csv, output_csv):
    # Lê o CSV de entrada como um DataFrame do pandas
    df = pd.read_csv(input_csv).drop_duplicates(subset='ID da Equipe')
    print(f"Total de equipes: {len(df)}")

    # Lista para armazenar os dados das equipes
    dados_equipes = []

    # Itera sobre as linhas do DataFrame
    for index, row in df.iterrows():

        print(f"{row['Equipe']} - {row['ID da Equipe']}")
        equipe_id = row['ID da Equipe']

        # Obtém detalhes da equipe
        detalhes_equipe = obter_detalhes_equipe(equipe_id)
        # print(detalhes_equipe['team']['manager']['name'], '\n')

        # Adiciona informações relevantes à lista
        dados_equipes.append({
            'Torneio': row['Torneio'],
            'Temporada': row['Temporada'],
            'Equipe': row['Equipe'],
            'Nome': detalhes_equipe['team']['name'],
            'Slug': detalhes_equipe['team']['slug'] if 'slug' in detalhes_equipe['team'] else None,
            'Short Name': detalhes_equipe['team']['shortName'] if 'shortName' in detalhes_equipe['team'] else None,
            'Gender': detalhes_equipe['team']['gender'] if 'gender' in detalhes_equipe['team'] else None,
            'Sport': detalhes_equipe['team']['sport']['name'] if 'sport' in detalhes_equipe['team'] else None,
            'Category': detalhes_equipe['team']['category']['name'] if 'category' in detalhes_equipe['team'] else None,
            'Tournament': detalhes_equipe['team']['tournament']['name'] if 'tournament' in detalhes_equipe['team'] else None,
            'Manager': detalhes_equipe['team']['manager']['name'] if 'manager' in detalhes_equipe['team'] else None,
            'Venue': detalhes_equipe['team']['venue']['stadium']['name'] if 'venue' in detalhes_equipe['team'] else None,
            'Foundation Date': converter_timestamp(detalhes_equipe['team'].get('foundationDateTimestamp', None)),
            'ID': detalhes_equipe['team']['id'] if 'id' in detalhes_equipe['team'] else None,
            'Country': detalhes_equipe['team']['country'].get('name', None), 
            'Full Name': detalhes_equipe['team']['fullName'] if 'fullName' in detalhes_equipe['team'] else None,
            'Team Colors': detalhes_equipe['team']['teamColors']['primary'] if 'teamColors' in detalhes_equipe['team'] else None
        })

    # Cria um DataFrame a partir da lista de dados das equipes
    df_equipes = pd.DataFrame(dados_equipes)

    # Salva o DataFrame em um novo CSV
    df_equipes.to_csv(output_csv, index=False)

# Chama a função principal
obter_detalhes_equipes_e_salvar_csv('classificacao_campeonatos.csv', 'detalhes_equipes.csv')

print("Detalhes das equipes salvos em 'detalhes_equipes.csv'.")
