import pandas as pd
import numpy as np
import re
import sys
from StyleFrame import StyleFrame, Styler
from elasticsearch import Elasticsearch

es = Elasticsearch()

def skill_names_builder():
    res = es.search(index='ipma', doc_type='skill', body={
        "_source": ['name'],
        "size": 47,
        "query":{
            "match_all":{}
        },
        "sort":[
            {"_id": "asc"}    
        ]
    })
    skills_list = []
    for hit in res['hits']['hits']:
        skills_list.append((hit['_source']['name'])) 
    return(skills_list)


def top_10(skills_names):
    top10 = []
    for skill_nb, skill in enumerate(skills_names):
        top10.append({})
        top10[skill_nb]['name'] = skill
        top10[skill_nb]['top10_stats'] = []
        res= es.search(index='classifier', doc_type='sentences', body={
            "size" : 10,
            "query":{
                "bool":{
                    "must":[
                        {"match":{"skill": skill }}  
                    ],
                    "must_not":[
                        {"match":{"skill": "Aucune compétence"}}  
                    ]
                }
            },
            "sort":[
                {"proba_skill":"desc"}  
            ]
        })
        
        for rank, hit in enumerate(res['hits']['hits']):
            top10[skill_nb]['top10_stats'].append({})
            top10[skill_nb]['top10_stats'][rank]['sentence{}'.format(str(rank+1))] = hit['_source']['sentence']
            # For later
            top10[skill_nb]['top10_stats'][rank]['search_results'] = [] 
            top10[skill_nb]['top10_stats'][rank]['correctness'] = 'False'
            top10[skill_nb]['top10_stats'][rank]['accuracy'] = 0
        print('----------{}-----------'.format(skill))
        print(top10[skill_nb]['top10_stats'][0]['sentence1'])
        print(top10[skill_nb]['top10_stats'][1]['sentence2'])
    return top10

def skill_query(top10):
    top10_filled = top10
    correctness_count = 0
    for id_skill, skill in enumerate(top10_filled):
        skill_score = 0
        for rank, sentence_stats in enumerate(top10_filled[id_skill]['top10_stats']):
            sentence = sentence_stats['sentence{}'.format(str(rank+1))]
            res = es.search(index='ipma', doc_type='skill', body={
                "size" : 5,
                "_source": ['name'],
                "query":{
                    "match": {
                        "content": "{}".format(sentence)
                        }
                    }
                })
            for hit in res['hits']['hits']:
                if (hit['_source']['name'] == skill['name']):
                    sentence_stats["correctness"] = 'True'
                    correctness_count += 1
                    skill_score += 1
                sentence_stats['search_results'].append(hit['_source']['name'])
            sentence_stats['accuracy'] = skill_score/10*100
    print('-----------{}-----------'.format(skill['name']))
    accuracy = '{}%'.format(int(round(correctness_count/470*100)))
    return (top10_filled, accuracy)

search_results, accuracy = skill_query(top_10(skill_names_builder()))

def df_builder(search_results):
    columns = []
    index_names = []
    for id_skill, skill in enumerate(search_results):
        columns.append([])
        index_names.append(skill['name'])
        for rank, sentence_results in enumerate(search_results[id_skill]['top10_stats']):
            result = sentence_results["sentence{}".format(rank+1)]
            result += '\n#'
            result += '\n#'.join(sentence_results['search_results'])
            result += '\n Correctness: {}'.format(sentence_results['correctness'])
            columns[id_skill].append(result)
        columns[id_skill].append(sentence_results['accuracy'])
    df = pd.DataFrame(data = columns, index = index_names, columns = ['#1', '#2', '#3', '#4', '#5', '#6', '#7', '#8', '#9', '#10', 'Score (%)'])
    return df

df_search = df_builder(search_results)     

def excel_builder(df_search, accuracy):
    number_rows = len(df_search.index)
    writer = pd.ExcelWriter('{}{}.xlsx'.format(sys.argv[1], accuracy), engine='xlsxwriter')
    df_search.to_excel(writer, sheet_name='study1')
    workbook = writer.book
    worksheet = writer.sheets['study1']
    # Define the ranges for the colors formatting
    cols = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']
    color_ranges = []
    for col in cols:
        color_ranges.append("{}2:{}{}".format(col, col, number_rows+1))
    # Add a format. Green fill with dark green text.
    green_format = workbook.add_format({'bg_color': '#C6EFCE', 'font_color': '#006100'})
    # Add a format. Light red fill with dark red text.
    red_format = workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'})
    for ranges in color_ranges:
        worksheet.conditional_format(ranges, {'type':  'text', 'criteria': 'ends with', 'value': 'True', 'format': green_format})
        worksheet.conditional_format(ranges, {'type':  'text', 'criteria': 'ends with', 'value': 'False', 'format': red_format})
    writer.save()

excel_builder(df_search, accuracy)
