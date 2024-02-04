#!/usr/bin/env python
# coding: utf-8

# In[23]:


import numpy as np

MOVES = [[-1,0,0], [0,1,1], [1,0,2], [0,-1,3]]  # N, E, S, W
DIRECS = ['N', 'E', 'S', 'W']

def oob(i,j,shape):
    if i < 0 or j < 0:
        return True
    if i >= shape[0] or j >= shape[1]:
        return True
    return False

def get_idx_least_dist_and_unvisited(dists, unvisited):
    masked = np.where(unvisited, dists, np.inf)
    min_ids = np.unravel_index(np.argmin(masked), dists.shape)
    return min_ids

def opposite(direc):
    direction_map = {'N': 'S', 'E': 'W', 'S': 'N', 'W': 'E'}
    return direction_map.get(direc, 'meh')
    
def get_valid_neighbours(i,j,z,k,unvisited,path):
    moves = MOVES.copy()
    direcs = DIRECS.copy()
    if path[-3:].count(path[-1]) == 3:
        moves.pop(direcs.index(path[-1]))
        direcs.remove(path[-1])
    for move, direc in zip(moves, direcs):
        if not oob(i+move[0], j+move[1], M.shape):
            knew = k + 1 if path[-1] == direc else 0
            if unvisited[i+move[0], j+move[1], move[2], knew] and                    direc != opposite(path[-1]):
                yield i+move[0], j+move[1], move[2], knew, direc

def get_valid_neighbours2(i,j,z,k,unvisited,path):
    moves = MOVES.copy()
    direcs = DIRECS.copy()
    counter = 1
    while path[-(counter+1)] == path[-1]:
        counter += 1
    n_lastdir = counter
    if n_lastdir == 10:
        mult = 4
        moves.pop(direcs.index(path[-1]))
        direcs.remove(path[-1])
        for move, direc in zip(moves, direcs):
            if not oob(i+mult*move[0], j+mult*move[1], M.shape) and                    direc != opposite(path[-1]):
                k = 0
                if unvisited[i+mult*move[0], j+mult*move[1], move[2], k]:
                    yield i+mult*move[0], j+mult*move[1], move[2], k, direc, mult
    else:
        for move, direc in zip(moves, direcs):
            if direc == path[-1]:
                mult = 1
                knew = k + 1
            else: 
                mult = 4
                knew = 0
            if not oob(i+mult*move[0], j+mult*move[1], M.shape) and                    direc != opposite(path[-1]):
                if unvisited[i+mult*move[0], j+mult*move[1], move[2], knew]:
                    yield i+mult*move[0], j+mult*move[1], move[2], knew, direc, mult

M = []
with open("test.txt", "r") as f:
    for line in f:
        M.append([int(x) for x in line.split()[0]])
M = np.array(M)

large_number = 10000000000
dists = np.ones((M.shape[0], M.shape[1], 4, 3), dtype=int)*large_number
unvisited = np.ones((M.shape[0], M.shape[1], 4, 3), dtype=bool)
dists[0,0,0] = 0
# fill every path el with a bogus value
paths = np.full((M.shape[0], M.shape[1], 4, 3),
                fill_value="bogus", dtype=object)

while unvisited[-1,-1,1].any() or unvisited[-1,-1,2].any():
    # find the unvisited node with the smallest distance
    # and visit it
    i,j,z,k = get_idx_least_dist_and_unvisited(dists, unvisited)
    unvisited[i,j,z,k] = False
    # get the unvisited neighbors of the current node
    path = paths[i,j,z,k] # path towards the current node
    moves = MOVES.copy()
    direcs = DIRECS.copy()
    for i2, j2, m2, k2, d2 in get_valid_neighbours(i,j,z,k,unvisited,path):
        dist = dists[i,j,z,k] + M[i2,j2]
        if dist < dists[i2,j2,m2,k2]:
            dists[i2,j2,m2,k2] = dist
            paths[i2,j2,m2,k2] = "" + path + d2

mindists = np.zeros_like(M)
for i, row in enumerate(dists):
    for j, col in enumerate(row):
        mindists[i,j] = np.min(dists[i,j])
print("q1:", np.min(mindists[-1,-1]))

### Q2 ###
M = []
with open("test.txt", "r") as f:
    for line in f:
        M.append([int(x) for x in line.split()[0]])
M = np.array(M)

large_number = 10000000000
dists = np.ones((M.shape[0], M.shape[1], 4, 7), dtype=int)*large_number
unvisited = np.ones((M.shape[0], M.shape[1], 4, 7), dtype=bool)
dists[0,0] = 0
# fill every path el with a bogus value
paths = np.full((M.shape[0], M.shape[1], 4, 7),
                fill_value="bogussssssssz", dtype=object)

while unvisited[-1,-1,1].any() or unvisited[-1,-1,2].any():
    i,j,z,k = get_idx_least_dist_and_unvisited(dists, unvisited)
    unvisited[i,j,z,k] = False
    # get the unvisited neighbors of the current node
    path = paths[i,j,z,k] # path towards the current node
    moves = MOVES.copy()
    direcs = DIRECS.copy()
    for i2, j2, m2, k2, d2, mult in get_valid_neighbours2(i,j,z,k,unvisited,path):
        dist = dists[i,j,z,k]
        start_idx = [i,j]
        end_idx = [i2,j2]
        di, dj = end_idx[0] - start_idx[0], end_idx[1] - start_idx[1]
        # either di or dj is zero, and for the other we sum from the smallest to the largest
        sumpart = 0
        if di == 0:
            third = -1 if dj < 0 else 1
            spool = start_idx[1] + third
            while spool != end_idx[1]:
                sumpart += M[start_idx[0], spool]
                spool += third
            sumpart += M[start_idx[0], spool]
        elif dj == 0:
            third = -1 if di < 0 else 1
            spool = start_idx[0] + third
            while spool != end_idx[0]:
                sumpart += M[spool, start_idx[1]]
                spool += third
            sumpart += M[spool, start_idx[1]]

        dist += sumpart
        if dist < dists[i2,j2,m2,k2]:
            dists[i2,j2,m2,k2] = dist
            paths[i2,j2,m2,k2] = "" + path + d2*mult
print("q2:", np.min(dists[-1,-1]))

