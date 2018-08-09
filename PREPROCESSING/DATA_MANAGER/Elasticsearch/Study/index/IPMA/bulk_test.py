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
res = es.search(index="ipma_test", body={"query": {"match_all": {}}})

print("Got %d Hits:" % res['hits']['total'])

for hit in res['hits']['hits']:
        print( hit["_source"]["content"])
        print('\n')

