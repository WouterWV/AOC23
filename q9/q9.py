#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import os
os.chdir("/home/wouter/AOC/q9")

seqs = []
with open("input.txt", "r") as f:
    for line in f:
        # split first, then cast each el to int
        seqs.append(list(map(int, line.split())))

def pred(seq):
    nseq = seq.copy()
    diffs = []
    while len(nseq) > 1:
        diffs.append(np.diff(nseq))
        nseq = np.diff(nseq)

    predict = sum([el[-1] for el in diffs[0:]]) + seq[-1]
    hists = [0]
    for first in [el[0] for el in diffs[::-1]]:
        hists.append(first - hists[-1])
    history = seq[0] - hists[-1]
    return predict, history
sols = (np.sum(np.array([pred(seq) for seq in seqs]), axis=0)).tolist()
print("q1:", (sols[0]))
print("q2:", (sols[1]))


# In[ ]:




