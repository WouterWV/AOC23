#!/usr/bin/env python
# coding: utf-8

# In[122]:


import numpy as np
workflows = {}
objects = []  # x m a s
object_map = {"x": 0, "m": 1, "a": 2, "s": 3}

with open("input.txt", 'r') as f:
    for line in f:
        if not line.startswith("{") and line != "\n":
            data = line.split("{")
            workflows[data[0]] = []
            for el in data[1].split(","):
                if ":" in el:
                    workflows[data[0]].append(el.split(":"))
                else:
                    workflows[data[0]].append([el[:-2]])
        elif line != "\n":
            objects.append([int(el.split("=")[-1]) for el in line[1:-2].split(",")])

def check_condition(workflowid, object, workflows):
    workflow = workflows[workflowid]
    maxcriteria = len(workflow)
    criterion_met = False
    count = 0
    
    while not criterion_met:
        if count == maxcriteria -1:
            if workflow[count][0] == "A":
                return True
            if workflow[count][0] == "R":
                return False
            else:
                return check_condition(workflow[count][0], object, workflows)
        object_id = workflow[count][0][0]
        comparer = workflow[count][0][1]
        cutoff = int(workflow[count][0][2:])
        if comparer == "<":
            criterion_met = object[object_map[object_id]] < cutoff
        elif comparer == ">":
            criterion_met = object[object_map[object_id]] > cutoff
        if criterion_met:
            if workflow[count][1] == "A":
                return True
            if workflow[count][1] == "R":
                return False
            else:
                return check_condition(workflow[count][1], object, workflows)
        else:
            count += 1
    
total = 0
for object in objects:
    if check_condition("in", object, workflows):
        total += np.sum(object)
print("q1:", total)

def split_range_condition(workflow, r, count):
    """ r: [[minx, maxx], [minm, maxm], [mina, maxa], [mins, maxs]]

    example output: let's say that dimension 2 will be split along cutoff
    
    output: r1 = [[minx, maxx], [minm, maxm], [mina, cutoff-1], [mins, maxs]]
            r2 = [[minx, maxx], [minm, maxm], [cutoff, maxa], [mins, maxs]]
    """
    object_id = workflow[count][0][0]
    comparer = workflow[count][0][1]
    cutoff = int(workflow[count][0][2:])
    # we know that the range will be split into two ranges
    met_ranges = []
    notmet_ranges = []
    if comparer == "<":
        # split our range into two ranges based on the cutoff
        if r[object_map[object_id]][1] < cutoff:
            met_ranges.append(r[object_map[object_id]])
        elif r[object_map[object_id]][0] > cutoff:
            notmet_ranges.append(r[object_map[object_id]])
        else:
            met_ranges.append([r[object_map[object_id]][0], cutoff-1])
            notmet_ranges.append([cutoff, r[object_map[object_id]][1]])
    if comparer == ">":
        if r[object_map[object_id]][0] > cutoff:
            met_ranges.append(r[object_map[object_id]])
        elif r[object_map[object_id]][1] < cutoff:
            notmet_ranges.append(r[object_map[object_id]])
        else:
            met_ranges.append([cutoff+1, r[object_map[object_id]][1]])
            notmet_ranges.append([r[object_map[object_id]][0], cutoff])
    # now we need to add back the other dimensions
    real_met_ranges = []
    real_notmet_ranges = []
    for i in range(4):
        if i == object_map[object_id]:
            if met_ranges != []:
                real_met_ranges.append(met_ranges[0])
            if notmet_ranges != []:
                real_notmet_ranges.append(notmet_ranges[0])
        else:
            if met_ranges != []:
                real_met_ranges.append(r[i])
            if notmet_ranges != []:
                real_notmet_ranges.append(r[i])
    return real_met_ranges if met_ranges != [] else None, real_notmet_ranges if notmet_ranges != [] else None

startrange = [[1, 4000], [1, 4000], [1, 4000], [1, 4000]]
def check_range(workflow, r, count):
    """For a workflow at count with range r, return a list of ranges with their new workflows and counts"""
    met, notmet = split_range_condition(workflow, r, count)
    ranges = []
    if met is not None:
        if workflow[count][1] == "A":
            ranges.append([met, "A"])
        elif workflow[count][1] == "R":
            ranges.append([met, "B"])
        else:
            ranges.append([met, workflows[workflow[count][1]], 0])            
    if notmet is not None:
        if count == len(workflow) - 2:
            if workflow[-1][0] == "A":
                ranges.append([notmet, "A"])
            elif workflow[-1][0] == "R":
                ranges.append([notmet, "B"])
            else: 
                ranges.append([notmet, workflows[workflow[-1][0]], 0])
        else:
            if workflow[count+1][0] == "A":
                ranges.append([notmet, "A"])
            elif workflow[count+1][0] == "R":
                ranges.append([notmet, "B"])
            else:
                ranges.append([notmet, workflow, count+1])
    
    return ranges

running = [[startrange, workflows["in"], 0]]
finishedA = []
finishedB = []
while running:
    new_running = []
    for run in running:
        ranges = check_range(run[1], run[0], run[2])
        for el in ranges:
            new_running.append(el)
    running = []
    for el in new_running:
        if el[1] == "A":
            finishedA.append(el[0])
        elif el[1] == "B":
            finishedB.append(el[0])
        else:
            running.append(el)

def rangelen(r):
    # r: [[minx, maxx], [minm, maxm], [mina, maxa], [mins, maxs]]
    return (r[0][1] - r[0][0]+1) * (r[1][1] - r[1][0]+1) * (r[2][1] - r[2][0]+1) * (r[3][1] - r[3][0]+1)

total = 0
for r in finishedA:
    total += rangelen(r)
print("q2:", total)

