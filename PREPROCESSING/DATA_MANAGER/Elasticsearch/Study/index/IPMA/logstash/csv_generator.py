import pandas as pd
import sys
import os

# GENERATE THE LIST OF ALL PDF SOURCES PATHS
def path_generator(initial_root):
    for root, dirs, files in os.walk(initial_root):
        paths = [os.path.join(root, name) for name in files]
    return paths

def get_content(paths_list):
    skill_names = []
    skill_content = []
    for num_path, path in enumerate(paths_list):
        skill_names.append(path.split('/')[-1].replace('_',' '))
        with open(path, 'r') as skill_path:
            skill_content.append(skill_path.read())
            skill_path.close()
    df = pd.DataFrame(columns = ['skill', 'content'])
    df['skill'] = skill_names
    df['content'] = skill_content
    return df

def get_csv(df):
    return df.to_csv('ipma.csv', index=True, sep='^')

get_csv(get_content(path_generator(sys.argv[1])))


