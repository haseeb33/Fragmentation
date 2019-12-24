#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 15:50:27 2019

@author: khan
"""


import sys
sys.path.insert(1, '/Users/khan/Documents/Thesis/Code/topicModels-java')
import pytm
import csv
import numpy as np
from nltk.corpus import stopwords
import re
import sys
import pandas as pd
import time


start_time = time.time()

csv.field_size_limit(sys.maxsize)

cachedStopWords = stopwords.words("english")

def removeURLs(tweet):
    return re.sub(r'http\S+', '', tweet)

def removeStopWords(messy_tweet):
    messy_tweet = messy_tweet.lower()
    refined_tweet = ' '.join([word for word in messy_tweet.split() if word not in cachedStopWords])
    return refined_tweet

def removeSpecialChar(orignal):
    final = [re.sub(r"[^a-zA-Z0-9]+", ' ', k) for k in orignal.split("\n")]
    return final
          
def remove2Char(tweet):
    new_tweet = ""
    for w in (" ".join(tweet)).split():
        if len(w) >= 3:
             new_tweet=new_tweet + w + " "
    return new_tweet
             
documents = []

with open('ordered_day_hashtag_fragmentation.txt', mode = 'r') as f:
    csv_reader = csv.reader((x.replace('\0', '') for x in f), delimiter = ',')
    for row in csv_reader:
        documents.append(remove2Char(removeSpecialChar(removeStopWords(removeURLs(row[2])))))



docs = pytm.DocumentSet(documents, min_df=5, max_df=0.5)

#Applying LDA on our dataset
n_topics = 30
lda = pytm.SVILDA(n_topics, docs.get_n_vocab())
lda.fit(docs, n_iteration=1000, B=1000, n_inner_iteration=5, n_hyper_iteration=20, J=5)

#Getting topic's and alpha values
topic_list = []
alphas = [lda.get_alpha(k) for k in range(n_topics)]
for k, alpha in enumerate(alphas):
    vocab = docs.get_vocab()
    phi = lda.get_phi(k)
    new_phi = np.around(list(phi), decimals = 3)
    print('topic {0} (alpha = {1})'.format(k, np.around(alpha, decimals = 2)))
    a = sorted(zip(vocab, new_phi), key=lambda x: -x[1])[:50]
    topic_list.append(a)

print("Topics Done")
training_time = time.time() - start_time

# Coverting topic into a excel file
print("Putting topics in DataFrame started")
df = pd.DataFrame(topic_list)
writer = pd.ExcelWriter("nips30topics_LDA.xlsx")
df.to_excel(writer, 'LDA')

df1 = pd.DataFrame([[training_time, "Seconds"]])
df1.to_excel(writer, 'LDATime')
writer.save()
