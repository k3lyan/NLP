# MINI-TUTO ES PYTHON API
## Filter thhe answer
* The filter_path parameter is used to reduce the response returned by elasticsearch. For example, to only return _id and _type, do:
	
	`es.search(index='test-index', filter_path=['hits.hits._id', 'hits.hits._type'])`

* It also supports the * wildcard character to match any field or part of a field’s name:
	
	`es.search(index='test-index', filter_path=['hits.hits._*'])`

