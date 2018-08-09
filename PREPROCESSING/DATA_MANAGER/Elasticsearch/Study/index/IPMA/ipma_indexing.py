import sys
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

#sys.argv[1]: skills_paths

# Get all the skills path
def get_skills(skills_paths):
    with open(skills_paths, 'r') as paths_list:
        skills_list = [line.strip() for line in paths_list.readlines()]
        paths_list.close()
    return skills_list

# Build the body of the bulk query
def body_builder(skills_list):
    body = ''
    for id_skill, path_skill in enumerate(skills_list):
        body += '{"index": {'+ \
                    '\"' + '_index' + '\"' + ':' + '\"' + 'ipma'  + '\"' + ',' + \
                    '\"' + '_type' + '\"' + ':' +  '\"' + 'skill'  + '\"' + ',' + \
                    '\"' + '_id' + '\"' + ':' + '\"' + '{}'.format(int(id_skill)) + '\"' + '}' + '}'
        body += '\n'
        with open(path_skill, 'r') as skill:
            # SKILL CONTENT IS TOKENIZED ONE LINE BY SENTENCE
            # NOT GOOD FOR JSON
            data = skill.readlines()
            for i, line in enumerate(data):
                data[i] = line.rstrip().replace('\"', '\\\"')
            content = ' '.join(data)
            body += '{'+ '\"' + 'name' + '\"' + ':' + '\"' + '{}'.format(path_skill.split('/')[-1].replace('_', ' ')) + '\",'  \
                       + '\"' + 'content' + '\"' + ':' + '\"' + '{}'.format(content) + '\"' + '}'  
            body += '\n'
            skill.close()
    return body

# INDEX
res = es.bulk(index="ipma", doc_type='skill', body= body_builder(get_skills(sys.argv[1])))
print('RES: \n{}'.format(res))

