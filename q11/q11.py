#!/usr/bin/env python
# coding: utf-8

# In[82]:


with open('input.txt', 'r') as f:
    M = []
    for line in f:
        M.append([0 if el == "." else 1 for el in line.strip()])
Mlist = M.copy()
M = np.array(M)

rowins, colins = [], []
for i in range(len(M)):
    if sum(M[i,:]) == 0:
        rowins.append(i)
    if sum(M[:,i]) == 0:
        colins.append(i)
print(rowins, colins)

# for i in rowins[::-1]:
#     Mlist.insert(i, [0 for el in range(len(Mlist[0]))])
# Mlist = np.array(Mlist).T.tolist()
# for i in colins[::-1]:
#     Mlist.insert(i, [0 for el in range(len(Mlist[0]))])
# Mlist = np.array(Mlist).T.tolist()
# M = np.array(Mlist)

galaxies = []
for i in range(len(M)):
    for j in range(len(M[0])):
        if M[i,j] == 1:
            galaxies.append((i,j))

def distance(i, j, k, l):
    return abs(k-i) + abs(j-l)

def distance2(i, j, k, l, rowins, colins, Nexp):
    dist = distance(i, j, k, l)
    for r in rowins:
        if i<=r<=k or k<=r<=i:
            dist+=Nexp
    for c in colins:
        if j<=c<=l or l<=c<=j:
            dist+=Nexp
    return dist

total = 0
total2 = 0
for i in range(len(galaxies)):
    for j in range(i+1, len(galaxies)):
        total += distance2(galaxies[i][0], galaxies[i][1],
                          galaxies[j][0], galaxies[j][1],
                          rowins, colins, 1)
        total2 += distance2(galaxies[i][0], galaxies[i][1],
                            galaxies[j][0], galaxies[j][1],
                            rowins, colins, 999999)
print(total)
print(total2)


# In[ ]:





# In[ ]:




