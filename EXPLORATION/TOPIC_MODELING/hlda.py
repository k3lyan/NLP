from graphviz import Digraph
import os
from preprocessing import utils
import string
from topic import topic
from collections import defaultdict
import sys

def hlda(corpus_folder):
    docs = []
    file_name_list = []
    remove_tokens = utils.load_stop_words()+['projet','management','s']
    for file_name in os.listdir(corpus_folder):
        file_name_list.append(file_name.replace('.txt',''))
        doc = utils.one_line_doc(os.path.join(corpus_folder, file_name)).lower()
        tokens = utils.remove_accents(
                utils.remove_symbols(utils.remove_num(
                    utils.normalize_quotes(doc)))).split()
        docs.append([w for w in tokens if w not in remove_tokens])
    #hlda_model = topic.do_hlda(docs, 3)
    hlda_model = topic.do_hlda(docs, 3)
    dot = Digraph(comment='hlda')
    topic_doc = defaultdict(list)
    added = []
    htree = defaultdict(list)
    for i in range(len(file_name_list)):
        node = hlda_model.document_leaves[i]
        words = node.get_top_words(10, False)[:-2].replace(","," ")
        parent = 'root'
        htree[node].append(file_name_list[i])
        dot.node('doc'+str(i), file_name_list[i])
        dot.node(str(node.node_id), words)
        dot.edge(str(node.node_id), 'doc'+str(i))
        print("['",file_name_list[i],"','",words.encode('utf-8'),"','']")
        prev_id = node.node_id
        node = node.parent
        while node:
            if node.parent:
                parent = node.parent
            else:
                parent = 'root'
            print("['",words,"','",end=' ')
            words = node.get_top_words(10, False)[:-2].replace(","," ")
            print(words,"', '']")
            if node not in htree[parent]:
                    htree[parent].append(node)
            if (node.node_id, prev_id) in added:
                break
            added.append((node.node_id, prev_id))
            dot.node(str(node.node_id), words)
            dot.edge(str(node.node_id), str(prev_id))
            prev_id = node.node_id
            node = node.parent
    dot.render('hlda.gv', view=False)

# Type the path where is located the Corpus !!
hlda('../../PREPROCESSING/DATA_STATS/Corpus')
