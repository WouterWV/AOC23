#!/usr/bin/env python
# coding: utf-8

# In[202]:


import numpy as np
planes = []
with open("input.txt", "r") as f:
    plane = []
    for line in f:
        if line=="\n":
            planes.append(plane)
            plane = []
        else:
            plane.append([1 if el =="." else 0 for el in line.strip()])
    planes.append(plane)
planes = [np.array(plane) for plane in planes]

def find_mirror(M, ignore=666):
    for i in range(1, M.shape[1]):
        mirror = True
        k = 1
        while k+i <= M.shape[1] and i - k >= 0: 
            if M[:,i-k].tolist() != M[:,i+k-1].tolist():
                mirror = False 
                break
            k += 1
        if mirror and i != ignore:
            return i
    return 0

Hmirrors, Vmirrors = [], []
newHmirrors, newVmirrors = [], []
for k,plane in enumerate(planes):
    # I was expecting multiple mirrors in part two, now damage controlling
    vmirror = find_mirror(plane)
    Vmirrors.append(vmirror)
    hmirror = find_mirror(plane.T)
    Hmirrors.append(hmirror)
    i = 0
    found = False
    while i < plane.shape[0] and not found:
        j = 0
        while j < plane.shape[1] and not found:
            newplane = plane.copy()
            newplane[i,j] = 0 if plane[i,j] == 1 else 1
            newvmirror = find_mirror(newplane, ignore=vmirror)
            newhmirror = find_mirror(newplane.T, ignore=hmirror)
            if newvmirror != 0:
                newVmirrors.append(newvmirror)
                # break out of both for loops
                found = True
            if newhmirror != 0:
                newHmirrors.append(newhmirror)
                found = True
            j += 1
        i += 1
    if not found:
        print("No mirror found for plane", k)

print("q1:", sum(Vmirrors)+100*sum(Hmirrors))
print("q2:", sum(newVmirrors)+100*sum(newHmirrors))

