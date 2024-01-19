### [spacey] TURN EXAMPLES PARAGRAPHS INTO LIST OF CHARACTERS ###
# Project: Trope
# Input: Paragraphs
# Output: List of characters

import spacy
from bs4 import BeautifulSoup
import codecs
import ast
import re
import requests
import pandas as pd


def get_characters(nlp, movie, text):
    doc = nlp(text)
    chars = []
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            chars.append(ent.text)
        if len(chars) >= 3:
            break
    return chars


def main(start, end):
    spacy.prefer_gpu()
    nlp = spacy.load("en_core_web_trf")
    print("spacy done loading")

    example_df = pd.read_csv("tropes_examples_v2_all.csv")
    print("old_data done loading")
    mdata = [] #list
    
    for index, row in example_df.iloc[start:end].iterrows():
        print("row: " + str(index) + ", " + row['text'])
        all_info = row[['text', 'href']].to_dict() #dict
        examples = ast.literal_eval(row['examples']) #list
        new_examples = [] #list
        count = 0
        for ex in examples: #dict
            count += 1
            characters = get_characters(nlp, ex['movie'], ex['text']) #list
            ex['characters'] = characters #dict
            new_examples.append(ex) #list
            print(" ex num: " + str(count) + "/" + str(len(examples)))
        
        new_info = {'examples' : new_examples} #dict
        if new_info['examples'] == []:
            print("[]")
        else:
            print(str(new_info['examples'][0]['characters']) + "..." + str(len(new_examples)))
        all_info.update(new_info) #dict
        mdata.append(all_info) #list
    
    df = pd.DataFrame(mdata)
    filename = "tropes_characters_v3_" + str(end) + ".csv"
    df.to_csv(filename, index=False)

main(0, 300)
