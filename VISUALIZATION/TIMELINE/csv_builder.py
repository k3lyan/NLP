import pandas as pd
import sys

#1st argument: excel file
#2nd argument: list of keywords to visualize
#3rd argument: name of the csv_file

#for i in range(5):
#    df = df.append({'A': i}, ignore_index=True)

def xlsx_to_csv(excel_path, words):
    # GET THE K-CORE DATA
    xls = pd.ExcelFile(excel_path)
    df = pd.read_excel(xls, 'Inf_top300')
    df = df[['Word', 'Year', 'Value']]
    # GET THE LIST OF TARGETED WORDS
    with open(words, 'r') as keywords:
        word_list = [line.strip() for line in keywords.readlines()]
        keywords.close()
    # KEEP ONLY THE DATA FOR THESE WORDS
    df_filtered = df.loc[df['Word'].isin(word_list)]
    df_filtered = df_filtered.sort_values(by='Word')
    df_filtered.loc[:,'Year'] -= 2011 
    # FILL THE YEAR WITHOUT VALUE WITH THE SCORE 0
    data = {}
    words = []    
    for word in df_filtered['Word']:
        words.append(word)
    unique_word = set(words)
    for w, word in enumerate(unique_word):
        data[word] = [0,0,0,0,0,0,0,0]

    for word, year, val in df_filtered.values:
        data[word][year] = val
    #print(data)
    # BUILD THE FINAL DF
    final_words = []
    years = []
    scores = []
    for w, word in enumerate(unique_word):
        for i in range(2011,2019):
            final_words.append(word)
            years.append(i)
            scores.append(data[word][i-2011])

    df_final = pd.DataFrame({'Word': final_words, 'Year': years, 'Value': scores})
    df_final = df_final[['Word', 'Year', 'Value']]
    print(df_final)
    df_final.to_csv(sys.argv[3], sep=',', index=False)

xlsx_to_csv(sys.argv[1], sys.argv[2])
