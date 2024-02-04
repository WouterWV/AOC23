#!/usr/bin/env python
# coding: utf-8

# In[174]:


import numpy as np

def get_new_pos(r, d, direc):
    r = np.array(r)
    if direc == "R":
        r[0] += d
    elif direc == "L":
        r[0] -= d
    elif direc == "U":
        r[1] += d
    elif direc == "D":
        r[1] -= d
    return r

path = [np.array([0,0])]
with open("input.txt", "r") as f:
    for line in f:
        d, r = line.split()[0], int(line.split()[1])
        path.append(get_new_pos(path[-1], r, d))
path = np.array(path)

minx, maxx = min(path[:,0]), max(path[:,0])
miny, maxy = min(path[:,1]), max(path[:,1])
# shift path to positive
path[:,0] += abs(minx)
path[:,1] += abs(miny)

M = np.zeros((maxx-minx+1, maxy-miny+1))
curr = path[0]
for pathel in path[1:]:
    for i in range(min(curr[0], pathel[0]), max(curr[0], pathel[0])+1):
        for j in range(min(curr[1], pathel[1]), max(curr[1], pathel[1])+1):
            M[i,j] += 1 if M[i,j] != 1 else 0
    curr = pathel

def oob(pos, shape):
    return pos[0] < 0 or pos[1] < 0 or pos[0] >= shape[0] or pos[1] >= shape[1]

# floodfill to find area
start = (100,250)
filled = np.zeros(M.shape)
to_fill = [start]
moves = [np.array([0,1]), np.array([0,-1]), np.array([1,0]), np.array([-1,0])]
while to_fill:
    new_to_fill = []
    for spool in to_fill:
        for move in moves:
            new_pos = np.array(spool) + move
            if not oob(new_pos, M.shape):
                if M[new_pos[0], new_pos[1]] != 1 and                    filled[new_pos[0], new_pos[1]] == 0:
                    filled[new_pos[0], new_pos[1]] = 1
                    new_to_fill.append((new_pos[0], new_pos[1]))
    new_to_fill = set(new_to_fill)
    to_fill = new_to_fill

print("q1:", int(np.sum(filled)+np.sum(M)))

# part 2
def get_dir(n):
    if n == 0:
        return "R"
    elif n == 1:
        return "D"
    elif n == 2:
        return "L"
    elif n == 3:
        return "U"
L = 0
path = [np.array([0,0])]
with open("input.txt", "r") as f:
    for line in f:
        rl = line.split()[2]
        r = int(rl[2:-2], 16)
        d = get_dir(int(rl[-2]))
        L += r
        path.append(get_new_pos(path[-1], r, d))
path = np.array(path)

def shoelace(x, y):
    """
    # https://stackoverflow.com/a/30408825
    """
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

def picks_theorem(x, y, L):
    """ 
    https://en.wikipedia.org/wiki/Pick%27s_theorem
    """
    return shoelace(x, y) + 1 + L//2

print("q2:", int(picks_theorem(path[1:,0], path[1:,1], L)))


# In[ ]:




