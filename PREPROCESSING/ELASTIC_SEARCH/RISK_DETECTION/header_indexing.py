import re
import timeit
import sys
import json
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

unicode_reg = re.compile(u"[\u00e9]")
ponctuation_reg = re.compile("[\ -/:-@\[-`{-~]")
bytes_reg = re.compile(b"[\xc3]")
#sys.argv[1]: headers_paths
def invalid_byte_cleaner(sentence):
    return sentence.replace(b'\xc3'.decode("utf-8", "replace"), '')

def string_cleaner(sentence, reg):
    return reg.sub('', sentence)

# Get all the headers path
def get_headers(headers_paths):
    with open(headers_paths, 'r') as paths_list:
        headers_list = [line.strip() for line in paths_list.readlines()]
        paths_list.close()
    return headers_list

def body_builder(headers_list):
    body_meta = []
    body_core = []
    for id_header, path_header in enumerate(headers_list):
        body_meta.append(json.JSONEncoder().encode({'index': {'_index': 'hydro_head', '_type': 'header', '_id': id_header}}))
        with open(path_header, 'rb') as header:
            data = [line.strip().decode('utf-8','ignore') for line in header.readlines()]
            header.close()
        content = [' '.join(field.split(':')[1:]).replace('\u00e9', u'é') for field in data]
        #print(content)
        #print('{' + '\"id_mail\": {},'.format() '\"sender\": {},' '\"timestamp\": {},' '\"receiver\": {},' '\"distribution\":{}, \"title\":{}\}'.format(path_header.split('/')[-1], content[0], content[1], content[2], content[3], content[4]))

        if (len(content) == 7):
            body_core.append(json.JSONEncoder().encode({'id_mail': path_header.split('/')[-1], 'sender' : content[0], 'timestamp': content[1],\
                    'receiver': content[4], 'distribution': content[5], 'title': content[6]}))
        elif (len(content) == 6):
            body_core.append(json.JSONEncoder().encode({'id_mail': path_header.split('/')[-1], 'sender' : content[1], 'timestamp': content[2],\
                    'receiver': content[3], 'distribution': content[4], 'title': content[5]}))
        elif (len(content) == 5):
            body_core.append(json.JSONEncoder().encode({'id_mail': path_header.split('/')[-1], 'sender' : content[0], 'timestamp': content[1],\
                    'receiver': content[2], 'distribution': content[3], 'title': content[4]}))
        elif(len(content) == 4):
            body_core.append(json.JSONEncoder().encode({'id_mail': path_header.split('/')[-1], 'sender' : content[0], 'timestamp': content[1],\
                    'receiver': content[2], 'distribution': 'unknown', 'title': content[3]}))
        elif(len(content) == 3):
            body_core.append(json.JSONEncoder().encode({'id_mail': path_header.split('/')[-1], 'sender' : 'unknown', 'timestamp': 'unknown',\
                    'receiver': content[0], 'distribution': content[1], 'title': content[2]}))
        elif(len(content) == 2):
            body_core.append(json.JSONEncoder().encode({'id_mail': path_header.split('/')[-1], 'sender' : content[0], 'timestamp': content[1],\
                    'receiver': 'unknown', 'distribution': 'unknown', 'title': 'unknown'}))
        elif(len(content) == 1):
            body_core.append(json.JSONEncoder().encode({'id_mail': path_header.split('/')[-1], 'sender' : content[0], 'timestamp': 'unknown',\
                    'receiver': 'unknown', 'distribution': 'unknown', 'title': 'unknown'}))
        elif(len(content) == 0):
            body_core.append(json.JSONEncoder().encode({'id_mail': path_header.split('/')[-1], 'sender' : 'unknown', 'timestamp': 'unknown',\
                    'receiver': 'unknown', 'distribution': 'unknown', 'title': 'unknown'}))
        else:
            print(len(content))
            print(path_header)
            print('INFORMATION IS  MISSING')
        print(body_core[id_header])
    return (body_meta, body_core)

with open('headers.json', 'w') as json_file:
    headers = body_builder(get_headers(sys.argv[1]))
    meta = headers[0]
    core = headers[1]
    for doc in range(len(meta)):
        json_file.write(meta[doc])
        json_file.write('\n')
        json_file.write(core[doc])
        json_file.write('\n')
    json_file.close()

#print(body_builder(get_headers(sys.argv[1])))

'''
# INDEX
res = es.bulk(index="hydro_head", doc_type='header', body= body_builder(get_headers(sys.argv[1])))
print('RES: \n{}'.format(res))
'''
