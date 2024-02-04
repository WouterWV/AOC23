#!/usr/bin/env python
# coding: utf-8

# In[54]:


import numpy as np
def read_graph(fn):
    graph = {}
    with open(fn, "r") as f:
        for line in f:
            mtype = line[0]
            data = line[1:].split()
            if data[0] == "roadcaster":
                mname = "broadcaster"
                mtype = "broadcaster"
            else:
                mname = data[0]
            connected_module_raw = data[2:]
            connected_modules =                [el[:-1] if el[-1] =="," else el for el in connected_module_raw]
            graph[mname] = {}
            graph[mname]['type'] = mtype
            graph[mname]['connects'] = connected_modules
            if mtype == "%":
                graph[mname]['state'] = 0
            elif mtype == "&":
                graph[mname]['inputs'] = {}

    graph['button'] = {}
    graph['button']['type'] = 'button'
    graph['button']['connects'] = set(['broadcaster'])
    
    # add the input modules for each conjuction modules in a second pass
    # also deal with dummy modules
    dummy_modules = []
    for mname in graph:
        for c in graph[mname]['connects']:
            if graph.get(c, None) is not None:
                if graph[c]["type"] == "&":
                    graph[c]['inputs'][mname] = 0  # initially remember low
            else:
                dummy_modules.append(c)
    for c in dummy_modules:
        graph[c] = {}
        graph[c]['type'] = "dummy"

    return graph

def compare_graph_states(state1, state2):
    for s1, s2 in zip(state1, state2):
        if s1 != s2:
            return False
    return True

def save_graph_state(graph):
    state = []
    for mname in graph:
        if graph[mname]['type'] == "&":
            state.append(graph[mname]['inputs'])
        elif graph[mname]['type'] == "%":
            state.append(graph[mname]['state'])
    return state

# we will call 0 a low pulse, 1 a high pulse
def print_pulse(source, dest, pulse):
    p = "high" if pulse == 1 else "low"
    print(f"{source} -{p}-> {dest}")


def iopulse(graph, module, pulse, source, verbose=False):
    if verbose:
        print_pulse(source, module, pulse)
    reciever_modules = []   # here we will save the modules that receive a pulse,
                            # so we can send a pulse to them in the next iteration
                            # while maintaining the correct order. (we can't just)
                            # use recursion...
    if graph[module]['type'] == "%":  # flip-flop
        if pulse == 0:  # low pulse: we do something
            # give connected modules the inverse pulse
            for cmod in graph[module]['connects']:
                reciever_modules.append((cmod, 1 - graph[module]['state'], module))
            # and flip our own state
            graph[module]['state'] = 1 - graph[module]['state']
        else:  # high pulse: we ignore
            pass
            
    elif graph[module]['type'] == "&":  # conjunction 
        # first remember the pulse
        graph[module]['inputs'][source] = pulse
        # then check if all pulses are high
        if all(graph[module]['inputs'][cmod] == 1 for cmod in graph[module]['inputs']):
            # if so, send low pulse to all connected modules
            for cmod in graph[module]['connects']:
                reciever_modules.append((cmod, 0, module))
        else:
            # otherwise send high pulse to all connected modules
            for cmod in graph[module]['connects']:
                reciever_modules.append((cmod, 1, module))
    
    elif graph[module]['type'] == "broadcaster":  # broadcaster
        # send the same pulse to all connected modules
        for cmod in graph[module]['connects']:
            reciever_modules.append((cmod, pulse, module))

    elif graph[module]['type'] == "button":  # button
        # send low pulse to broadcaster
        reciever_modules.append(('broadcaster', 0, module))

    return graph, reciever_modules

def get_total_pulsecount(cycle, cyclecount, N):
    """cycle: number of pushes in a cycle
    cyclecount: number of pulses in a complete cycle
    N: total number of pushes to be done
    """
    return cyclecount * (N // cycle) + sum(range(N % cycle + 1))

def lcm(a, b, c, d):
    return np.lcm.reduce([a, b, c, d])

graph = read_graph("input.txt")
state_list = [save_graph_state(graph)]
steps = 0
lowpulsecount = 0
highpulsecount = 0
while True and steps < 1000:  # Their is no cycle < 1000 for q1.........
    steps+=1
    reciever_modules = [('broadcaster', 0, 'button')]  # dest, pulse, source
    while reciever_modules:
        new_reciever_modules = []
        for reciever_module in reciever_modules:
            lowpulsecount += 1 if reciever_module[1] == 0 else 0
            highpulsecount += 1 if reciever_module[1] == 1 else 0
            graph, temp_reciever_modules = iopulse(graph, *reciever_module,
                                                   verbose=False)
            new_reciever_modules.extend(temp_reciever_modules)
        reciever_modules = new_reciever_modules
    state = save_graph_state(graph)
    if any(compare_graph_states(state, s) for s in state_list):
        print("graph repeated after {} steps".format(steps))
        print("final counts: low: {}, high: {}".format(lowpulsecount, 
                                                       highpulsecount))
        state_list.append(state)
        break 
    else:
        state_list.append(state)

print("q1:", get_total_pulsecount(steps, lowpulsecount, 1000)*      get_total_pulsecount(steps, highpulsecount, 1000))

graph = read_graph("input.txt")
steps = 0
lsinputs = ['dd', 'tx', 'nz', 'ph']
lsinput_list = [[],[],[],[]] # these feed into ls which feeds into rx...
while True:
    steps+=1
    reciever_modules = [('broadcaster', 0, 'button')]  # dest, pulse, source
    while reciever_modules:
        new_reciever_modules = []
        for reciever_module in reciever_modules:
            if reciever_module[2] in lsinputs and reciever_module[1] == 1:
                lsinput_list[lsinputs.index(reciever_module[2])].append(steps)
            lowpulsecount += 1 if reciever_module[1] == 0 else 0
            highpulsecount += 1 if reciever_module[1] == 1 else 0
            graph, temp_reciever_modules = iopulse(graph, *reciever_module,
                                                   verbose=False)
            new_reciever_modules.extend(temp_reciever_modules)
        reciever_modules = new_reciever_modules
    if all(len(l) > 1 for l in lsinput_list):
        print("all inputs have had a cycle: {}".format(lsinput_list))
        break
print("q2:", lcm(*[el[1]- el[0] for el in lsinput_list]))

