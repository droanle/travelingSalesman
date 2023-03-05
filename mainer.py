from events import EventHandler
from components import *
import pygame
from pygame.locals import *

BLACK       = (0, 0, 0)
GRAY        = (100, 100, 100)
RED         = (255, 0, 0)
GREEN       = (0, 255, 0)
BLUE        = (0, 0, 255)
VIOLET      = (255, 0, 255)

HEIGHT  = 600
WIDTH   = 800
BOUNDS  = (WIDTH, HEIGHT)
START   =  (0, 0)

pygame.init()
display = pygame.display.set_mode(BOUNDS)
event_handler = EventHandler(display)

fps = TextComponent(0, START)
display.blit(fps.component, (0, 0))
pygame.display.update()
ADD_NODE = 1
average_fps = [0]
clock = pygame.time.Clock()
while True:
    event_handler.update()
    if(event_handler.proccess_events()):
        print(event_handler.get_events())
    average_fps.append(clock.get_fps())
    if(len(average_fps) > 60):
        average_fps.pop(0)
    fps.set_text(str(round(sum(average_fps)/len(average_fps), 2)) + ' fps')
    display.fill(BLACK, fps.get_bounds(10))
    display.blit(fps.component, (0, 0))
    pygame.display.update()
    clock.tick(10000)
        
    