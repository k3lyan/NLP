from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LTTextBox, LTChar, LTTextLine
from wrapper_pdf import PdfMinerWrapper
import sys
import os
import re


def extract_pdf():

    regexp_cleant_sentences = r"[\n]"

    with PdfMinerWrapper(sys.argv[1]) as doc:
        # LOADING THE NUMBER OF PAGES
        nb_pages = 0
        print('Loading the number of pages...\n')
        for p, page in enumerate(doc):
            print('-PAGE no.{}-'.format(page.pageid))
            nb_pages += 1

        # EXTRACTION QUESTIONS SCALE
        print('\nThis PDF file has {} pages.\n'.format(nb_pages))
        print('What do you want to extract from the pdf file ?\n')
        print('1.All the pages')
        print('2.A sequence of pages')
        print('3.A sequence of sentences')
        print('4.A sequence of words')
        print('5.The font and size of a specific word\n')
        extraction_type = input('Please enter the number corresponding to your request: ')
        print('\n')

        # PAGES LEVEL
        if (extraction_type == '1' or extraction_type == '2'):
            sentences = ""
            if (extraction_type == '1'):
                try:
                    for p, page in enumerate(doc):
                        print('---PAGE no.{} of pdf {}---'.format(page.pageid,sys.argv[1]))
                        for tbox in page:
                            if not isinstance(tbox, LTTextBox):
                                continue
                                # Loop on the sentences
                            for obj in tbox:
                                sentences += re.sub(regexp_cleant_sentences, r" ", obj.get_text())
                    return sentences
                except:
                    print('ERROR WHILE EXTRACTING !')
            elif (extraction_type == '2'):
                # DECLARE THE RANGE OF PAGES
                try:
                    first_page = int(input('Enter the first page you would like to extract: '))
                    last_page = int(input('Enter the last page you would like to extract: '))
                    print('First page extracted: {}'.format(first_page))
                    print('Last page extracted: {}'.format(last_page))
                    for p, page in enumerate(doc):
                        if (p> first_page-2 and p < last_page):
                            print('---PAGE no.{} of pdf {}---'.format(page.pageid,sys.argv[1]))
                            for tbox in page:
                                if not isinstance(tbox, LTTextBox):
                                    continue
                                for obj in tbox:
                                    sentences += re.sub(regexp_cleant_sentences, r" ", obj.get_text())
                    return sentences
                except:
                    print('INVALID RANGE OF PAGES ! You should have select a right range of numbers !')
        # SENTENCES AND WORDS LEVEL
        elif ((extraction_type == '3') or (extraction_type == '4') or (extraction_type == '5')):
            sentences = []
            targeted_page = int(input('What is the number of the targeted page?: '))
            print('Targeted page: {}'.format(targeted_page))
            print('Loading the sentences...')
            for p, page in enumerate(doc):
                try:
                    if (p == (int(targeted_page)-1)):
                        for tbox in page:
                            if not isinstance(tbox, LTTextBox):
                                continue
                            for obj in tbox:
                                for i, c in enumerate(obj):
                                    if not isinstance(c, LTChar):
                                        continue
                                    if(i == 0):
                                        sentences.append({'sentence':obj.get_text(), 'font':c.fontname, 'size':c.size})
                except:
                    print('INVALID TARGETED PAGE!')
            for s, sentence in enumerate(sentences):
                print('{}: {}'.format(s+1, sentence['sentence']))
            print('\nThis page has {} sentences\n'.format(len(sentences)))
            # SENTENCES LEVEL
            if (extraction_type == '3'):
                try:
                    first_sentence = int(input('Number of the first sentence you would like to extract: '))
                    last_sentence = int(input('Number of the last sentence you would like to extract: '))
                    sentences_string = ""
                    for i in range(first_sentence-1, last_sentence):
                        sentences_string += " " + sentences[i]['sentence']
                    return sentences_string
                except:
                    print('SENTENCES RANGE INVALID !')
            # WORDS LEVEL
            elif ((extraction_type == '4') or (extraction_type == '5')):
                try:
                    sentence = int(input('Choose a sentence (by its number): '))
                    words_sentence = sentences[sentence-1]['sentence'].split(" ")
                    print('This sentence has {} words'.format(len(words_sentence)))
                    for w, word in enumerate(words_sentence):
                        print('{}: {}'.format(w+1, word))
                except:
                    print('INVALID NUMBER OF SENTENCE !')
                # RANGE OF WORDS
                if (extraction_type == '4') :
                    try:
                        first_word = int(input('Position of the first word you would like to extract in this sentence: '))
                        last_word = int(input('Position of the last word you would like to extract in this sentence: '))
                        return (str(" \n".join(words_sentence[first_word-1:last_word])) + '\n')
                    except:
                        print('WORDS RANGE INVALID !')
                # WORD FEATURE
                elif (extraction_type == '5'):
                    word_position = int(input('Position of the number you would like to know the features: '))
                    print(str("\nWord: {} \nFont name: {} \nFont size: {}\n".format(\
                                                        words_sentence[word_position-1],\
                                                        sentences[sentence-1]['font'],\
                                                        sentences[sentence-1]['size'])))
                    return str("Word: {} \nFont name: {} \nFont size: {}\n".format(\
                                                        words_sentence[word_position-1][word_position-1],\
                                                        sentences[sentence-1]['font'],\
                                                        sentences[sentence-1]['size']))
        else:
            print('INVALID NUMBER ! You should have select a number from 1 to 5 ! \n')

# BUILDING PDF FILES
titre_rapport = sys.argv[1].replace(" ", "_")
repertoire = titre_rapport.replace(".pdf", "")
titre_rapport = titre_rapport.replace(".pdf", ".txt")
os.system('mkdir {}'.format(repertoire))
file = open('./{}/{}'.format(repertoire, titre_rapport), "w")
file.write(extract_pdf())
file.close()
