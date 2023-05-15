# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 07:53:03 2023

@author: aluno
"""

from display import Display
from events import EventHandler
from components import *
import pygame
from pygame.locals import *

BLACK       = (0, 0, 0)
GRAY        = (40, 40, 40)
RED         = (255, 0, 0)
GREEN       = (0, 255, 0)
BLUE        = (0, 0, 255)
VIOLET      = (255, 0, 255)

HEIGHT          = 600
WIDTH           = 800
BORDER_WIDTH    = 5/2
BOUNDS          = (WIDTH, HEIGHT)
START           =  (0, 0)

pygame.init()
display = Display(WIDTH, HEIGHT)

screen  = display.surfaces['display']

event_handler = EventHandler(display)

display.add_surface('methods', pygame.Surface(BOUNDS, pygame.SRCALPHA))
display.add_surface('map', pygame.Surface(BOUNDS, pygame.SRCALPHA))
display.add_surface('init_solution', pygame.Surface(BOUNDS, pygame.SRCALPHA))


display.fill('methods', GRAY, 0, 0, WIDTH * 0.5 - BORDER_WIDTH, HEIGHT)
display.fill('map', GRAY, WIDTH * 0.5 + BORDER_WIDTH, 0, WIDTH * 0.5, HEIGHT * 0.75 - BORDER_WIDTH)
display.fill('init_solution', GRAY, WIDTH * 0.5 + BORDER_WIDTH, HEIGHT * 0.75 + BORDER_WIDTH, WIDTH * 0.5, HEIGHT * 0.25 - BORDER_WIDTH)


display.render_surface('methods')
display.render_surface('map')
display.render_surface('init_solution')
display.update()

while True:
    event_handler.update()
    
    display.tick(1000)

