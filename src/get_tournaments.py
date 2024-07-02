import requests
import csv

# Função para obter os dados da API
def obter_dados_tabela(id_torneio, id_temporada):
    url = f"https://api.sofascore.com/api/v1/unique-tournament/{id_torneio}/season/{id_temporada}/standings/total"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    resposta = requests.get(url, headers=headers)
    dados = resposta.json()
    return dados

# Função para obter os torneios
def obter_torneios():
    url = "https://api.sofascore.com/api/v1/config/top-unique-tournaments/BR/football"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    resposta = requests.get(url, headers=headers)
    dados = resposta.json()
    return dados["uniqueTournaments"]

# Função para obter as temporadas de um torneio
def obter_temporadas(id_torneio):
    url = f"https://api.sofascore.com/api/v1/unique-tournament/{id_torneio}/seasons"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    resposta = requests.get(url, headers=headers)
    dados = resposta.json()
    return dados["seasons"]

# Função para processar e exibir os dados da tabela
def exibir_dados_tabela(dados, writer, torneio_nome, temporada_nome):
    # Verifica se a resposta contém dados de classificação
    if "standings" in dados and dados["standings"]:
        # Itera sobre as linhas da tabela
        for linha in dados["standings"][0]["rows"]:
            equipe = linha["team"]["name"]
            slug = linha["team"]["slug"]
            posicao = linha["position"]
            partidas = linha["matches"]
            vitorias = linha["wins"]
            gols_pro = linha["scoresFor"]
            gols_contra = linha["scoresAgainst"]
            equipe_id = linha["team"]["id"]
            derrotas = linha["losses"]
            empates = linha["draws"]
            pontos = linha["points"]

            # Escreve as informações no arquivo CSV
            writer.writerow([torneio_nome, temporada_nome, equipe, slug, posicao, partidas, vitorias, gols_pro, gols_contra, equipe_id, derrotas, empates, pontos])

# Função para percorrer torneios e temporadas
def percorrer_torneios_e_temporadas(writer):
    torneios = obter_torneios()

    # Itera sobre os torneios
    for torneio in torneios:
        torneio_id = torneio["id"]
        torneio_nome = torneio["name"]

        # Obtém as temporadas do torneio
        temporadas = obter_temporadas(torneio_id)

        # Itera sobre as temporadas do torneio
        for temporada in temporadas:
            print(f"Obtendo dados da temporada {temporada['name']} do torneio {torneio_nome}")
            temporada_id = temporada["id"]
            temporada_nome = temporada["name"]

            # Obtém e exibe os dados da tabela de classificação
            dados_tabela = obter_dados_tabela(torneio_id, temporada_id)
            exibir_dados_tabela(dados_tabela, writer, torneio_nome, temporada_nome)

# Abre o arquivo CSV para escrita
with open('classificacao_campeonatos.csv', 'w', newline='', encoding='utf-8') as csvfile:
    # Define o cabeçalho do CSV
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Torneio", "Temporada", "Equipe", "Slug", "Posição", "Partidas", "Vitórias", "Gols Pró", "Gols Contra", "ID da Equipe", "Derrotas", "Empates", "Pontos"])

    # Chama a função para percorrer torneios e temporadas
    percorrer_torneios_e_temporadas(csv_writer)

print("Resultados salvos em 'classificacao_campeonatos.csv'.")
