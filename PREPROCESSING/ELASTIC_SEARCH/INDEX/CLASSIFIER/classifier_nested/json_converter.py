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

# POPULATE YOUR NESTED OBJECT
def nested_objects_generator(sentence, skill_probability, skill, delimiter):
    nested_structure =  '{'+ '\"' + 'sentence' + '\"' + ':' + '\"' + '{}'.format(string_cleaner(str(sentence))) + '\",'  \
                           + '\"' + 'proba_skill' + '\"' + ':' +   '\"' + '{}'.format(skill_probability) + '\",' \
                           + '\"' + 'skill' + '\"' + ':' + '\"' + '{}'.format(str(skill)) + '\"' + '}' + '{}'.format(delimiter)
    return nested_structure


# GENERATE THE FRAME OF THE JSON
def json_generator(title, df):
    my_json = '\n'
    my_json += '{'+ '\"' + 'name' + '\"' + ':' + '\"' + '{}'.format(title) + '\",'  \
                + '\"' + 'sentences' + '\"' + ': [' 
    for row in range(len(df)):
        if (row < (len(df)-1)):
            my_json += nested_objects_generator(df.loc[row, df.columns[0]], float(df.loc[row, df.columns[1]]), df.loc[row, df.columns[2]], ",")
        else:
            my_json += nested_objects_generator(df.loc[row, df.columns[0]], float(df.loc[row, df.columns[1]]), df.loc[row, df.columns[2]], "")
    my_json += ']}'
    my_json += '\n'
    return my_json

# FILL THE JSON STRUCTURE WITH YOUR DATA
def df2json(excel_path):
    worksheets = pd.ExcelFile(excel_path)
    # HERE THE TITLES HAVE BEEN ANONYMISED (range(172))
    titles = range(172)
    json_content = ''
    for doc_number, doc_name in enumerate(titles):
        ## the worksheet names can only contain 31 characters maximum
        df = pd.read_excel(worksheets, str(doc_number))
        print(doc_number)
        df.fillna('Aucune compétence', inplace=True)
        df = skill_cleaning(df)
        json_content += '{'+'\"'+ 'index' + '\"' + ': {'+ \
                           '\"' + '_index' + '\"' + ':' + '\"' + 'classifier_nested'  + '\"' + ',' + \
                           '\"' + '_type' + '\"' + ':' +  '\"' + 'reports'  + '\"' + ',' + \
                           '\"' + '_id' + '\"' + ':' + '\"' + '{}'.format(str(doc_number)) + '\"' + '}}'
        json_content += json_generator(doc_number, df) 
    return json_content

# STOCK THE DATA AS A JSON SPECIFIC ELASTICSEARCH FILE (FOR THE TEXT TO BE PUSHED IN ES)
with open('classifier.json', 'w') as json_file:
    json_file.write(df2json(sys.argv[1]))
    json_file.close()

