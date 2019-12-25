#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 18:37:52 2019

@author: khan
"""

from gensim import corpora
import csv
from nltk.corpus import stopwords
import re
import sys
import time
from collections import defaultdict

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
def id2TokenFn():
    dic = corpora.Dictionary.load('dict.pickle')
    return {Id: token for token, Id in dic.token2id.items()}
    

             
documents = []
max_doc_size = 408200
count = 0
ts = []
ts_ls = []
prev = "1_23_2011"
tweet_count = 0
with open('ordered_day_hashtag_fragmentation.txt', mode = 'r') as f:
    csv_reader = csv.reader((x.replace('\0', '') for x in f), delimiter = ',')
    for row in csv_reader:
        documents.append(remove2Char(removeSpecialChar(removeStopWords(removeURLs(row[2])))))
        tag = row[0].split("_")
        dat = tag[0] + "_" + tag[1] + "_" + tag[2]
        if dat == prev:
            tweet_count += 1
        else:
            ts.append(tweet_count)
            ts_ls.append(prev)
            tweet_count = 1
            prev = dat
        
        count += 1
        if count == max_doc_size:
            if tweet_count >= 1:
                ts.append(tweet_count)
                ts_ls.append(prev)
                tweet_count = 0
            break

# Formatting into list for tokenize
texts = [[word for word in document.lower().split()]
         for document in documents]

 
# remove words that appear only once
frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1

texts = [[token for token in text if frequency[token] > 0] for text in texts]

dictionary = corpora.Dictionary(texts)
dictionary.save('dict.pickle')  # store the dictionary, for future reference

#Corpus Created
corpus = [dictionary.doc2bow(text) for text in texts]

print("Corpus Created")
id2token = id2TokenFn()