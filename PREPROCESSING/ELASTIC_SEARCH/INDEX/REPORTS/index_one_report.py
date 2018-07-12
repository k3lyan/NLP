import sys
from datetime import datetime
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

#sys.argv[1]: list of report paths
#sys.argv[2]: number of the targeted report in that list
#sys.argv[3]: id number in the index

# Get all the reports documentation
def get_reports(reports_list_paths):
    with open(reports_list_paths, 'r') as paths_list:
        reports_files = [line.strip() for line in paths_list.readlines()]
        paths_list.close()
    return reports_files

def doc_builder(report_name, report_number):
    with open(report_name[int(report_number)], 'r') as report:
        report_content = str(report.read())
        report.close()
    return {'report': str(report_name[int(report_number)].split('/')[-1].replace('_', ' ')), 'content': report_content}

res = es.index(index="report_test", doc_type='report', id=sys.argv[3], body=doc_builder(get_reports(sys.argv[1]), sys.argv[2]))

print(res['result'])

res = es.get(index="report_test", doc_type='report', id=sys.argv[3])

#print(res['_source'])

es.indices.refresh(index="report_test")

res = es.search(index="report_test", body={"query": {"match_all": {}}})

print("Got %d Hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
        print("%(report)s " % hit["_source"])
