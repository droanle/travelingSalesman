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

for v in x:
    for w in y:
        plt.scatter(v, w)
        
x_path = []
y_path = []

MAX_LEN = len(x)

for x in x:
    x_p = randint(1, MAX_LEN)
    y_p = randint(1, MAX_LEN)
    
    x_path.append(x_p)
    y_path.append(y_p)

plt.plot(x_path, y_path, linestyle = 'dotted')
plt.show()