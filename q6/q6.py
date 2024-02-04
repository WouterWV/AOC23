#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import os
os.chdir("/home/wouter/AOC/q6")

with open("input.txt", "r") as f:
    for i,line in enumerate(f):
        if i == 0:
            times = [int(el) for el in line.split()[1:]]
        else:
            dists = [int(el) for el in line.split()[1:]]

wins_races = []
for t,d in zip(times,dists):
    wins = 0
    for pt in range(1,t):  # don't care bout 0 or t press
        wins += 1 if pt*(t-pt) > d else 0
    wins_races.append(wins)
print("q1:", np.prod(wins_races))

# q2: quadratic function instead of looping...
t = int("".join([str(t) for t in times]))
d = int("".join([str(t) for t in dists]))

D = t**2 - 4*(-1)*(-d)
x1 = (-t + np.sqrt(D))/(-2)
x2 = (-t - np.sqrt(D))/(-2)

print("q2:", int(np.floor(x2) - np.ceil(x1) + 1))

