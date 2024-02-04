#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
M = []
with open("input.txt", "r") as f:
    for line in f:
        M.append([s for s in line.strip()])
M = np.array(M)

def move(prev, curr, typ):
    """
    prev: np.array([y,x])
    curr: np.array([y,x])
    typ: str
    """
    #print("type:", typ)
    direc = curr - prev
    if typ == ".":
        return [2 * curr - prev]
    if typ == "-":
        if abs(direc[1]) == 1:
            return [2 * curr - prev]
        else: 
            return [curr+np.array([0,1]), curr+np.array([0,-1])]
    if typ == "|":
        if abs(direc[0]) == 1:
            return [2 * curr - prev]
        else: 
            return [curr+np.array([1,0]), curr+np.array([-1,0])]
    if typ == "/":
        if direc[0] == 0:  # equal horizontal
            if direc[1] < 0:  # current is left of prev
                return [curr + np.array([1,0])]
            else:
                return [curr + np.array([-1,0])]
        else:  # equal vertical
            if direc[0] < 0:
                return [curr + np.array([0,1])]
            else:
                return [curr + np.array([0,-1])]
    if typ == "\\":
        if direc[0] == 0:  # equal horizontal
            if direc[1] < 0:
                return [curr + np.array([-1,0])]
            else:
                return [curr + np.array([1,0])]
        else:  # equal vertical
            if direc[0] < 0:
                return [curr + np.array([0,-1])]
            else:
                return [curr + np.array([0,1])]
            
            
def check_oob(pos, Mshape):
    if pos[0] < 0 or pos[0] >= Mshape[0]:
        return True
    if pos[1] < 0 or pos[1] >= Mshape[1]:
        return True
    return False

prev = np.array([0,0])
curr = np.array([1,0])
path = [[prev.tolist(), curr.tolist()]]
currents = [curr]
prevs = [prev]
step = 0
newones_generated = True
while newones_generated:
    newcurrents, newprevs = [], []
    for curr, prev in zip(currents, prevs):
        typ = M[curr[0], curr[1]]
        movecurrs = move(prev, curr, typ)
        newcurrents.extend([el for el in movecurrs if not check_oob(el, M.shape)])
        newprevs.extend([curr for el in movecurrs if not check_oob(el, M.shape)])
    newones_generated = False
    selnewcurrents, selnewprevs = [], []
    for c, p in zip(newcurrents, newprevs):
        if not check_oob(c, M.shape) and [p.tolist(), c.tolist()] not in path:
            path.append([p.tolist(), c.tolist()])
            newones_generated = True
            selnewcurrents.append(c)
            selnewprevs.append(p)
    step += 1
    currents, prevs = selnewcurrents, selnewprevs
path = np.array(path)
pathunique = set([(0,0)]+[(el[1,0], el[1,1]) for el in path])
print("q1:", len(pathunique))


# Q2: Too lazy to write a function for this, so i just do it 4 times....
lens = []
starts = []
for i in range(M.shape[0]):
    prev = np.array([-1,i])
    curr = np.array([0,i])
    path = [[prev.tolist(), curr.tolist()]]
    currents = [curr]
    prevs = [prev]
    newones_generated = True
    while newones_generated:
        newcurrents, newprevs = [], []
        for curr, prev in zip(currents, prevs):
            typ = M[curr[0], curr[1]]
            movecurrs = move(prev, curr, typ)
            newcurrents.extend([el for el in movecurrs if not check_oob(el, M.shape)])
            newprevs.extend([curr for el in movecurrs if not check_oob(el, M.shape)])
        newones_generated = False
        selnewcurrents, selnewprevs = [], []
        for c, p in zip(newcurrents, newprevs):
            if not check_oob(c, M.shape) and [p.tolist(), c.tolist()] not in path:
                path.append([p.tolist(), c.tolist()])
                newones_generated = True
                selnewcurrents.append(c)
                selnewprevs.append(p)
        step += 1
        currents, prevs = selnewcurrents, selnewprevs
    path = np.array(path)
    lens.append(len(set([(0,i)]+[(el[1,0], el[1,1]) for el in path])))

    prev = np.array([M.shape[0],i])
    curr = np.array([M.shape[0]-1,i])
    path = [[prev.tolist(), curr.tolist()]]
    currents = [curr]
    prevs = [prev]
    newones_generated = True
    while newones_generated:
        newcurrents, newprevs = [], []
        for curr, prev in zip(currents, prevs):
            typ = M[curr[0], curr[1]]
            movecurrs = move(prev, curr, typ)
            newcurrents.extend([el for el in movecurrs if not check_oob(el, M.shape)])
            newprevs.extend([curr for el in movecurrs if not check_oob(el, M.shape)])
        newones_generated = False
        selnewcurrents, selnewprevs = [], []
        for c, p in zip(newcurrents, newprevs):
            if not check_oob(c, M.shape) and [p.tolist(), c.tolist()] not in path:
                path.append([p.tolist(), c.tolist()])
                newones_generated = True
                selnewcurrents.append(c)
                selnewprevs.append(p)
        step += 1
        currents, prevs = selnewcurrents, selnewprevs
    path = np.array(path)
    lens.append(len(set([(M.shape[0]-1,i)]+[(el[1,0], el[1,1]) for el in path])))

    prev = np.array([i, -1])
    curr = np.array([i, 0])
    path = [[prev.tolist(), curr.tolist()]]
    currents = [curr]
    prevs = [prev]
    newones_generated = True
    while newones_generated:
        newcurrents, newprevs = [], []
        for curr, prev in zip(currents, prevs):
            typ = M[curr[0], curr[1]]
            movecurrs = move(prev, curr, typ)
            newcurrents.extend([el for el in movecurrs if not check_oob(el, M.shape)])
            newprevs.extend([curr for el in movecurrs if not check_oob(el, M.shape)])
        newones_generated = False
        selnewcurrents, selnewprevs = [], []
        for c, p in zip(newcurrents, newprevs):
            if not check_oob(c, M.shape) and [p.tolist(), c.tolist()] not in path:
                path.append([p.tolist(), c.tolist()])
                newones_generated = True
                selnewcurrents.append(c)
                selnewprevs.append(p)
        step += 1
        currents, prevs = selnewcurrents, selnewprevs
    path = np.array(path)
    lens.append(len(set([(i,0)]+[(el[1,0], el[1,1]) for el in path])))

    prev = np.array([i, M.shape[1]])
    curr = np.array([i, M.shape[1]-1])
    path = [[prev.tolist(), curr.tolist()]]
    currents = [curr]
    prevs = [prev]
    newones_generated = True
    while newones_generated:
        newcurrents, newprevs = [], []
        for curr, prev in zip(currents, prevs):
            typ = M[curr[0], curr[1]]
            movecurrs = move(prev, curr, typ)
            newcurrents.extend([el for el in movecurrs if not check_oob(el, M.shape)])
            newprevs.extend([curr for el in movecurrs if not check_oob(el, M.shape)])
        newones_generated = False
        selnewcurrents, selnewprevs = [], []
        for c, p in zip(newcurrents, newprevs):
            if not check_oob(c, M.shape) and [p.tolist(), c.tolist()] not in path:
                path.append([p.tolist(), c.tolist()])
                newones_generated = True
                selnewcurrents.append(c)
                selnewprevs.append(p)
        step += 1
        currents, prevs = selnewcurrents, selnewprevs
    path = np.array(path)
    lens.append(len(set([(i, M.shape[1]-1)]+[(el[1,0], el[1,1]) for el in path])))
print("q2:", max(lens))

