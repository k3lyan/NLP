# NESTED OBJECTS STRUCTURE 
## 1) CREATE THE INDEX WITH KIBANA
Use case: classified sentences from client reports     
if the index 'classifier' was already existing be sure to delete it before creating a new one:    
`DELETE classifier`     
### Settings: 
Here you create the analyzer (see the all list of analyzers in the analyzer_list.txt file)   
### Mappings: 
Each document will contains sub-object, 1 per sentence. 
Customed analyzer mapped to the text of the sentence.

`PUT classifier
{
  "settings": {
    "analysis": {
      "filter": {
        "french_stop": {
          "type":       "stop",
          "stopwords":  "_french_"
        },
        "nfkc_normalizer": { 
          "type": "icu_normalizer",
          "name": "nfkc"
        },
        "french_keywords": {
          "type":       "keyword_marker",
          "keywords":   ["Exemple"] 
        },
        "asciifolding": {
          "type": "asciifolding"
        }
      },
      "analyzer": {
        "my_custom_analyzer": {
          "tokenizer": "whitespace",
          "filter": ["french_stop", "nfkc_normalizer"]
        }
      }
    }
  },
  "mappings": {
    "reports": {
      "properties": {
        "sentences": {
          "type": "nested",
          "properties": {
            "sentence": {"type": "text", "analyzer": "my_custom_analyzer"},
            "proba_skill": {"type" : "float"},
            "skill":  {"type": "text"}
          }
        }
      }
    }
  }
}`           

## 2) POPULATE
### Id by id:
From Kibana console, you can populate manually by adding the documents one by one (not really efficient)
`PUT sentences/reports/111
{
	"title": "111"
	"sentences": [
		{
		  "text":"Je commence ce rapport par blablabla.",
		  "skill":"Aucune compétence",
		  "proba":0.003125
		},
		{
		  "text" : "Puis vient la 2ème phrase de mon rapport, tel un leader."
		  "skill" : "Leadership",
		  "proba" : 0.001231
		},
		...
		{
		  "text" : "Ainsi nous arrivons à la fin de mon argumentaire."
		  "skill" : "Argumentation",
		  "proba" : 0.00211
		}
	]
}`

### _bulk API:
Add several documents at the same time
--> generate a json files matching your data: json_converter.py.
--> Type in a terminal (in the same directory containing your json file data.json):   
`$ curl -H "Content-Type:application/json" -XPOST "http://localhost:9200/thales/report_sentences/_bulk?pretty" --data-binary "@data.json"`

## 3) ANALYZERS
Install icu-analysis plugin:     
`$ sudo bin/elasticsearch-plugin install analysis-icu`

## 4) SEARCH & AGGREGATIONS
Full search example with aggregation, highlight, filter...
          
GET /_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "title": "smith"
          }
        }
      ],
      "must_not": [
        {
          "match_phrase": {
            "title": "granny smith"
          }
        }
      ],
      "filter": [
        {
          "exists": {
            "field": "title"
          }
        }
      ]
    }
  },
  "aggs": {
    "my_agg": {
      "terms": {
        "field": "user",
        "size": 10
      }
    }
  },
  "highlight": {
    "pre_tags": [
      "<em>"
    ],
    "post_tags": [
      "</em>"
    ],
    "fields": {
      "body": {
        "number_of_fragments": 1,
        "fragment_size": 20
      },
      "title": {}
    }
  },
  "size": 20,
  "from": 100,
  "_source": [
    "title",
    "id"
  ],
  "sort": [
    {
      "_id": {
        "order": "desc"
      }
    }
  ]
}

## 5) AGGREGATIONS
## 6) VISUALIZATIONS
## 7) MACHINE LEARNING


