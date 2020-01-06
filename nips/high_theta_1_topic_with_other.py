#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 21:43:22 2019

@author: khan
"""

import pandas as pd
import matplotlib.pyplot as plt
import re

TIME_SLICES = 30 # Max time slice number
T = [i for i in range(31)] # Total time slices
dtm_gl = 0 # global value: changed with graph() function
year_col = 60 # year's column in sheet name "Theta"
d_years = {} # count of docs in each year, filled with function Init_d_years() call

def removeSpecialChar(orignal): 
    return re.sub(r"[^a-zA-Z0-9.]+", '', orignal)
def strToval(a):
    w,m = a.split(",")
    return removeSpecialChar(w)
def J(var): # use in graph()
    return JS[var][dtm_gl*31:(dtm_gl+1)*31]
def DTMWithAllLDA(a): # use in DTMcount(), can also be called indiviually 
    return [i[1] for i in LDA_related_DTM if i[0] == a] 
  
def populationGraph(t): # graph of estimated number of docs for topic t of LDA
    d = {}
    for p in Theta_ls:
        if p[year_col] not in d.keys():
            d[p[year_col]] = p[t]
            d_years[p[year_col]] = 1
        else:
            d[p[year_col]] += p[t]
            d_years[p[year_col]] += 1
            
    sorted_d_keys = sorted(d.keys())
    plt.plot([d[i]/d_years[i] for i in sorted_d_keys])

def Init_d_years():
    for p in Theta_ls:
        if p[year_col] not in d_years.keys():
            d_years[p[year_col]] = 1

def timeCorr(t1,t2):
    corr_time = []
    Init_d_years() if not(d_years) else None
    
    for i in sorted(d_years.keys()):
        a = Theta_df[Theta_df[60]==i]
        corr_time.append(a[t1].corr(a[t2]))
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_ylim(-0.75,0.75)
    ax.plot(corr_time)

#def highTheta(t1, t2):
    

def graph(dtm, x, a=None, b=None, c=None, d=None, e=None, f=None, g=None, h=None, i=None, j=None):
    global dtm_gl
    dtm_gl = dtm
    if j: 
        plt.plot(T,J(x), T,J(a), T,J(b), T,J(c), T,J(d), T,J(e), T,J(f), T,J(g), T,J(h), T,J(i), T,J(j))
    elif i:
        plt.plot(T,J(x), T,J(a), T,J(b), T,J(c), T,J(d), T,J(e), T,J(f), T,J(g), T,J(h), T,J(i))
    elif h:
        plt.plot(T,J(x), T,J(a), T,J(b), T,J(c), T,J(d), T,J(e), T,J(f), T,J(g), T,J(h))
    elif g:
        plt.plot(T,J(x), T,J(a), T,J(b), T,J(c), T,J(d), T,J(e), T,J(f), T,J(g))
    elif f:
        plt.plot(T,J(x), T,J(a), T,J(b), T,J(c), T,J(d), T,J(e), T,J(f))
    elif e:
        plt.plot(T,J(x), T,J(a), T,J(b), T,J(c), T,J(d), T,J(e))
    elif d:
        plt.plot(T,J(x), T,J(a), T,J(b), T,J(c), T,J(d))
    elif c:
        plt.plot(T,J(x), T,J(a), T,J(b), T,J(c))
    elif b:
        plt.plot(T,J(x), T,J(a), T,J(b))
    elif a:
        plt.plot(T,J(x), T,J(a))
    else:
        plt.plot(T,J(x))

def getAllDTMwords(topic):
    words = []
    for i in range(31):
        for j in range(50):
            w = strToval(DTM[i*TIME_SLICES+topic][j])
            if w not in words:
                words.append(w)
    return words

def DTMcount():
    DTM_count_dict = {}
    
    for i in LDA_related_DTM:
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

f = pd.ExcelFile("60topics.xlsx")
DTM = pd.read_excel(f, sheet_name = "DTM", index_col=0).values.tolist()
LDA = pd.read_excel(f, sheet_name = "LDA", index_col=0).values.tolist()
DTM_time = pd.read_excel(f, sheet_name = "DTMTime").values.tolist()
LDA_time = pd.read_excel(f, sheet_name = "LDATime").values.tolist()
JS = pd.read_excel(f, sheet_name = "JS", index_col=0).values.tolist()
Theta_df = pd.read_excel(f, sheet_name = "Theta", index_col=0)
Theta_ls = Theta_df.values.tolist()

LDA_related_DTM = []

for i_index, i in enumerate(JS):
    for j_index, j in enumerate(i):
        if j<=0.7:
            a = [j_index//31, i_index]
            if a not in LDA_related_DTM:
                LDA_related_DTM.append(a)
LDA_related_DTM = sorted(LDA_related_DTM)
Init_d_years()                
DTM_all, DTM_2orMore = DTMcount()
