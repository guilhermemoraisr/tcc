import pandas as pd
from datetime import datetime

jogadores = pd.read_csv('../data/jogadores.csv')

jogadores = jogadores[['player.name','player.team.name','player.team.sport.name','player.team.tournament.name','player.position','player.preferredFoot','player.height','player.jerseyNumber','player.country.name','player.dateOfBirthTimestamp','player.contractUntilTimestamp','player.proposedMarketValue']]
jogadores = jogadores.rename(columns={
    'player.name': 'name',
    'player.team.name': 'team_name',
    'player.team.sport.name': 'sport_name',
    'player.team.tournament.name': 'tournament_name',
    'player.position': 'position',
    'player.preferredFoot': 'preferred_foot',
    'player.height': 'height',
    'player.jerseyNumber': 'jersey_number',
    'player.country.name': 'country_name',
    'player.dateOfBirthTimestamp': 'date_of_birth',
    'player.contractUntilTimestamp': 'contract_until',
    'player.proposedMarketValue': 'proposed_market_value'
})

# Função para criar perguntas e respostas
def create_qa(row):
    name = row['name']

    qa_pairs = []
    for col in jogadores.columns[1:]:

        if col == 'team_name' and pd.notnull(row[col]):
            question = f"What team does {name} play for?"
            answer = f"{name} plays for {row[col]}."
        if col == 'sport_name' and pd.notnull(row[col]):
            question = f"What sport does {name} play?"
            answer = f"{name} plays {row[col]}."
        if col == 'tournament_name' and pd.notnull(row[col]):
            question = f"What championship does {name} play in?"
            answer = f"{name} plays in the {row[col]} championship."
        if col == 'position' and pd.notnull(row[col]):
            question = f"In which position does {name} play?"
            answer = f"{name} plays as a {row[col]}."
        if col == 'preferred_foot' and pd.notnull(row[col]):
            question = f"Which is {name}'s preferred foot?"
            answer = f"{name}'s preferred foot is {row[col]}."
        if col == 'height' and pd.notnull(row[col]):
            question = f"How tall is {name}?"
            answer = f"{name} is {int(row[col])} cm tall."
        if col == 'jersey_number' and pd.notnull(row[col]):
            question = f"What is {name}'s jersey number?"
            answer = f"{name}'s jersey number is {int(row[col])}."
        if col == 'country_name' and pd.notnull(row[col]):
            question = f"Which country does {name} represent?"
            answer = f"{name} represents {row[col]}."
        if col == 'date_of_birth' and pd.notnull(row[col]):
            date_of_birth = datetime.strptime(row[col], '%Y-%m-%d %H:%M:%S')
            date_of_birth = date_of_birth.strftime('%m/%d/%Y')
            question = f"When was {name} born?"
            answer = f"{name} was born on {date_of_birth}."
        if col == 'contract_until' and pd.notnull(row[col]):
            contract_until = datetime.strptime(row[col], '%Y-%m-%d %H:%M:%S')
            contract_until = contract_until.strftime('%m/%d/%Y')
            question = f"When does {name}'s contract expire?"
            answer = f"{name}'s contract expires on {contract_until}."
        if col == 'proposed_market_value' and pd.notnull(row[col]):
            question = f"What is the proposed market value for {name}?"
            answer = f"The proposed market value for {name} is {int(row[col])} EUR."

        
        text = f"<s>[INST] {question} [/INST] {answer} </s>"
        qa_pairs.append({'question': question, 'answer': answer, 'text': text})

    return qa_pairs

# Aplicar a função a cada linha do dataframe original
df_qa = jogadores.apply(create_qa, axis=1)

# Converter a lista de dicionários em um novo dataframe
df_qa = pd.DataFrame(df_qa.explode().tolist())
print(df_qa.info())

# Salvar o dataframe em um arquivo csv
df_qa.to_csv('../data/guanaco_jogadores.csv', index=False, sep=';', encoding='utf-8')