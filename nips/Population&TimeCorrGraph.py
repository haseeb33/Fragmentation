#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 23:34:41 2019

@author: khan
"""
import pandas as pd
import matplotlib.pyplot as plt


year_col = 60
d_years = {}

#Run Atleast once before using timeCorr Fn
def populationGraph(t):
    d = {}
    for p in LDA_theta_ls:
        if p[year_col] not in d.keys():
            d[p[year_col]] = p[t]
            d_years[p[year_col]] = 1
        else:
            d[p[year_col]] += p[t]
            d_years[p[year_col]] += 1
            
    sorted_d_keys = sorted(d.keys())
    plt.plot([d[i]/d_years[i] for i in sorted_d_keys])

def timeCorr(t1,t2):
    corr_time = []
    for i in sorted(d_years.keys()):
        a = LDA_theta_df[LDA_theta_df[60]==i]
        corr_time.append(a[t1].corr(a[t2]))
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_ylim(-0.75,0.75)
    ax.plot(corr_time)

f = pd.ExcelFile("theta/Theta_values_60topics_LDA.xlsx")
#f1 = pd.ExcelFile('nips30topics.xlsx')

LDA_theta_df = pd.read_excel(f, sheet_name = "ThetaValues", index_col=0)
LDA_theta_ls = LDA_theta_df.values.tolist()
#DTM = pd.read_excel(f1, sheet_name = "DTM", index_col=0).values.tolist()

