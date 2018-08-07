import json
import pandas as pd
import numpy as np
import sys
import re

# CLEAN YOUR DATA
def skill_cleaning(df):
    col = df.columns[-1]
    for row in range(0, len(df)):
        df.loc[row, col] = df.loc[row, col].replace('.txt', '')
        df.loc[row, col] = df.loc[row, col].replace('.json', '')
        df.loc[row, col] = df.loc[row, col].replace('_', ' ')
    return df

def string_cleaner(sentence):
    return re.sub(r"[=.:><'•§œ;/)(!?@\\\'\`\"\_\n]", r"", sentence)

# FILL THE JSON STRUCTURE WITH YOUR DATA
def df_to_json(excel_path):
    worksheets = pd.ExcelFile(excel_path)
    # HERE THE TITLES HAVE BEEN ANONYMISED (range(172))
    titles = range(172)
    nb_sentence = 0
    for doc_number, doc_name in enumerate(titles):
        # One worksheet by report
        df = pd.read_excel(worksheets, str(doc_number))
        print(doc_number)
        df.fillna('Aucune compétence', inplace=True)
        df = skill_cleaning(df)
        json_content = []
        # One row by sentence
        for row in range(len(df)):
            json_content.append(json.JSONEncoder().encode({'index':{'_index': 'classifier', \
                    '_type': 'sentences', '_id': str(nb_sentence)}}))
            json_content.append(json.JSONEncoder().encode({'report_id': doc_number, 'sentence': df.loc[row, df.columns[0]] ,\
                    'proba_skill': float(df.loc[row, df.columns[1]]), 'skill': df.loc[row, df.columns[2]]}))
            nb_sentence += 1
    return json_content

# STOCK THE DATA AS A JSON SPECIFIC ELASTICSEARCH FILE (FOR THE TEXT TO BE PUSHED IN ES)
with open('classifier.json', 'w') as json_file:
    sentences = df_to_json(sys.argv[1])
    for doc in sentences:
        json_file.write(doc)
        json_file.write('\n')
    json_file.close()

