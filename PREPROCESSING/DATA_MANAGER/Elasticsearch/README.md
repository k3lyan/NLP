# ELASTICSEARCH
This module aims at evaluating the Elasticsearch (ES) efficiency inside my pipeline.
## Comparative study: 
Comparaison between my semi-supervised management skills classifier and indexing/querying through Elasticsearch.   
Is Elasticsearch able to return the expected document in the top 5 (out of 47 possibilities)?
## Risk Detection:
* Indexing e-mails exchanged during a project with customized mappings and analyzer 
* Querying these e-mails with risk sentences from the risk register of this project
## Requirements (06/18):
* Elastisearch 5.6.x: highest ES version supporting the most different OS.
* Logstash 5.6: same, plus supports all the debian systems
* Java compatibility: 
ES 5.6 <--> Oracle JVM 1.8u60+ | OpenJDK 1.8.0.111 | Azul Zing 16.01.9.0+
Logstash 5.6 <-->  Oracle JVM 1.8u60+ | OpenJDK 1.8.0.111 
* ELK compatibility:
ES 5.6 <--> Kibana 5.6 <--> Logstash 2.4 to 5.6

More information at: https://www.elastic.co/fr/support/matrix 
