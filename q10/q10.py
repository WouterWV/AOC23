#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import os
os.chdir("/home/wouter/AOC/q10")
M = []
with open("input.txt") as f:
    for line in f:
        M.append(list(line.strip()))
M = np.array(M)

map = {}
map["-"] = [np.array([0,-1]), np.array([0, 1])]
map["|"] = [np.array([-1, 0]), np.array([1, 0])]
map["L"] = [np.array([0, 1]), np.array([-1, 0])]
map["J"] = [np.array([0, -1]), np.array([-1, 0])]
map["7"] = [np.array([0, -1]), np.array([1, 0])]
map["F"] = [np.array([0, 1]), np.array([1, 0])]
map["S"] = [[]]
map["."] = []

start = np.where(M == "S")
startpos = np.array([start[0][0], start[1][0]])

def get_start_token(pos):
    connects = []
    for i in [-1,0,1]:
        for j in [-1,0,1]:
            if i == 0 and j == 0:
                continue
            possloc = pos[0]+i, pos[1]+j
            poss = map[M[possloc]]
            for possib in poss:
                if (possloc + possib == pos).all():
                    connects.append(possloc-pos)
    return connects

startmoves = get_start_token(startpos)
map["S"] = startmoves
pathlens, paths = [], []
for k in [0,1]:
    path1 = [startpos + startmoves[k]]
    while not (path1[-1] == startpos).all():
        dirs = map[M[path1[-1][0], path1[-1][1]]]
        possibs = [path1[-1] + el for el in dirs]
        for i,possib in enumerate(possibs):
            if len(path1) > 1:
                if not ((possib == path1[-1]).all() or (possib == path1[-2]).all()):
                    move = possib
                    break
            else:
                if not (possib == path1[-1]).all():
                    move = possib
                    break
        path1.append(move)

    pathlens.append(len(path1))
    paths.append(path1)
assert pathlens[0] == pathlens[1]
print("q1:", int(pathlens[0]/2))


# Floodfill for q2, but first make the map bigger because enclosed 
# spaces are not connected in the original pixel map...
loop = []
for path in paths:
    for el in path:
        loop.append([el[0], el[1]])
Mbig = np.zeros((3*len(M), 3*len(M[0])), dtype=int)
bigloop = np.zeros((3*len(M), 3*len(M[0])), dtype=int)
for i in range(len(M)):
    for j in range(len(M[i])):
        if M[i,j] == ".":
            continue
        Mbig[3*i+1, 3*j+1] = 1
        for moves in map[M[i,j]]:
            Mbig[3*i+1+moves[0], 3*j+1+moves[1]] = 1
        if [i,j] in loop:
            bigloop[3*i+1, 3*j+1] = 1
            for moves in map[M[i,j]]:
                bigloop[3*i+1+moves[0], 3*j+1+moves[1]] = 1

seed = [237, 225]
running_seeds = [seed]
filled = [seed]
while len(running_seeds) != 0:
    new_running_seeds = []
    print(len(running_seeds))
    for seed in running_seeds:
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                probei,probej = seed[0]+i, seed[1]+j
                probe = [seed[0]+i, seed[1]+j]
                if probe not in filled and bigloop[probei, probej] != 1:
                    filled.append(probe)
                    if probe not in new_running_seeds:
                        new_running_seeds.append(probe)
    running_seeds = new_running_seeds
    
total = 0
for i in range(len(M)):
    for j in range(len(M[i])):
        if [3*i+1, 3*j+1] in filled:
            total += 1
print("q2:", total)

# import matplotlib.pyplot as plt
# %matplotlib qt
# fig, ax = plt.subplots()
# ax.imshow(Mbig)
# ax.imshow(bigloop, alpha=0.5)
# fig.show()

