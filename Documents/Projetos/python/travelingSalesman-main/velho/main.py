# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 07:53:03 2023

@author: aluno
"""

from display import Display
from events import EventHandler
from hillClimb import HillClimb
from components import *
import pygame
from pygame.locals import *

BLACK = (0, 0, 0)
GRAY = (40, 40, 40)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
VIOLET = (255, 0, 255)
WHITE = (255, 255, 255)

HEIGHT = 400
WIDTH = 800
BORDER_WIDTH = 4
BOUNDS = (WIDTH, HEIGHT)
START = (0, 0)

pygame.init()
display = Display(WIDTH, HEIGHT)
screen = display.surfaces['display']
font_25 = pygame.font.SysFont(None, 25)
font_35 = pygame.font.SysFont(None, 35)

event_handler = EventHandler(display)

# [10, 50][185, 50]
# [185, 75][10, 75]

# (  2,   4),         (  7,   4),
# (  2,   2),         (  7,   2)
# ( 10,  50),         (185,  50)
# ( 10,  75)          (185,  75)
# Blocks
display.add_surface('methods', pygame.Surface(BOUNDS, pygame.SRCALPHA), {
    "local": [0, 0],
    "width": "35%",
    "height": "100%",
    "fill-color": "GRAY"
})
display.add_surface(
    'map', pygame.Surface(BOUNDS, pygame.SRCALPHA), {
        "x-local": ["right", "methods"],
        "y-local": 0,
        "width": "65%",
        "height": "75%",
        "border": str(BORDER_WIDTH) + "size",
        "fill-color": "GRAY"
    })
display.add_surface(
    'init_solution', pygame.Surface(BOUNDS, pygame.SRCALPHA), {
        "x-local": ["right", "methods"],
        "y-local": ["bottom", "map"],
        "width": "65%",
        "height": "25%",
        "border": str(BORDER_WIDTH) + "size",
        "fill-color": "GRAY"
    })

mapStruture = display.strutures.get('map')

event_handler.add_subscribe(
    1,
    HillClimb("Subida de encosta", display, mapStruture['local'],
              [mapStruture['height'], mapStruture['width']], BORDER_WIDTH,
              RED), {
                  "init": [10, 50],
                  "form": [175, 25]
              })

# Texts
display.add_surface(
    'txt_sud-de-encost',
    pygame.font.SysFont(None, 25).render(' ▣ Subida de encosta', True, GREEN))
display.add_surface(
    'txt_metodo',
    pygame.font.SysFont(None, 35).render('Métodos', True, GREEN))
display.add_surface(
    'txt_sud-de-encost-alter',
    pygame.font.SysFont(None, 25).render('Subida de encosta alterado', True,
                                         GREEN))
display.add_surface(
    'txt_tentativa',
    pygame.font.SysFont(None, 23).render(' -- Tentativa', True, GREEN))

# Fill Blocks
display.fill('methods')
display.fill('map')
display.fill('init_solution')

# Render Surface
display.render_surface('methods')
display.render_surface('map')
display.render_surface('init_solution')

display.render_surface('txt_metodo', (BORDER_WIDTH * 3, BORDER_WIDTH * 4))
display.render_surface(
    'txt_sud-de-encost',
    (BORDER_WIDTH * 3, (BORDER_WIDTH * 4) + 35),
)

# display.render_surface('txt_sud-de-encost-alter',
#                        (BORDER_WIDTH * 3, ((BORDER_WIDTH * 4) + 28 * 2)))

# display.render_surface('txt_tentativa', (((BORDER_WIDTH * 3) + 5),
#                                          ((BORDER_WIDTH * 4) + 25 * 3)))

# Update Display
display.update()

while True:
    event_handler.update()

    display.tick(1000)
