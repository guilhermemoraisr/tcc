import pandas as pd
import inflect

campeonatos = pd.read_csv('../data/classificacao_campeonatos.csv')

campeonatos = campeonatos.rename(columns={
    'Torneio': 'Tournament',
    'Temporada': 'Season',
    'Equipe': 'Team',
    'Slug': 'Slug',
    'Posição': 'Position',
    'Partidas': 'Matches',
    'Vitórias': 'Wins',
    'Gols Pró': 'Goals For',
    'Gols Contra': 'Goals Against',
    'ID da Equipe': 'Team ID',
    'Derrotas': 'Losses',
    'Empates': 'Draws',
    'Pontos': 'Points'
})

# Função para criar perguntas e respostas
def create_qa(row):
    team = row['Team']    
    season = row['Season']

    qa_pairs = []
    for col in campeonatos.columns[4:]:
        if col == 'Position' and pd.notnull(row[col]):
            question = f"What is {team}'s position in the {season}?"
            answer = f"{team}'s position in the {season} is {inflect.engine().ordinal(row[col])}."
        if col == 'Matches' and pd.notnull(row[col]):
            question = f"How many matches has {team} played in the {season}?"
            answer = f"{team} has played {int(row[col])} matches in the {season}."
        if col == 'Wins' and pd.notnull(row[col]):
            question = f"How many matches has {team} won in the {season}?"
            answer = f"{team} has won {int(row[col])} matches in the {season}."
        if col == 'Goals For' and pd.notnull(row[col]):
            question = f"How many goals has {team} scored in the {season}?"
            answer = f"{team} has scored {int(row[col])} goals in the {season}."
        if col == 'Goals Against' and pd.notnull(row[col]):
            question = f"How many goals has {team} conceded in the {season}?"
            answer = f"{team} has conceded {int(row[col])} goals in the {season}."
        if col == 'Losses' and pd.notnull(row[col]):
            question = f"How many matches has {team} lost in the {season}?"
            answer = f"{team} has lost {int(row[col])} matches in the {season}."
        if col == 'Draws' and pd.notnull(row[col]):
            question = f"How many matches has {team} drawn in the {season}?"
            answer = f"{team} has drawn {int(row[col])} matches in the {season}."
        if col == 'Points' and pd.notnull(row[col]):
            question = f"How many points does {team} have in the {season}?"
            answer = f"{team} has {int(row[col])} points in the {season}."

        text = f"<s>[INST] {question} [/INST] {answer} </s>"
        qa_pairs.append({'question': question, 'answer': answer, 'text': text})

    return qa_pairs

# Apply the function to each row of the original dataframe
df_qa = campeonatos.apply(create_qa, axis=1)

# Convert the list of dictionaries into a new dataframe
df_qa = pd.DataFrame(df_qa.explode().tolist())
print(df_qa.info())

# Save the dataframe to a csv file
df_qa.to_csv('../data/guanaco_campeonatos.csv', index=False, sep=';', encoding='utf-8')