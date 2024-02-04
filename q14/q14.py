#!/usr/bin/env python
# coding: utf-8

# In[134]:


import numpy as np
import os 
os.chdir("/home/wouter/AOC/q14")
M = []
with open("input.txt", 'r') as f:
    for line in f:
        rowline = line.strip()
        row = [el for el in line.strip()]
        M.append(row)
M = np.array(M)

def tilt(M, direction='north'):
    if direction == 'north':
        M = np.rot90(M)
    if direction == 'west':
        M = M
    if direction == 'south':
        M = np.rot90(M, 3)
    if direction == 'east':
        M = np.rot90(M,2)
    newM = []
    for col in M:
        col = ''.join(col)
        segs = col.split('#')
        #print("segs: ", segs)
        newseg = ''
        for seg in segs:
            no = seg.count('O')
            nd = seg.count('.')
            if no + nd > 0:
                newseg += 'O' * no + '.' * nd
            newseg += '#'
        newM.append(newseg[:-1])
    newM = np.array([list(row) for row in newM])
    if direction == 'north': 
        newM = np.rot90(newM, -1)
    if direction == 'west':
        newM = newM
    if direction == 'south':
        newM = np.rot90(newM, -3)
    if direction == 'east':
        newM = np.rot90(newM,-2)
    return newM

def cycle(M):
    for direction in ['north', 'west', 'south', 'east']:
        M = tilt(M, direction)
    return M

Mcopy = M.copy()
Mcopy = tilt(Mcopy)
count1 = 0
for i,row in enumerate(Mcopy):
    row = ''.join(row)
    no = row.count('O')
    count1+=no*(len(Mcopy)-i)
print("q1:", count1)

Mlist = [M]
i=0
Mnew = M.copy()
found = False
while not found:
    i+=1
    Mnew = cycle(Mnew)
    for j,Mt in enumerate(Mlist):
        if np.array_equal(Mt, Mnew):
            found = True
            print("found: ", j, i)
            cycle = i-j
            first = j
            last = i
            print("first, last, cycle: ", first, last, cycle)
            break

    Mlist.append(Mnew.copy())

idx = first + (1000000000 - first) % cycle 
print(idx)
count = 0
#newM = tilt(M)
Mke = Mlist[idx]
for i,row in enumerate(Mke):
    row = ''.join(row)
    no = row.count('O')
    count+=no*(len(Mke)-i)
print("q2:", count)

