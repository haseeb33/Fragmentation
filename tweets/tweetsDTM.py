#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 15:42:00 2019

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
df.to_excel(writer, 'DTM')

df1 = pd.DataFrame([[training_time, "Seconds"]])
df1.to_excel(writer, 'DTMTime')
writer.save()
