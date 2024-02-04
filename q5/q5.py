#!/usr/bin/env python
# coding: utf-8

# In[15]:


import numpy as np 
import os 

def mapAtoB(Astarts, Bstarts, Ls, A):
    # [Astart, Astart + L] -> [Bstart, Bstart + L] for every Astart, Bstart, L
    # in the lists Astarts, Bstarts, Ls
    for Astart, Bstart, L in zip(Astarts, Bstarts, Ls):
        if Astart <= A < Astart + L:
            idx = A - Astart
            return Bstart + idx
    # if A is not in any of the ranges, return A
    return A

os.chdir("/home/wouter/AOC/q5")
lists = []
with open('input.txt', 'r') as f:
    listel = []
    for line in f:
        if line.startswith('seeds:'):
            seeds = [int(el) for el in (line.split()[1:])]
        elif 'map' in line:
            lists.append(listel)
            listel = []
        elif len(line.split()) > 1:
            listel.append([int(el) for el in line.split()])
    # don't forget the last map
    lists.append(listel)

# format mappers 
mappers = [np.array([el for el in lists[1:][i]]) for i in range(len(lists[1:]))]

soils = []
# loop the maps 
for seed in seeds:
    for mapper in mappers:
        seed = mapAtoB(mapper[:,1], mapper[:,0], mapper[:,2], seed)
    soils.append(seed)
print("Closest soil q1: ", min(soils))

# we have to sort the mappers along mappers[i][:,1] ... 
sorted_mappers = []
for mapper in mappers:
    sorted_mapper = np.array([[x,y,z]for y, x, z in sorted(zip(mapper[:,1], mapper[:,0], mapper[:,2]))])
    sorted_mappers.append(sorted_mapper)
mappers = sorted_mappers


def maprangeAtorangesB(startsA, startsB, Ls, Aa, Ab):
    min_startA = min(startsA)
    max_endA = max([startA + L for (startA,L) in zip(startsA, Ls)])
    Branges = []
    delimeters = [-np.inf] # let's assume there is no overlap in the functions??
    for startA, L in zip(startsA, Ls):
        delimeters += [startA]
        delimeters += [startA + L]
    delimeters += [np.inf]
    ids = np.digitize([Aa, Ab], delimeters)
    if ids[0] == ids[1]:  # the interval lies within a single mapping range
        #print("we are here")
        if ids[0]%2 == 1:  # And it actually falls out of the mapping ranges
            return [[Aa, Ab]]  # we return the original interva
        else:
            startid = int(ids[0]/2 - 1)
            return [[startsB[startid] + (Aa - startsA[startid]), 
                     startsB[startid] + (Ab - startsA[startid])]]
    else:  # The interval covers multiple mapping ranges
        n = ids[1] - ids[0] + 1
        i = 0
        Branges = []
        # we go form Aa to startsA[idx[0]]+Ls[idx[0]]
        # And this maps to 'from Ba to startsB[idx[0]]+Ls[idx[0]]'
        # where Ba is given by... startsB[idx[0]] + (Aa - startsA[idx[0]])
        if ids[0]%2 == 1:  # it falls out
            odd = 1
            startid = int((ids[0]-1)/2)
            Branges.append([Aa, startsA[startid]])
        else:
            startid = int(ids[0]/2 - 1)
            Branges.append([startsB[startid] + (Aa - startsA[startid]),
                        startsB[startid] + Ls[startid]])
            odd = -1
        # Now we get some fixed length pieces in the body
        i = 1
        odd = -1*odd
        while n-i > 1: 
            if odd > 0:
                startid = int((ids[0]-1)/2+i/2)
                Branges.append([startsA[startid-1] + Ls[startid-1], 
                                startsA[startid]])

            else:
                startid = int(ids[0]/2 + i/2 - 1)
                Branges.append([startsB[startid],
                                startsB[startid] + Ls[startid]])
            i+=1 
            odd=-1*odd
        # Then do the final piece
        if odd > 0:
            startid = int((ids[0]-1)/2+i/2)
            Branges.append([startsA[startid-1] + Ls[startid-1], 
                            Ab])
        else:
            startid = int(ids[0]/2 + i/2 - 1)
            Branges.append([startsB[startid],
                            startsB[startid] + Ab - startsA[startid]])
    return Branges

                    
oddseeds = seeds[1::2]
evenseeds = seeds[::2]
ranges = [
    [[es, es+oss] for (es,oss) in zip(evenseeds, oddseeds)]
]
for i,mapper in enumerate(mappers):
    ranges.append([])
    for ranger in ranges[i]:
        newranges=maprangeAtorangesB(mapper[:,1], mapper[:,0], mapper[:,2], ranger[0], ranger[1]-1)
        for newrange in newranges:
            ranges[i+1].append(newrange)
closest = np.inf
for el in test:
    if el[0] < el[1] and el[0] < closest:
        closest = el[0]
print("Closest loc for q2:", closest)

