import re
import string
import sys
import os
import wikipediaapi

# Function to delete automatically printed \n
def string_cleaner(article):
    return re.sub(r"[\n]", r"", article).lower()

# Function to get the article from wikipedia whose titles are written in an input list
def wikipedia_docs(list_titles_file, language, destination_root):
    langue = wikipediaapi.Wikipedia("'"+language+"'")
    print('-------------LISTE DES TITRES-------------')
    with open(list_titles_file, 'r') as articles_list:
        articles = [line.strip() for line in articles_list.readlines()]
        articles_list.close()

    for i, article in enumerate(articles):
        # Check if the related article exists
        if(langue.page(article).exists()):
            print('TITRE {}: {}'.format(i, article))
            if not os.path.exists(destination_root):
                os.makedirs(destination_root)
            # CREATE THE NEW ARBORESCENCE
            with open('{}/{}.txt'.format(destination_root, str(article)), "w") as text_article:
                text_article.write(string_cleaner(langue.page(article).text))
                text_article.close()
        else:
            print('ARTICLE {}: {} MISSING'.format(i, article))

wikipedia_docs(sys.argv[1], sys.argv[2], sys.argv[3])
