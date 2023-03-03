import pygame
from pygame.locals import *
from datetime import datetime
import time



pygame.init()
width = 640
height = 480
screen = pygame.display.set_mode((width, height), 0, 24)
BLACK = (255, 255, 255)

class FPS:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Verdana", 20)
        self.text = self.font.render(str(self.clock.get_fps()), True, BLACK)
 
    def render(self, display, x, y, value = None):
        if value is not None:
            self.text = self.font.render(str(value), True, BLACK)
        else:
            self.text = self.font.render(str(round(self.clock.get_fps(),2)), True, BLACK)
        display.blit(self.text, (x, y))

            
 
fps = FPS()   

cycles = 0
run = True

max_frames = 125 # 25*5
current_frame = 1

	
clock = pygame.time.Clock()  

current_cycle = 0
coords = '0, 10'
nodes = []
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            current_cycle += 1
            coords = event.pos
            nodes.append(coords)
            print(nodes)
            
            
    screen.fill((0, 0, 0))
 
    fps.render(screen, 10, 10)
    fps.render(screen, width - 50, 10, current_cycle)
    fps.render(screen, round(width/2) - 50, 10, coords)
    
    for point in nodes:
        pygame.draw.circle(screen, (255, 0, 0), point, 5)
        for node in nodes:
            pygame.draw.line(screen, (128, 64, 255), point, node, 2)
    
    pygame.display.update()
    fps.clock.tick(30)
    