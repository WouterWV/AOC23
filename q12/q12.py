#!/usr/bin/env python
# coding: utf-8

# In[83]:


import numpy as np
import itertools
configs, groups = [], []
with open('input.txt', 'r') as f:
    for line in f:
        data = line.split()
        configs.append(data[0])
        groups.append([int(el) for el in data[1].split(',')])
print(configs)
print(groups)


# In[7]:



def get_N_of_conformations(groups, restraint, generalized=False):
    trials = []
    engrestraintpos = [i for i, el in enumerate(restraint) if el == '#']
    dotrestraintpos = [i for i, el in enumerate(restraint) if el == '.']
    Nleftdots = len(restraint) - sum(groups) - len(groups) + 1
    # I first made it way to general...
    if generalized:
        initperms = set([el for el in itertools.permutations(groups)])
    else:
        initperms = [(el for el in groups)]
    initstrings = ['.'.join(["#"*el for el in perm]) for perm in initperms]
    for initstring in initstrings:
        possibs =[0] + [i for i, el in enumerate(initstring) if el == '.'] + [len(initstring)]
        for leftoverdots in itertools.combinations_with_replacement(possibs, Nleftdots):
            trial = list(initstring)
            for pos in np.sort(leftoverdots)[::-1]:
                trial.insert(pos, '.')
            trials.append(''.join(trial))
    N_conform = 0
    goodtrials = []
    for trial in trials:
        good = True
        for restpos in engrestraintpos:
            if trial[restpos] != '#':
                good = False
                break
        for dotpos in dotrestraintpos:
            if trial[dotpos] != '.':
                good = False
                break
        if good:
            goodtrials.append(trial)
            N_conform += 1
    return N_conform


# In[9]:


import functools 
@functools.lru_cache(maxsize=None)
def get_N_of_conformations(groups, restraint, generalized=False):
    trials = []
    engrestraintpos = [i for i, el in enumerate(restraint) if el == '#']
    dotrestraintpos = [i for i, el in enumerate(restraint) if el == '.']
    Nleftdots = len(restraint) - sum(groups) - len(groups) + 1
    # I first made it way to general...
    if generalized:
        initperms = set([el for el in itertools.permutations(groups)])
    else:
        initperms = [(el for el in groups)]
    initstrings = ['.'.join(["#"*el for el in perm]) for perm in initperms]
    for initstring in initstrings:
        possibs =[0] + [i for i, el in enumerate(initstring) if el == '.'] + [len(initstring)]
        for leftoverdots in itertools.combinations_with_replacement(possibs, Nleftdots):
            trial = list(initstring)
            for pos in np.sort(leftoverdots)[::-1]:
                trial.insert(pos, '.')
            trials.append(''.join(trial))
    N_conform = 0
    goodtrials = []
    for trial in trials:
        good = True
        for restpos in engrestraintpos:
            if trial[restpos] != '#':
                good = False
                break
        for dotpos in dotrestraintpos:
            if trial[dotpos] != '.':
                good = False
                break
        if good:
            goodtrials.append(trial)
            N_conform += 1
    return N_conform


# In[10]:


# I read the question wrong: the dot engines are also fixed....
def get_N_conformations(group, restraint):
    trials = []
    engrestraintpos = [i for i, el in enumerate(restraint) if el == '#']
    possibs = [i for i, el in enumerate(restraint) if el == '?']
    Ntofillengines = sum(group) - len(engrestraintpos)
    for engpos in itertools.combinations(possibs, Ntofillengines):
        trial = list(restraint)
        for pos in engpos:
            trial[pos] = '#'
        # change ? to . 
        trial = ''.join(trial)
        trial = trial.replace('?', '.')
        trials.append(trial)
    N_conform = 0
    for trial in trials:
        lens = [len(el) for el in trial.split('.')]
        lens = [el for el in lens if el != 0]
        if lens == group:
            N_conform += 1
    return N_conform
    


# In[11]:


# I read the question wrong: the dot engines are also fixed....
def fill_and_check(sortedgroup, trials):
    newtrials = []
    for trial in trials:
        possibs = [i for i, el in enumerate(trial) if el == '?']
        # choose a possib, and place an engine there
        for possib in possibs:
            worktrial = list(trial)
            worktrial[possib] = '#'
            if checktrial(worktrial, sortedgroup):
                newtrials.append("".join(worktrial))
    return newtrials

def checktrial(trial, sortedgroup):
    trial = ''.join(trial)
    trial = trial.replace('?', '.')
    #print("checking trial: ", trial)
    lens = [len(el) for el in trial.split('.')]
    lens = [el for el in lens if el != 0]
    sortedlens = np.sort(lens)[::-1]
    for gl, sl in zip(sortedgroup, sortedlens):
        if sl > gl:
            return False
    return True

def get_Nconforms(group, restraint):
    sortedgroup = np.sort(group)[::-1]
    trials = [restraint]
    engrestraintpos = [i for i, el in enumerate(restraint) if el == '#']
    Ntofill = sum(sortedgroup) - len(engrestraintpos)
    while Ntofill > 0:
        trials = fill_and_check(sortedgroup, trials)
        trials = set(trials)
        #print(trials)
        Ntofill -= 1
    #trials = set([''.join(trial) for trial in trials])
    return number_of_good_conformations(trials, group)

def number_of_good_conformations(trials, group):
    #print("Trials we have to check: ", trials)
    N_conform = 0
    for trial in trials:
        trial = ''.join(trial)
        trial = trial.replace('?', '.')
        lens = [len(el) for el in trial.split('.')]
        lens = [el for el in lens if el != 0]
        if lens == group:
            N_conform += 1
    
    return N_conform
    


# In[8]:


N = 0
for group, restraint in zip(groups, configs):
    print(group, restraint)
    N+=get_Nconforms(group, restraint)
print(N)


# In[12]:



N = 0
for group, restraint in zip(groups, configs):
    #print(group, restraint)
    N += get_N_of_conformations(group, restraint)
print("q1:", N)

N2 = 0
for group, restraint in zip(groups, configs):
    print("doing a group")
    group = group*5
    restraint = "?".join([restraint for i in range(5)])
    N2 += get_N_of_conformations(group, restraint)
print("q2:", N2)


# In[41]:


def get_Nconforms(group, restraint):
    trials = [restraint.replace('#', '?')]
    for g in np.sort(group)[::-1]:
        new_trials = []
        for trial in trials:
           new_trials += add_group_to_trials(g, trial)
        #print("new trials: ", new_trials)
        trials = new_trials
    
    return number_of_good_conformations(trials, group)


def add_group_to_trials(group, trial):
    """
    trials: '??.#??.##.????????'
    we will try to place x's for engine groups
    """
    target = '?'*group
    locs = [i for i in range(len(trial)) if trial.startswith(target, i)]
    #print("locs: ", locs)
    newtrials = []
    for loc in locs:
        newtrial = trial[:loc] + 'x'*group + trial[loc+group:]
        #print("newtrial: ", newtrial)
        newtrials.append(newtrial)
    return set(newtrials)


def number_of_good_conformations(trials, group):
    #print("Trials we have to check: ", trials)
    N_conform = 0
    for trial in trials:
        trial = ''.join(trial)
        trial = trial.replace('?', '.')
        lens = [len(el) for el in trial.split('.')]
        lens = [el for el in lens if el != 0]
        if lens == group:
            N_conform += 1
    
    return N_conform

        


# In[ ]:


def add_engines(restraint, group):
    """
    restraint: '????#????'
    group: 3
    """
    Ntofill = sum(group) - restraint.count('#')
    locs = [i for i in range(len(restraint)) if restraint[i] == '?']
    goupstodo = np.sort(groups)[::-1]
    trials = [restraint]
    for loc in locs:
        newtrial = restraint[:loc] + '#' + restraint[loc+group:]
        newtrials.append(newtrial)
    return newtrials


# In[ ]:





# In[45]:


N = 0
for group, restraint in zip(groups, configs):
    print(group, restraint)
    N+=get_Nconforms(group, restraint)
print(N)


# In[17]:


trial = '???.#??.##.????????'
group = 3
target = '?'*group
locs = [i for i in range(len(trial)) if trial.startswith(target, i)]
print(locs)


# In[18]:


ntrial = trial.replace('#', '?')


# In[19]:


trial


# In[ ]:





# In[26]:


import numpy as np
import functools
configs, groups = [], []
with open('input.txt', 'r') as f:
    for line in f:
        data = line.split()
        configs.append(data[0])
        groups.append([int(el) for el in data[1].split(',')])


# In[33]:


N = 0
for config, group in zip(configs, groups):
    N+= get_Nconform(config, tuple(group))
print(N)


# In[87]:


@functools.lru_cache(maxsize=None)
def get_conformations(config, groups):
    if not groups:
        if "#" not in config:
            return 1
        else:
            return 0
    if not config: 
        return 0
    character = config[0]
    group = groups[0]

    def hashtag():
        subconfig = config[:group]
        # let's see if we can fit group*hashtags into subconfig
        subconfig = subconfig.replace('?', '#')
        # if "." in subconfig:  ## THIS DIT NOT ACCOUNT FOR TOO SHORT SUBCONFIGS
        if subconfig != group*'#':
            return 0  # did not work
        else:
            if len(groups) == 1:  # we are done
                # but check whether there was config left!!
                if "#" in config[group:]:
                    return 0
                return 1
            else:  # keep going
                # but check whether we have . or ? after this group
                if len(config) < group + 1:  # not big enough
                    return 0
                if config[group] not in '.?':
                    return 0
                return get_conformations(config[group+1:], groups[1:])
    
    def point():
        if len(config) == 1:
            return 0
        return get_conformations(config[1:], groups)
    

    if character == '#':
        return hashtag()
    elif character == '.':
        return point()
    elif character == '?':
        return hashtag() + point()


# In[90]:


N = 0
for config, group in zip(configs, groups):
    N+=(get_conformations(config, tuple(group)))
print("q1: ", N)

N2 = 0
for config, group in zip(configs, groups):
    group = group*5
    config = "?".join([config for i in range(5)])
    N2 += get_conformations(config, tuple(group))
print("q2:", N2)


# In[82]:


N


# In[ ]:




