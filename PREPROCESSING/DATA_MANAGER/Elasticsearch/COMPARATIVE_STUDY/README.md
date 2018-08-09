# Comparative study
## Goal:
Look at Elasticsearch performances in terms of "classifier" (through its internal ranking).
### The original classifier:
Its goal was to classify sentences from project manager reports (172 reports), among 47 management skills described by a textual reference, the IPMA.
IPMA and reports have been embedded as vectors and cosine similarity was applied between them, giving for each sentence of each report a 'management skill label', if the score was over an arbitrary threshold (if not the label was 'no skill represented').
### Elasticsearch Indexing
For the study one type of documenty had to be indexed: IPMA documents, 1 doc by described skill.
For personnal tests 3 types of documents were indexed:
* IPMA documents: 1 doc by described skill
* the project manager reports: here 2 options one sentence of a report per doc or one report per doc
* the classified sentences with their label
### Elasticsearch querying
Query on the IPMA index with the top 10 labelised sentences form the classifier (classified with the highest score by the classifier) for each skill. Which leads to 470 sentences in total.           
 
If the IPMA document describing the labelized skill for the sentence appears in the top 5 out of the 47 documents from IPMA index, the Elasticsearch answer is considered as successfull.
