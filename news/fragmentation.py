#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Updated on Sat Jan  18 13:06:35 2020

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
DTM_topics = 100
LDA_topics = 100
time_slices = 24

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
writer = pd.ExcelWriter("JS_convergence.xlsx")
df.to_excel(writer, 'JS')
writer.save()
