# SETTINGS AND MAPPINGS
Here I give example on how to use were set the settings and mappings for the different index.
The customed analyzers varied during the tests of the study to find the more optimized one for my study.

## IPMA
PUT ipma        
'''json
{
  "settings":{
    "analysis": {
      "filter": {
        "french_stop":{
          "type": "stop",
          "stopwords": "_french_"
        },
        "shingle_filter":{
          "type": "shingle",
          "min_shingle_size": 2,
          "max_shingle_size": 5,
          "output_unigrams": false
        },
        "my_length_filter":{
          "type": "length",
          "max": 10,
          "min": 3
        }
      },
      "analyzer": {
        "stop_analyzer":{
          "tokenizer": "whitespace",
          "filter": ["my_length_filter", "french_stop", "asciifolding", "lowercase", "flatten_graph"]
        }
      }
    }
  },
  "mappings":{
    "skill":{
      "properties":{
        "name": {"type": "text"}, 
        "content": {"type": "text", "analyzer": "stop_analyzer"}
      }
    }
  }
}
'''
## Classifier
PUT classifier     
'''json
{
  "settings":{
    "analysis": {
      "filter": {
        "french_stop":{
          "type": "stop",
          "stopwords": "_french_"
        },
        "shingle_filter":{
          "type": "shingle",
          "min_shingle_size": 2,
          "max_shingle_size": 5,
          "output_unigrams": false
        },
        "my_length_filter":{
          "type": "length",
          "max": 10,
          "min": 3
        }
      },
      "analyzer": {
        "stop_analyzer":{
          "tokenizer": "whitespace",
          "filter": ["my_length_filter", "french_stop", "asciifolding", "lowercase", "flatten_graph"]
        }
      }
    }
  },
  "mappings":{
    "sentences":{
      "properties":{
        "report_id": {"type": "text"}, 
        "sentence": {"type": "text", "analyzer": "stop_analyzer"},
        "proba_skill": {"type": "float"},
        "skill": {"type": "text"}
      }
    }
  }
}
'''

## Nested Classifier
PUT classifier_nested      
'''json
{
  "settings":{
    "analysis": {
      "filter": {
        "french_stop":{
          "type": "stop",
          "stopwords": "_french_"
        }
      },
      "analyzer": {
        "stop_analyzer":{
          "tokenizer": "whitespace",
          "filter": ["french_stop"]
        }
      }
    }
  },
  "mappings":{
    "reports":{
      "properties":{
        "name": {"type": "text"}, 
        "sentences":{
          "type": "nested",
          "properties":{
            "sentence": {"type": "text", "analyzer": "stop_analyzer"},
            "proba_skill": {"type": "float"},
            "skill": {"type": "text"}
          }
        }
      }
    }
  }
}
'''
