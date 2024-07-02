import pandas as pd
from datetime import datetime, timedelta

def converter_timestamp(timestamp):
    if timestamp is None:
        return None
    datetime_obj = datetime(1970, 1, 1) + timedelta(seconds=timestamp)
    return datetime_obj.strftime('%Y-%m-%d %H:%M:%S')

equipes = pd.read_csv('../data/detalhes_equipes.csv')

equipes = equipes.rename(columns={
    'Torneio': 'Tournament',
    'Temporada': 'Season',
    'Equipe': 'Team',
    'Nome': 'Name',
    'Slug': 'Slug',
    'Short Name': 'Short Name',
    'Gender': 'Gender',
    'Sport': 'Sport',
    'Category': 'Category',
    'Tournament': 'Tournament',
    'Manager': 'Manager',
    'Venue': 'Venue',
    'Foundation Date': 'Foundation Date',
    'ID': 'ID',
    'Country': 'Country',
    'Full Name': 'Full Name',
    'Team Colors': 'Team Colors'
})
equipes = equipes[['Team','Season','Manager','Venue','Foundation Date','Country','Full Name']]


def create_qa(row):
    team = row['Team']    
    season = row['Season']

    qa_pairs = []
    for col in equipes.columns[2:]:
        question = ''  # Initialize question
        answer = ''  # Initialize answer
        if col == 'Manager' and pd.notnull(row[col]):
            question = f"Who is the manager of {team} in the {season}?"
            answer = f"The manager of {team} in the {season} is {row[col]}."
        if col == 'Venue' and pd.notnull(row[col]):
            question = f"Where does {team} play their home games in the {season}?"
            answer = f"{team} plays their home games at {row[col]} in the {season}."
        if col == 'Foundation Date' and pd.notnull(row[col]):
            foundation_date = datetime.strptime(row[col], '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
            question = f"When was {team} founded?"
            answer = f"{team} was founded on {foundation_date}."
        if col == 'Country' and pd.notnull(row[col]):
            question = f"In which country is {team} based?"
            answer = f"{team} is based in {row[col]}."
        if col == 'Full Name' and pd.notnull(row[col]):
            question = f"What is the full name of {team}?"
            answer = f"The full name of {team} is {row[col]}."

        if question and answer:  # Only append if question and answer are not empty
            text = f"<s>[INST] {question} [/INST] {answer} </s>"
            qa_pairs.append({'question': question, 'answer': answer, 'text': text})

    return qa_pairs

# Apply the function to each row of the original dataframe
df_qa = equipes.apply(create_qa, axis=1)

# Convert the list of dictionaries into a new dataframe
df_qa = pd.DataFrame(df_qa.explode().tolist())
print(df_qa.info())

# Save the dataframe to a csv file
df_qa.to_csv('../data/guanaco_equipes.csv', index=False, sep=';', encoding='utf-8')