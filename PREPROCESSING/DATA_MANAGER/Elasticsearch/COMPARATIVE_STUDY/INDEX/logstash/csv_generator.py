import pandas as pd
import sys

#sys.argv[1]: filename of the ipma chapters text file

def get_paths(ipma_paths):
    with open(ipma_paths, 'r') as paths_list:
        paths = [line.strip() for line in paths_list.readlines()]
        paths_list.close()
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

get_csv(get_content(get_paths(sys.argv[1])))


