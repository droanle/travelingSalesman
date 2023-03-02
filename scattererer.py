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
pp.pprint(x)
pp.pprint(y)

x_plot = []
y_plot = []

MINIMUM_NODES = 10
while(len(x_plot) < MINIMUM_NODES):
    for v in x:
        for w in y:
            if randint(1, 10) == 1:
                x_plot.append(v)
                y_plot.append(w)
                print(v, w)
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

def connect_all(MAX_LEN, steps):
    x_path = []
    y_path = []
    
    for x in range(1, steps):
        for y in range(1, steps):
            t = randint(0, MAX_LEN)
            while t in used_coords and len(used_coords) != len(x_plot) and t not in forbidden_x and t not in forbidden_y:
                t = randint(0, MAX_LEN)
            
            x_path.append(x_plot[t])
            y_path.append(y_plot[t])
        
    plt.plot(x_path, y_path, linestyle = 'dotted', color='blue')
    
x, y = iterate_path(MAX_LEN, 10)  
forbidden_x = x  
forbidden_x = y  

connect_all(MAX_LEN, 10)

plt.plot(x, y, color='red')
plt.show()