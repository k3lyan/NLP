# LOGSTACH INDEXING
Here I try another alternative to index documents: by using logstach tool.   
To do so you have to configure a logstach.config file, specifying the input and output.  
Then after being sure that elasticsearch and kibana are running, run logstach as following:
`$ bin/logstach -f absolute_path_to_the_logstach_config_file/logstach.config`

## csv_generator.py:
### Input
Root directory containing all the IPMA documents (one document per skill).
### Output 
csv file: first column is the skill name, second one is the text describing the skill.
