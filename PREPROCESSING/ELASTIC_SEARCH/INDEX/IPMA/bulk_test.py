import sys
from datetime import datetime
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

# Get all the skills documentation
def get_skills(skills_list_paths):
    with open(skills_list_paths, 'r') as paths_list:
        skills_files = [line.strip() for line in paths_list.readlines()]
        paths_list.close()
    return skills_files

def doc_builder(skill_name, skill_number):
    with open(skill_name[int(skill_number)], 'r') as skill:
        skill_content = str(skill.read())
        skill.close()
    return {'skill': str(skill_name[int(skill_number)].split('/')[-1].replace('_', ' ')), 'content': skill_content}
'''
#1
doc = '{'+'\"'+ 'index' + '\"' + ': {'+ \
            '\"' + '_index' + '\"' + ':' + '\"' + 'ipma_test'  + '\"' + ',' + \
            '\"' + '_type' + '\"' + ':' +  '\"' + 'skill'  + '\"' + ',' + \
            '\"' + '_id' + '\"' + ':' + '\"' + '1' + '\"' + '}' + '}'

doc += '\n'
doc += '{'+ '\"' + 'name' + '\"' + ':' + '\"' + 'Leadership' + '\",'  \
          + '\"' + 'content' + '\"' + ':' + '\"' + 'On ne naît pas leader, on le devient.' + '\"' + '}'  
doc += '\n'

#2
doc += '{'+'\"'+ 'index' + '\"' + ': {'+ \
            '\"' + '_index' + '\"' + ':' + '\"' + 'ipma_test'  + '\"' + ',' + \
            '\"' + '_type' + '\"' + ':' +  '\"' + 'skill'  + '\"' + ',' + \
            '\"' + '_id' + '\"' + ':' + '\"' + '2' + '\"' + '}'+ '}'

doc += '\n'
doc += '{'+ '\"' + 'name' + '\"' + ':' + '\"' + 'Technologies' + '\",'  \
          + '\"' + 'content' + '\"' + ':' + '\"' + 'Qu\'il est bon d\'être technophile !' + '\"' + '}'  
doc += '\n'

#3
doc += '{'+'\"'+ 'index' + '\"' + ': {'+ \
            '\"' + '_index' + '\"' + ':' + '\"' + 'ipma_test'  + '\"' + ',' + \
            '\"' + '_type' + '\"' + ':' +  '\"' + 'skill'  + '\"' + ',' + \
            '\"' + '_id' + '\"' + ':' + '\"' + '3' + '\"' + '}'+ '}'

doc += '\n'
doc += '{'+ '\"' + 'name' + '\"' + ':' + '\"' + 'Team management' + '\",'  \
          + '\"' + 'content' + '\"' + ':' + '\"' + 'Tout est dans la tête les gars, on peut le faire!' + '\"' + '}'  
doc += '\n'

#4
doc += '{'+'\"'+ 'index' + '\"' + ': {'+ \
            '\"' + '_index' + '\"' + ':' + '\"' + 'ipma_test'  + '\"' + ',' + \
            '\"' + '_type' + '\"' + ':' +  '\"' + 'skill'  + '\"' + ',' + \
            '\"' + '_id' + '\"' + ':' + '\"' + '4' + '\"' + '}'+ '}'

doc += '\n'
doc += '{'+ '\"' + 'name' + '\"' + ':' + '\"' + 'Control' + '\",'  \
          + '\"' + 'content' + '\"' + ':' + '\"' + 'Maitrise du sujet' + '\"' + '}'  
doc += '\n'

#5
doc += '{'+'\"'+ 'index' + '\"' + ': {'+ \
            '\"' + '_index' + '\"' + ':' + '\"' + 'ipma_test'  + '\"' + ',' + \
            '\"' + '_type' + '\"' + ':' +  '\"' + 'skill'  + '\"' + ',' + \
            '\"' + '_id' + '\"' + ':' + '\"' + '5' + '\"' + '}'+ '}'

doc += '\n'
doc += '{'+ '\"' + 'name' + '\"' + ':' + '\"' + 'Finition' + '\",'  \
        + '\"' + 'content' + '\"' + ':' + '\"' + 'Phase finale: on termine tout le monde.' + '\"' + '}'  
doc += '\n'


#print(doc)


res = es.bulk(index="ipma_test", doc_type='skill', body=doc)

print('----------------------------------------')
print('RES: \n{}'.format(res))
print('----------------------------------------')
#print('RES[_source]: \n{}'.format(res['_source']))
print('----------------------------------------')
print('res[\'result\']):\n{}'.format(res['result']))
'''

#res = es.get(index="ipma_test", doc_type='skill', id=4)

#print(res['_source'])

#es.indices.refresh(index="ipma_test")

res = es.search(index="ipma_test", body={"query": {"match_all": {}}})

print("Got %d Hits:" % res['hits']['total'])
#print(res['hits']['hits'])

for hit in res['hits']['hits']:
        print( hit["_source"]["content"])
        print('\n')

