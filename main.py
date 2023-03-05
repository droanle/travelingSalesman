from display import Display
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
display = Display(WIDTH, HEIGHT)
screen  = display.surfaces['display']
event_handler = EventHandler(display)

display.add_surface('points',   pygame.Surface(BOUNDS, pygame.SRCALPHA))
display.add_surface('lines',    pygame.Surface(BOUNDS, pygame.SRCALPHA))
display.add_surface('components', pygame.Surface(BOUNDS, pygame.SRCALPHA))

display.fill('components', GRAY, 0, 0, WIDTH, HEIGHT/5)

fps = TextComponent(0, START)
display.add_component('fps', fps)
display.render_surface('components')
display.update()


ADD_NODE = 1

while True:
    event_handler.update()
    if(event_handler.proccess_events()):
        print(event_handler.get_events())
    print(display.get_fps())
    # display.render_surfaces('clean_components')
    fps.set_text(str(round(display.get_fps(), 2)) + ' fps')
    
    display.fill('components', GRAY, fps.get_x(), fps.get_x(), fps.get_width() + 5, fps.get_height())
    display.update_component('fps', fps)
    display.update('components')
    display.tick(100000)