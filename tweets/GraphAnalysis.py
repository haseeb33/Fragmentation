#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Updated on Sat Jan 18 16:04:22 2020

@author: khan
"""

import pandas as pd
import matplotlib.pyplot as plt
import re

file_name = "30topics.xlsx"
TOPICS = int(file_name[:2])
TIME_SLICES = 17
T = [i for i in range(TIME_SLICES)]
dtm_gl = 0

def removeSpecialChar(orignal):
    return re.sub(r"[^a-zA-Z0-9.]+", '', orignal)
def strToval(a):
    w,m = a.split(",")
    return removeSpecialChar(w)
def J(var):
    return JS[var][dtm_gl*TIME_SLICES:(dtm_gl+1)*TIME_SLICES]
def DTMWithAllLDA(a):
    return [i[1] for i in DTM_related_LDA if i[0] == a]

def graphJS(dtm, ls): #ls is list of LDA topics,
    global dtm_gl
    dtm_gl = dtm
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.ylabel("JSD value")
    plt.xlabel("Time slot")
    for i in ls:
        ax.plot(T, J(i), label="Topic %i" %i)
    ax.legend()
    plt.show()

def getAllDTMwords(topic):
    words = []
    for i in range(TIME_SLICES):
        for j in range(50):
            w = strToval(DTM[i*TOPICS+topic][j])
            if w not in words:
                words.append(w)
    return words

def DTMcount():
    DTM_count_dict = {}

    for i in DTM_related_LDA:
        if i[0] in DTM_count_dict.keys():
            DTM_count_dict[i[0]] += 1
        else:
            DTM_count_dict[i[0]] = 1
    DTM_2orMore = [[dtm, DTMWithAllLDA(dtm)] for dtm, v in DTM_count_dict.items() if v>1]
    return DTM_count_dict, DTM_2orMore

def getDTM(topic):
    print([strToval(DTM[topic][i]) for i in range(50)])
def getLDA(topic):
    print([strToval(LDA[topic][i]) for i in range(50)])

def comp(l1, l2):
    print("Words removed :----->")
    for i in l1:
        if i not in l2:
            print(i , end = ", ")
    print("\n" + "Words added :------>")
    for j in l2:
        if j not in l1:
            print(j, end = ", ")
def common(l1, l2):
    print("Common words in both: ---->")
    for i in l1:
        if i in l2:
            print(i, end = ", ")

f = pd.ExcelFile(file_name)
DTM = pd.read_excel(f, sheet_name = "DTM", index_col=0).values.tolist()
LDA = pd.read_excel(f, sheet_name = "LDA", index_col=0).values.tolist()
DTM_time = pd.read_excel(f, sheet_name = "DTMTime",).values.tolist()[0][1]
LDA_time = pd.read_excel(f, sheet_name = "LDATime").values.tolist()[0][1]
JS = pd.read_excel(f, sheet_name = "JS", index_col=0).values.tolist()

DTM_related_LDA = []

for i_index, i in enumerate(JS):
    for j_index, j in enumerate(i):
        if j<=0.7:
            a = [j_index//TIME_SLICES, i_index]
            if a not in DTM_related_LDA:
                DTM_related_LDA.append(a)
DTM_related_LDA = sorted(DTM_related_LDA)

DTM_all, DTM_2orMore = DTMcount()
