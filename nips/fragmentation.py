#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 16:32:35 2019

@author: khan
"""

import pandas as pd
import re 
from scipy.spatial import distance

# not good function for texts other than english
def removeSpecialChar(orignal):
    final = re.sub(r"[^a-zA-Z0-9.]+", '', orignal)
    return final

def strToval(a):
    w,m = a.split(",")
    w = removeSpecialChar(w); m = float(removeSpecialChar(m));
    return w,m

f = pd.ExcelFile("theta/Theta_values_60topics_LDA.xlsx")
f1 = pd.ExcelFile('old/nips60topics.xlsx')
DTM = pd.read_excel(f1, sheet_name = "DTM", index_col=0).values.tolist()
LDA = pd.read_excel(f, sheet_name = "LDA", index_col=0).values.tolist()
JS_matrix = []
DTM_topics = 60
LDA_topics = 60
time_slices = 31
for i in range(LDA_topics):
    words = []
    matrix = [] # Included if needed in future
    lda_matrix = []
    JS = []
    for x in range(50):
        w,m = strToval(LDA[i][x])
        words.append(w); matrix.append(m); lda_matrix.append(m);
    
    for x in range(DTM_topics):  
        for j in range(time_slices):
            dtm_matrix = [0 for k in range(50)]
            possible_words = words.copy()
            
            for y in range(50):
                w,m =strToval(DTM[j*DTM_topics+x][y])
                
                if w in words:
                    pos = words.index(w)
                    dtm_matrix[pos] = m
                else:
                    possible_words.append(w); dtm_matrix.append(m);
                
            lda_matrix1 = lda_matrix + [0 for k in range(50,len(dtm_matrix))]
            JS.append(distance.jensenshannon(lda_matrix1, dtm_matrix))
    JS_matrix.append(JS)

# Making new excel with JS_divergence values 
df = pd.DataFrame(JS_matrix)
writer = pd.ExcelWriter("JS_convergence60.xlsx")
df.to_excel(writer, 'JS')
writer.save()
