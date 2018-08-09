import sys
import re
import os
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

def path_generator(initial_root):
    for root, dirs, files in os.walk(path_sources):
        paths = [os.path.join(root, name) for name in files]
    return paths

def string_cleaner(sentence):
    return re.sub(r"[=.:><'•§œ;/)(!?@\\\'\`\"\_\n]", r"", sentence)

# Build the body of the bilk query
def body_builder(reports_list):
    body = ''
    for id_report, path_report in enumerate(reports_list):
        body += '{'+'\"'+ 'index' + '\"' + ': {'+ \
                    '\"' + '_index' + '\"' + ':' + '\"' + 'reports'  + '\"' + ',' + \
                    '\"' + '_type' + '\"' + ':' +  '\"' + 'report'  + '\"' + ',' + \
                    '\"' + '_id' + '\"' + ':' + '\"' + '{}'.format(int(id_report)) + '\"' + '}' + '}'
        body += '\n'
        with open(path_report, 'r') as report:
            # SKILL CONTENT IS TOKENIZED ONE LINE BY SENTENCE
            # NOT GOOD FOR JSON
            data = report.readlines()
            for i, line in enumerate(data):
                data[i] = string_cleaner(line.rstrip())
            content = ' '.join(data)
            body += '{'+ '\"' + 'name' + '\"' + ':' + '\"' + '{}'.format(path_report.split('/')[-1].replace('_', ' ')) + '\",'  \
                       + '\"' + 'content' + '\"' + ':' + '\"' + '{}'.format(content) + '\"' + '}'  
            body += '\n'
            report.close()
    return body

# INDEX
res = es.bulk(index="ipma", doc_type='report', body= body_builder(get_reports(sys.argv[1])))
print('RES: \n{}'.format(res))

