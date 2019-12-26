#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 16:32:35 2019

@author: khan
"""

import pandas as pd
import re 
from scipy.spatial import distance

def removeSpecialChar(orignal):
    final = re.sub(r"[^a-zA-Z0-9.]+", '', orignal)
    return final

def strToval(a):
    w,m = a.split(",")
    w = removeSpecialChar(w); m = float(removeSpecialChar(m));
    return w,m

f = pd.ExcelFile("100topics.xlsx")
DTM = pd.read_excel(f, sheet_name = "DTM").values.tolist()
LDA = pd.read_excel(f, sheet_name = "LDA").values.tolist()
DTM_time = pd.read_excel(f, sheet_name = "DTMTime").values.tolist()
LDA_time = pd.read_excel(f, sheet_name = "LDATime").values.tolist()

JS_matrix = []
for i in range(100):
    words = []
    matrix = [] # Included if needed in future
    lda_matrix = []
    JS = []
    for x in range(50):
        w,m = strToval(LDA[i][x])
        words.append(w); matrix.append(m); lda_matrix.append(m);
    
    for x in range(100):  
        for j in range(17):
            dtm_matrix = [0 for k in range(50)]
            possible_words = words.copy()
            
            for y in range(50):
                w,m =strToval(DTM[j*100+x][y])
                
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
writer = pd.ExcelWriter("JS_convergence.xlsx")
df.to_excel(writer, 'JS')
writer.save()
