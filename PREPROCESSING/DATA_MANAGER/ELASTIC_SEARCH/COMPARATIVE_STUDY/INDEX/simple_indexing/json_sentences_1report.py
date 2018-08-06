import pandas as pd
import numpy as np
import json
import sys

# FUNCTION TO CLEAN THE SKILLS NAMES
def skill_cleaning(df):
    col = df.columns[-1]
    for row in range(0, len(df)):
        df.loc[row, col] = df.loc[row, col].replace('.txt', '')
        df.loc[row, col] = df.loc[row, col].replace('.json', '')
    return df

# FUNCTION TO GENERATE THE FRAME OF THE JSON NEEDED TO UPLOAD SEVERAL DOCS IN ES
def json_generator(id_sentence, sentence, skill_probability, skill):
    my_json = '\n'
    my_json += '{'+'\"'+ 'index' + '\"' + ': {'+ '\"' + '_id' + '\"' + ': {}'.format(id_sentence) + '}}'
    my_json += '\n'
    my_json += '{'+ '\"' + 'sentence' + '\"' + ':' + '\"' + '{}'.format(sentence) + '\",'  \
                + '\"' + 'proba_skill' + '\"' + ': {},'.format(str(skill_probability)) \
                + '\"' + 'skill' + '\"' + ':' + '\"' + '{}'.format(skill) + '\"' + \
                '}'
    return my_json

# FUNCTION TO FILL THE JSON STRUCTURE WITH THE OUR DATA
def df2json(df):
    json_content = ''
    for row in range(0, len(df)):
        json_content += json_generator(str(row), df.loc[row, df.columns[0]], df.loc[row, df.columns[1]], df.loc[row, df.columns[2]])
    return json_content

# READ AND CLEAN THE INPUT DATA
df_classifier = pd.read_excel("./skills_excel.xlsx")
df_classifier.fillna('Aucune compétence', inplace=True)
df_classifier = skill_cleaning(df_classifier)

# STOCK THE DATA AS A JSON SPECIFIC ELASTICSEARCH FILE - FOR THE TEXT TO BE PUSHED IN ES
with open('es_skills.json', 'w') as json_file:
    json_file.write(df2json(df_classifier))
    json_file.close()
