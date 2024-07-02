import requests, csv
from datetime import datetime, timedelta

def converter_timestamp(timestamp):
    if timestamp is None:
        return None
    datetime_obj = datetime(1970, 1, 1) + timedelta(seconds=timestamp)
    return datetime_obj.strftime('%Y-%m-%d %H:%M:%S')

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

# Função para obter os dados da API
def obter_dados_resultados_jogos(id_torneio, id_temporada, num_evento):
    url = f"https://api.sofascore.com/api/v1/unique-tournament/{id_torneio}/season/{id_temporada}/events/last/{num_evento}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    resposta = requests.get(url, headers=headers)
    
    # Se o status da resposta for 404, retorne None
    if resposta.status_code == 404:
        return None
    
    dados = resposta.json()
    return dados

# Função para exibir os dados dos resultados dos jogos
def exibir_dados_resultados_jogos(dados, writer, torneio_nome, temporada_nome):
    if "events" in dados:
        for evento in dados["events"]:
            home_team = evento["homeTeam"].get("name")
            away_team = evento["awayTeam"].get("name")
            home_score = evento["homeScore"].get("current")
            away_score = evento["awayScore"].get("current")
            status = evento["status"].get("description")
            start_timestamp = evento.get("startTimestamp")

            # Converter timestamp para formato de data
            data_do_jogo = converter_timestamp(start_timestamp)

            # Escreve as informações no arquivo CSV
            writer.writerow([torneio_nome, temporada_nome, home_team, away_team, home_score, away_score, status, data_do_jogo])

# Função para percorrer torneios e temporadas
def percorrer_torneios_e_temporadas(writer):
    torneios = obter_torneios()
    total_torneios = len(torneios)

    # Itera sobre os torneios
    for i, torneio in enumerate(torneios):
        torneio_id = torneio["id"]
        torneio_nome = torneio["name"]

        # Obtém as temporadas do torneio
        temporadas = obter_temporadas(torneio_id)

        # Itera sobre as temporadas do torneio
        for temporada in temporadas:
            print(f"Obtendo dados da temporada {temporada['name']} do torneio {torneio_nome} - {torneio_id}/{temporada['id']}")
            temporada_id = temporada["id"]
            temporada_nome = temporada["name"]

            # Inicializa o número do evento
            num_evento = 0

            # Continua obtendo dados enquanto houver resposta
            while True:
                print(f"Tabela {num_evento}")
                # Obtém e exibe os dados dos resultados dos jogos
                dados_resultados_jogos = obter_dados_resultados_jogos(torneio_id, temporada_id, num_evento)
                
                # Se não houver dados, pare o loop
                if dados_resultados_jogos is None:
                    break
                
                exibir_dados_resultados_jogos(dados_resultados_jogos, writer, torneio_nome, temporada_nome)
                
                # Incrementa o número do evento para a próxima iteração
                num_evento += 1

        torneios_restantes = total_torneios - (i + 1)
        print(f"Torneios restantes: {torneios_restantes}")

# Abre o arquivo CSV para escrita
with open('resultados_jogos.csv', 'w', newline='', encoding='utf-8') as csvfile:
    # Define o cabeçalho do CSV
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Torneio", "Temporada", "Time da Casa", "Time Visitante", "Placar Casa", "Placar Visitante", "Status", "Data do Jogo"])

    # Chama a função para percorrer torneios e temporadas
    percorrer_torneios_e_temporadas(csv_writer)

print("Resultados dos jogos salvos em 'resultados_jogos.csv'.")
