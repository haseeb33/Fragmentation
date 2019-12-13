#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 17:57:13 2019

@author: khan
"""

from gensim.models.wrappers import DtmModel
from gensim import corpora
import csv
import time
from nltk.corpus import stopwords
import re
import sys
from collections import defaultdict
import pandas as pd

start_time = time.time()

csv.field_size_limit(sys.maxsize)

cachedStopWords = stopwords.words("english")

def removeURLs(text):
    return re.sub(r'http\S+', '', text)

def removeStopWords(messy_text):
    messy_text = messy_text.lower()
    refined_text = ' '.join([word for word in messy_text.split() if word not in cachedStopWords])
    return refined_text

def removeSpecialChar(orignal):
    final = [re.sub(r"[^a-zA-Z0-9]+", ' ', k) for k in orignal.split("\n")]
    return final

def remove2Char(text):
    new_text = ""
    for w in (" ".join(text)).split():
        if len(w) >= 3:
             new_text=new_text + w + " "
    return new_text

def id2TokenFn():
    dic = corpora.Dictionary.load('dict.pickle')
    return {Id: token for token, Id in dic.token2id.items()}

years = []
contents = []
with open("nips-papers/papers.csv") as f:
    csv_reader = csv.reader((x.replace('\0', '') for x in f), delimiter = ',')
    for row in csv_reader:
        txt = remove2Char(removeSpecialChar(removeStopWords(removeURLs(row[6]))))
        if len(txt) > 500:
            contents.append(txt)
            years.append(row[1])

sorted_years = sorted(enumerate(years), key=lambda x:x[1])

ts = [] ;documents = []; prev = '1987' ; doc_count = 0 ; count = 0
for pos in range(len(sorted_years)):
    dat = sorted_years[pos][1]
    if dat == prev:
        doc_count+= 1
    else:
        ts.append(doc_count)
        doc_count = 1
        prev = dat
    count += 1
    documents.append(contents[sorted_years[pos][0]])
    if count == len(sorted_years):
        if doc_count > 1:
            ts.append(doc_count)
            doc_count = 0

#Formatting into list for tokenize
texts = [[word for word in document.lower().split()] for document in documents]

# Tokenization using collection library
frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1

texts = [[token for token in text] for text in texts]

dictionary = corpora.Dictionary(texts)
dictionary.save('dict.pickle')  # store the dictionary, for future reference

#Corpus Created
corpus = [dictionary.doc2bow(text) for text in texts]
print("Corpus Created")

num_topics = 30
path_to_dtm_binary = "/home/khan/DTM/dtm/dtm/main"
model = DtmModel(path_to_dtm_binary,
corpus=corpus, time_slices=ts,
mode='fit', model='dtm', num_topics=num_topics)

training_time = time.time() - start_time

print("Model fitted")
id2token = id2TokenFn()
topics = []
for t in range(len(ts)):
    for j in range(num_topics):
        topic = model.show_topic(topicid = j, time = t, topn = 50)
        new_topic = []
        info = ("Time,", t, "TopicID,", j)
        for item in topic:
            new_topic.append((id2token[int(item[1])], round(item[0], 4)))
        new_topic.append(info)
        topics.append(new_topic)

# Coverting topic into a excel file
print("Putting in DataFrame started")
df = pd.DataFrame(topics)
writer = pd.ExcelWriter("nips30topics_DTM.xlsx")
df.to_excel(writer, 'Topics')

df1 = pd.DataFrame([[training_time, "Seconds"]])
df1.to_excel(writer, 'TrainingTime')
writer.save()
