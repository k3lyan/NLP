import json
import re
import sys
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

#sys.argv[1]: mails_paths

def string_cleaner(sentence):
    return re.sub(r"[=.:><'•§œ;/)(!?@\\\'\`\"\_\n]", r"", sentence)

def balise_cleaner(sentence):
    regexp_balise = r"<(c|t|b|\|a)*[^>]+>"
    return  re.sub(regexp_balise, r" ", sentence)

# Get all the mails path
def get_mails(mails_paths):
    with open(mails_paths, 'r') as paths_list:
        mails_list = [line.strip() for line in paths_list.readlines()]
        print('NOMBRE DE MAILS: {}'.format(len(mails_list)))
        paths_list.close()
    return mails_list

# Build the body of the bilk query
def body_builder(mails_list):
    body_meta = []
    body_core = []
    for id_mail, path_mail in enumerate(mails_list):
        body_meta.append(json.JSONEncoder().encode({'index': {'_index': 'hydro_mail', '_type': 'mail', '_id': id_mail}}))
        with open(path_mail, 'r') as mail:
            body_core.append(json.JSONEncoder().encode({'id_mail': path_mail.split('/')[-1], 'content' : balise_cleaner(mail.read())}))  
            ## Rajouter un paramètre 'date' provenant des metadonnées et polarimo venant de l'étude de positivité !!!
            mail.close()
    return (body_meta, body_core)


# SAVE THE DATA AS A JSON FILE
with open('mails.json', 'w') as json_file:
    mails = body_builder(get_mails(sys.argv[1]))
    meta = mails[0]
    core = mails[1]
    for doc in range(len(meta)):
        json_file.write(meta[doc])
        json_file.write('\n')
        json_file.write(core[doc])
        json_file.write('\n')
    json_file.close()


'''
# INDEX
res = es.bulk(index="hydro_mail", doc_type='mail', body= body_builder(get_mails(sys.argv[1])))
print('RES: \n{}'.format(res))
'''
