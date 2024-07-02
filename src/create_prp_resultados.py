import pandas as pd

resultados = pd.read_csv('../data/resultados_jogos.csv')

resultados = resultados.rename(columns={
    'Torneio': 'Tournament',
    'Temporada': 'Season',
    'Time da Casa': 'Home Team',
    'Time Visitante': 'Away Team',
    'Placar Casa': 'Home Score',
    'Placar Visitante': 'Away Score',
    'Data do Jogo': 'Game Date'
})

# Função para criar perguntas e respostas
def create_qa(row):
    season = row['Season']
    home_team = row['Home Team']    
    away_team = row['Away Team']
    game_date = row['Game Date']

    qa_pairs = []

    question = ''  # Initialize question
    answer = ''  # Initialize answer
    if pd.notnull(row['Home Score']) and pd.notnull(row['Away Score']):
        question = f"What was the score for {home_team} against {away_team} on {game_date} in the {season}?"
        answer = f"The score for {home_team} against {away_team} on {game_date} was {row['Home Score']}-{row['Away Score']}."

    if question and answer:  # Only append if question and answer are not empty
        text = f"<s>[INST] {question} [/INST] {answer} </s>"
        qa_pairs.append({'question': question, 'answer': answer, 'text': text})

    if not qa_pairs:  # If qa_pairs is empty, return a dictionary with empty strings
        qa_pairs.append({'question': '', 'answer': '', 'text': ''})

    return qa_pairs

# Apply the function to each row of the original dataframe
df_qa = resultados.apply(create_qa, axis=1)

# Convert the list of dictionaries into a new dataframe
df_qa = pd.DataFrame(df_qa.explode().tolist())
df_qa = df_qa[df_qa['question'] != '']
empty_questions = df_qa[df_qa['text'] == '']

print(df_qa.info())

# Save the dataframe to a csv file
df_qa.to_csv('../data/guanaco_resultados.csv', index=False, sep=';', encoding='utf-8')