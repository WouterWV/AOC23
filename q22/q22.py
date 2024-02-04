#!/usr/bin/env python
# coding: utf-8

# In[318]:


import numpy as np
class Brick():
    def __init__(self, brick, id=None):
        self.start = brick[0]
        self.end = brick[1]
        self.supported_by = []
        self.supports = []
        self.removable = False
        self.removed = False
        self.id = id

    def points_in_brick(self):
        for i in range(self.start[0], self.end[0]+1):
            for j in range(self.start[1], self.end[1]+1):
                for k in range(self.start[2], self.end[2]+1):
                    yield [i,j,k]

    def contains_point(self, p):
        if p[0] >= self.start[0] and p[0] <= self.end[0] and           p[1] >= self.start[1] and p[1] <= self.end[1] and           p[2] >= self.start[2] and p[2] <= self.end[2]:
            return True
        else:
            return False
        
    def supports_brick(self, brick):
        for point in brick.points_in_brick():
            if self.contains_point(point+np.array([0,0,-1])):
                return True
        return False
    
    def is_supported_by_brick(self, brick):
        return brick.supports_brick(self)
    
    def how_many_do_i_support(self, bricklist):
        count = 0
        supported_bricks = []
        for brick in bricklist:
            if not brick == self:
                if self.supports_brick(brick):
                    count += 1
                    supported_bricks.append(brick)
        self.supports = count
        self.supported_bricks = supported_bricks
        return count
    
    def how_many_support_me(self, bricklist):
        count = 0
        support_bricks = []
        for brick in bricklist:
            if not brick == self:
                if self.is_supported_by_brick(brick):
                    count += 1
                    support_bricks.append(brick)
        self.supported_by = count
        self.support_bricks = support_bricks
        return count

    def __str__(self):
        return str(self.start) + " " + str(self.end)
    
    # is this brick the same as another brick?
    def __eq__(self, other):
        if all(self.start == other.start) and all(self.end == other.end):
            return True
        else:
            return False
            
bricks = []
with open("input.txt", 'r') as f:
    for line in f:
        bricks.append([np.array([int(il) for il in el.split(",")])                       for el in line.strip().split("~")])
bricks = np.array(bricks)

# sort bricks by their lowest z-position
bricks = np.array([brick if brick[0,2] <= brick[1,2] else brick[::-1]                   for brick in bricks])
# do the other dims as well (they should be same if z differs already...)
bricks = np.array([brick if brick[0,1] <= brick[1,1] else brick[::-1]                   for brick in bricks])
bricks = np.array([brick if brick[0,0] <= brick[1,0] else brick[::-1]                   for brick in bricks])
sorter = np.argsort(bricks[:,0,2])
bricks = bricks[sorter]

# values are all positive :) 
stationary_bricks = np.zeros((np.max(bricks[:,:,0]+1),
                              np.max(bricks[:,:,1]+1),
                              np.max(bricks[:,:,2])+2))
# set the z = 0 plane to ones
stationary_bricks[:,:,0] = 1

for brick in bricks:
    # get the closest bricks directly below the current brick
    #print("working on brick", brick)
    dists = []
    brickidsbelow = np.where(stationary_bricks[brick[0,0]:brick[1,0]+1,
                                               brick[0,1]:brick[1,1]+1]==1)
    # get max z-position of these bricks
    maxz = np.max(brickidsbelow[2])

    dz = brick[0,2] - maxz - 1 
    # set the brick to the new z-position
    brick[:,2] -= dz
    # add the brick to the stationary bricks
    stationary_bricks[brick[0,0]:brick[1,0]+1,brick[0,1]:brick[1,1]+1,
                      brick[0,2]:brick[1,2]+1] = 1

# let's resort the bricks by their z-position
sorter = np.argsort(bricks[:,0,2])
bricks = bricks[sorter]

# and do q2 first because I don't need the brick object for that 
# (probably not for q1 either but I'm lazy)
nfalls = []
for i,bbrick in enumerate(bricks):
    # do not loop over brick i 
    newbricks = [brick for brick in bricks[:i]] +                [brick for brick in bricks[i+1:]]
    newbricks = np.array(newbricks)
    fallen_bricks = 0
    # values are all positive :) 
    stationary_bricks = np.zeros((np.max(newbricks[:,:,0]+1),
                                  np.max(newbricks[:,:,1]+1),
                                  np.max(newbricks[:,:,2])+2))
    # set the z = 0 plane to ones
    stationary_bricks[:,:,0] = 1
    for brick in newbricks:
        # get the closest bricks directly below the current brick
        #print("working on brick", brick)
        brickidsbelow = np.where(stationary_bricks[brick[0,0]:brick[1,0]+1,
                                                   brick[0,1]:brick[1,1]+1]==1)
        # get max z-position of these bricks
        maxz = np.max(brickidsbelow[2])

        dz = brick[0,2] - maxz - 1 
        if dz != 0:
            fallen_bricks += 1
        # set the brick to the new z-position
        brick[:,2] -= dz
        # add the brick to the stationary bricks
        stationary_bricks[brick[0,0]:brick[1,0]+1,
                          brick[0,1]:brick[1,1]+1,
                          brick[0,2]:brick[1,2]+1] = 1
    nfalls.append(fallen_bricks)

print("q2:", np.sum(nfalls))

# now let's make brick objects of these bricks
bricks = [Brick(brick,i) for i,brick in enumerate(bricks)]

# set the supported_by and supports attributes
for brick in bricks:
    brick.how_many_do_i_support(bricks)
    brick.how_many_support_me(bricks)

n_supported_by_more_than_one = 0

n_supports_nothing = 0
bricklist = []
for brick in bricks:
    if all(sbrick.supported_by > 1 for sbrick in brick.supported_bricks):
        # this also covers bricks that don't support anything!!
        n_supported_by_more_than_one += 1
        bricklist.append(brick)

# get unique bricks
unique_bricks = []
for brick in bricklist:
    if brick not in unique_bricks:
        unique_bricks.append(brick)

print("q1:", len(unique_bricks))

