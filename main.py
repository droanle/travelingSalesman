from display import Display
from events import EventHandler
import pygame
from pygame.locals import *

BLACK       = (0, 0, 0)
GRAY        = (100, 100, 100)
RED         = (255, 0, 0)
GREEN       = (0, 255, 0)
BLUE        = (0, 0, 255)
VIOLET      = (255, 0, 255)

HEIGHT = 600
WIDTH = 800
BOUNDS = (WIDTH, HEIGHT)

pygame.init()
display = Display(WIDTH, HEIGHT)
display.add_surface('points',   pygame.Surface(BOUNDS, pygame.SRCALPHA))
display.add_surface('lines',    pygame.Surface(BOUNDS, pygame.SRCALPHA))


event_handler = EventHandler(display)
display.fill('display', GRAY, 0, 0, 800, 600)
display.render('display', 0, 0)
display.update()


ADD_NODE = 1

while True:
    event_handler.update()
    if(event_handler.proccess_events()):
        display.update()

    
    display.tick(60)