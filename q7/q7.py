#!/usr/bin/env python
# coding: utf-8

# In[52]:


import numpy as np
import os
os.chdir("/home/wouter/AOC/q7")

hands, bids = [], []
with open("input.txt", "r") as f:
    for i,line in enumerate(f):
        bids.append(int(line.split()[-1]))
        hands.append(line.split()[0])

def hand_to_typeandhighs(hand, cardels, part2=False):
    """
    The jokers influence only the type, so just increase the highest count 
    by the amount of jokers, and that's that...
    """
    counts = np.zeros_like(cardels, dtype=int)
    high = []
    jokers = 0
    for card in hand:
        idx = cardels.index(card)
        if idx == len(cardels)-1:
            jokers += 1
        else:
            counts[idx] += 1
        high.append(idx)
    counts = np.sort(counts)[::-1]
    if part2:
        counts[0] += jokers
    if counts[0] == 5:
        type = 0
    elif counts[0] == 4:
        type = 1
    elif counts[0] == 3:
        type = 2 if counts[1] == 2 else 3
    elif counts[0] == 2:
        type = 4 if counts[1] == 2 else 5
    else: 
        type = 6
    return [type] + [el for el in high]

# Q1
cardels = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
results = [hand_to_typeandhighs(hand, cardels) for hand in hands]
results = np.array([el + [bid] for el, bid, hand in zip(results, bids, hands)])
copyresults = results.copy()
# sort by type
results = results[results[:,0].argsort(), :]
# and then sort by Nth high card
for j in range(1, 6):
    k = 0
    while k < len(results):
        kk = k+1
        while (results[kk][:j] == results[k][:j]).all():
            kk += 1
            if kk >= len(results):
                break
        if kk - k > 1:
            results[k:kk] = results[k+results[k:kk,j].argsort(),:]
        k = kk
        if kk >= len(results) - 1:
            break

total = 0
for i, el in enumerate(results[::-1]):
    total += float(el[-1]) * (i+1)
print("Total winnings q1:", total)

# Q2
cardels = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]
results = [hand_to_typeandhighs(hand, cardels, True) for hand in hands]
for el in results:
    print(el)
results = np.array([el + [bid] for el, bid, hand in zip(results, bids, hands)])
copyresults = results.copy()
# sort by type
results = results[results[:,0].argsort(), :]
# and then sort by Nth high card
for j in range(1, 6):
    k = 0
    while k < len(results):
        kk = k+1
        while (results[kk][:j] == results[k][:j]).all():
            kk += 1
            if kk >= len(results):
                break
        if kk - k > 1:
            results[k:kk] = results[k+results[k:kk,j].argsort(),:]
        k = kk
        if kk >= len(results) - 1:
            break

total = 0
for i, el in enumerate(results[::-1]):
    total += float(el[-1]) * (i+1)
print("Total winnings q2:", total)

