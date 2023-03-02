import matplotlib.pyplot as plt
import numpy as np
import pprint
from random import randint, shuffle

"""
Created on Thu Mar  2 07:36:56 2023

@author: aluno
"""

x = [n for n in range (1, 10)]
y = [n for n in range (1, 10)]

pp = pprint.PrettyPrinter(indent=4)
x_plot = []
y_plot = []

MINIMUM_NODES = 10
while(len(x_plot) < MINIMUM_NODES):
    for v in x:
        for w in y:
            if randint(1, 10) == 1:
                x_plot.append(v)
                y_plot.append(w)
                plt.scatter(v, w, color='gray')
        

used_coords = []
forbidden_x = []    
forbidden_y = []
MAX_LEN = len(x_plot) - 1

def iterate_path(MAX_LEN, steps):
    x_path = []
    y_path = []
    
    for x in range(1, steps):
        t = randint(0, MAX_LEN)
        while t in used_coords and len(used_coords) != len(x_plot):
            t = randint(0, MAX_LEN)
        
        x_path.append(x_plot[t])
        y_path.append(y_plot[t])
        
    return x_path, y_path
nodes = []
def connect_all(MAX_LEN, steps):
    x_path = []
    y_path = []
    
    for x in range(1, steps):
        found_values = []
        for y in range(1, steps):
            t = randint(0, MAX_LEN)
            while t in used_coords and len(used_coords) != len(x_plot) and t not in forbidden_x and t not in forbidden_y:
                t = randint(0, MAX_LEN)
            
            x_path.append(x_plot[t])
            y_path.append(y_plot[t])
            found_values.append({'x': x_plot[t], 'y': y_plot[t]})
        nodes.append(found_values)
        
    #plt.plot(x_path, y_path, linestyle = 'dotted', color='blue')
    
x, y = iterate_path(MAX_LEN, 10)  
forbidden_x = x  
forbidden_x = y  

connect_all(MAX_LEN, 10)


nodes2 = []
for w in range(len(nodes)):
    nodes2.append([])
    for z in range(len(nodes)):
        if(w == z):
            nodes2[w].append(0)
        else:
            if randint(0, 1) == 1:
                nodes2[w].append(1)
            else:
                nodes2[w].append(0)
        
pp.pprint(nodes2)
print(len(nodes), len(nodes2))
available_nodes = []
for t in range(len(nodes)):
    y_value = nodes2[t]
    for q in range(len(nodes)):
        x_value = y_value[q]
        if(x_value == 1):
            nodes2[t][q] = nodes[t][q]
            available_nodes.append(nodes[t][q])


xxx = []
yyy = []
for node in available_nodes:
    xxx.append(node['x'])
    yyy.append(node['y'])
    
size = len(available_nodes)
count = 0
while(size > 5):    
    for h in range(0, len(xxx)):
        index = randint(0, size)
        target = available_nodes[index]
        size -= 1
        print(target['x'])
        plt.arrow(xxx[h], yyy[h], target['x'] - xxx[h], target['y'] - yyy[h], color='red', head_width=0.25, head_length=0.5, head_starts_at_zero=False)
        plt.scatter(xxx[h], yyy[h], color='green')
        plt.scatter(target['x'], target['y'], color='blue')
        count += 1
        if count >= 1: break # change to increase arrows
    if count >= 1: break
        
plt.show()