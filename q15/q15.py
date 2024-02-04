#!/usr/bin/env python
# coding: utf-8

# In[54]:


import numpy as np
# import ascii stuff
with open("input.txt", "r") as f:
    for line in f:
        words = line.strip().split(',')

def hashmap(word):
    cv = 0
    for letter in word:
        # get ascii value of letter
        cv += ord(letter)
        cv *= 17
        cv %= 256
    return cv

cvs = []
for word in words:
    cvs.append(hashmap(word))
print("q1:", sum(cvs))

boxes = [[] for i in range(256)]
instructions = []
for word in words:
    if "-" in word:
        box = int(hashmap(word.split('-')[0]))
        label = word.split('-')[0]
        if label in [b[0] for b in boxes[box]]:
            # remove label from box
            boxes[box].remove([b for b in boxes[box] if b[0] == label][0])
    if "=" in word:
        box = int(hashmap(word.split('=')[0]))
        label, pos = word.split('=')[0], int(word.split('=')[1])
        if label not in [b[0] for b in boxes[box]]:
            # add label to box
            boxes[box].append([label, pos])
        else:
            # update label in box
            boxes[box][[b[0] for b in boxes[box]].index(label)][1] = pos

focal_power = 0
for i, box in enumerate(boxes):
    for j, lens in enumerate(box):
        local_power = (i+1)*(j+1)*lens[1]
        focal_power += local_power
print("q2:", focal_power)


# In[ ]:




