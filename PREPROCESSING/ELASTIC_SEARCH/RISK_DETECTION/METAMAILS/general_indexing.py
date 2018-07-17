import re
import sys
import json
from elasticsearch import Elasticsearch

#sys.argv[1]: file containing the headers paths, one path per line
#sys.argv[2]: file containing the mails paths, one path per line

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

def balise_cleaner(sentence):
    regexp_balise = r"<(c|t|b|\|a)*[^>]+>"
    return  re.sub(regexp_balise, r" ", sentence)

# Get all the targeted paths
def get_files(paths):
    with open(paths, 'r') as paths_list:
        files_list = [line.strip() for line in paths_list.readlines()]
        paths_list.close()
    return files_list

def content_builder(header_files, mail_files):
    header = []
    mail = []
    meta = []
    core = []
    
    # MAILS DATA
    for id_mail, path_mail in enumerate(mail_files):
        mail = {}
        with open(path_mail, 'r') as mail_file:
            mail[path_mail.split('/')[-1].replace(' ','')] = balise_cleaner(mail_file.read())
            print('MAIL: {}'.format(path_mail.split('/')[-1].replace(' ','')))
            mail_file.close()
    
    # HEADERS DATA
    for file_id, path_header in enumerate(header_files):
        with open(path_header, 'rb') as header_file:
            data_header = [line.strip().decode('utf-8','ignore') for line in header_file.readlines()]
            header_file.close()
        content = [' '.join(field.split(':')[1:]).replace('\u00e9', u'é') for field in data_header]

        if (len(content) == 7):
            header.append({'id_mail': path_header.split('/')[-1].replace(' ',''), 'sender' : content[0], 'timestamp': content[1],\
                    'receiver': content[4], 'distribution': content[5], 'title': content[6]})
        elif (len(content) == 6):
            header.append({'id_mail': path_header.split('/')[-1].replace(' ',''), 'sender' : content[1], 'timestamp': content[2],\
                    'receiver': content[3], 'distribution': content[4], 'title': content[5]})
        elif (len(content) == 5):
            header.append({'id_mail': path_header.split('/')[-1].replace(' ',''), 'sender' : content[0], 'timestamp': content[1],\
                    'receiver': content[2], 'distribution': content[3], 'title': content[4]})
        elif(len(content) == 4):
            header.append({'id_mail': path_header.split('/')[-1].replace(' ',''), 'sender' : content[0], 'timestamp': content[1],\
                    'receiver': content[2], 'distribution': 'unknown', 'title': content[3]})
        elif(len(content) == 3):
            header.append({'id_mail': path_header.split('/')[-1].replace(' ',''), 'sender' : 'unknown', 'timestamp': 'unknown',\
                    'receiver': content[0], 'distribution': content[1], 'title': content[2]})
        elif(len(content) == 2):
            header.append({'id_mail': path_header.split('/')[-1].replace(' ',''), 'sender' : content[0], 'timestamp': content[1],\
                    'receiver': 'unknown', 'distribution': 'unknown', 'title': 'unknown'})
        elif(len(content) == 1):
            header.append({'id_mail': path_header.split('/')[-1].replace(' ',''), 'sender' : content[0], 'timestamp': 'unknown',\
                    'receiver': 'unknown', 'distribution': 'unknown', 'title': 'unknown'})
        elif(len(content) == 0):
            header.append({'id_mail': path_header.split('/')[-1].replace(' ',''), 'sender' : 'unknown', 'timestamp': 'unknown',\
                    'receiver': 'unknown', 'distribution': 'unknown', 'title': 'unknown'})
        else:
            print(len(content))
            print(path_header)
            print('INFORMATION IS  MISSING')
        print('HEADER: {}'.format(path_header.split('/')[-1].replace(' ','')))
    for file_id in range(len(header)):
        # META DATA
        if header[file_id]['id_mail'] in mail:
            meta.append(json.JSONEncoder().encode({'index': {'_index': 'hydro', '_type': 'all', '_id': file_id}}))
            header[file_id]['content'] = mail[header[file_id]['id_mail']]
            print(header[file_id]['id_mail'])
            core.append(json.JSONEncoder().encode(header[file_id]))
    return (meta, core)

with open('global.json', 'w') as json_file:
    meta, core = content_builder(get_files(sys.argv[1]), get_files(sys.argv[2]))
    for doc in range(len(meta)):
        json_file.write(meta[doc])
        json_file.write('\n')
        json_file.write(core[doc])
        json_file.write('\n')
        print('{} \n'.format(doc))
    json_file.close()

