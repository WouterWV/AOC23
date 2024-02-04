#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import os
os.chdir("/home/wouter/AOC/q8")

dict = {}
with open("input.txt", "r") as f:
    for i,line in enumerate(f):
        if i == 0:
            LRs = line.strip()
        if i > 1:
            data = line.split()
            dict[data[0]] = {}
            dict[data[0]]["L"] = data[2][1:-1]
            dict[data[0]]["R"] = data[3][:-1]

def lcm(l):
    """least common multiple of a list of integeres"""
    lcm = l[0]
    for i in l[1:]:
        lcm = lcm*i//np.gcd(lcm, i)
    return lcm
    

pos = 'AAA'
id = 0 
while pos != 'ZZZ':
    idrun = id % len(LRs)
    pos = dict[pos][LRs[idrun]]
    id += 1
print('q1:', id)

poses = [el for el in dict.keys() if el[-1] == 'A']
initposes = poses.copy()
looped = np.array([False for el in poses])
loopcount = np.array([0 for el in poses])
print("init poses:", poses)
id = 0
while not looped.all():
    idrun = id % len(LRs)
    poses = [dict[el][LRs[idrun]] for el in poses]
    for i, el, initel in zip(range(len(poses)), poses, initposes):
        if el[-1] == 'Z':
            looped[i] = True
            loopcount[i] = id + 1
    id += 1

print("q2:",lcm(loopcount))

