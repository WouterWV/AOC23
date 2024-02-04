#!/usr/bin/env python
# coding: utf-8

# In[223]:


import numpy as np
M = []
with open("input.txt", 'r') as f:
    for line in f:
        M.append([0 if el == '.' else 1 if el == '#' else 2 for el in line.strip()])
M = np.array(M)
# get indices where M == 2:
S = np.where(M == 2)
M[S] = 0
S = np.array([S[0][0], S[1][0]])
Sp = [S[0], S[1], 0, 0]

def oob(i, j, Mshape):
    return i < 0 or j < 0 or i >= Mshape[0] or j >= Mshape[1]

def move(r, M):
    moves = [[-1,0], [1,0], [0,-1], [0,1]]
    possible_moves = []
    for i,j in moves:
        if not oob(r[0]+i, r[1]+j, M.shape):
            if M[r[0]+i, r[1]+j] == 0:
                possible_moves.append((r[0]+i, r[1]+j))
    return possible_moves

def periodicmove(r, M):
    # now we keep i,j,I,J
    moves = [[-1,0], [1,0], [0,-1], [0,1]]
    possible_moves = []
    for i,j in moves:
        if M[(r[0]+i)%M.shape[0], (r[1]+j)%M.shape[1]] == 0:
            possible_moves.append(((r[0]+i)%M.shape[0], (r[1]+j)%M.shape[1],
                                   (r[0]+i)//M.shape[0]+r[2],
                                   (r[1]+j)//M.shape[1]+r[3]))
    #print(f"from {r}: {possible_moves}")
    return possible_moves
    
def Nsteps(r, M, N, periodic=True):
    steps = 0
    current = [r]
    while steps < N and current:
        #print("step:", steps)
        nexter = []
        for c in current:
            if periodic:
                nexter.extend(periodicmove(c,M))
            else:
                nexter.extend(move(c,M))
        nexter = list(set([tuple(el) for el in nexter]))
        current = nexter
        steps += 1
    return current

steps = 26501365
# steps before we get to the diamond shape: 65
# then we have 131 steps to get the new diamond shape
rdiamond = (steps-65) // 131
leftoversteps = (steps-65) % 131

Aodd = np.sum(evenA * np.array([4*i-4 for i in range(1, rdiamond+2, 2)]))
Aeven = np.sum(oddA * np.array([4*i-4 for i in range(2, rdiamond+2, 2)]))
print(Aodd+Aeven)

# reddit post solution
G = {i+j*1j:c for i,r in enumerate(open('input.txt'))
              for j,c in enumerate(r) if c in '.S'}

done = []
todo = {x for x in G if G[x]=='S'}
cmod = lambda x: complex(x.real%131, x.imag%131)

for s in range(3 * 131):
    if s == 64: print(len(todo))
    if s%131 == 65: done.append(len(todo))

    todo = {p+d for d in {1, -1, 1j, -1j}
                for p in todo if cmod(p+d) in G}

f = lambda n,a,b,c: a+n*(b-a+(n-1)*(c-b-b+a)//2)
print(f(26501365 // 131, *done))

