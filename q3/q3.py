#!/usr/bin/env python
# coding: utf-8

# In[50]:


draws, wnrs = [], []
with open("input.txt", "r") as f:
    for line in f:
        line = (line.strip().split(":")[1])
        dat = line.split("|")
        draw = [(el) for el in dat[0][1:-1].split(" ")]
        draws.append([int(el) for el in draw if el != ""])
        wnr = [(el) for el in dat[1][1:].split(" ")]
        wnrs.append([int(el) for el in wnr if el != ""])

tot = 0
for (wnr, draw) in zip(draws, wnrs):
    drawpt = 0
    for d in draw:
        if d in wnr:
            drawpt+=1
    if drawpt>0:
        tot += 2**(drawpt-1)
print("q1:", int(tot))
numbers = [i for i in range(len(draws))]
winningnumbers = [0 for i in range(len(draws))]
for (i, wnr, draw) in zip([k for k in range(len(draws))], draws, wnrs):
    for d in draw:
        if d in wnr:
            winningnumbers[i] += 1
numbers = [1 for i in range(len(draws))]
for k, wins in enumerate(winningnumbers):
    for i in range(wins):
        numbers[k+i+1] += numbers[k]
print("q2:", sum(numbers))

