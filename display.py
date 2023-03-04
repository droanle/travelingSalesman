import pygame
from pygame.locals import *

class Display:
    surfaces = {}
    
    def __init__(self, width, height):
        self.width  = width
        self.height = height
        display = pygame.display.set_mode((width, height))
        self.surfaces['display']  = display
        
        self.font   = pygame.font.SysFont('Arial', 18)
        self.clock  = pygame.time.Clock()

        
    def render(self, surface, x, y):
        self.surfaces['display'].blit(self.surfaces[surface], (x, y))
        pygame.display.update()
        
    def fill(self, surface, color, x = 0, y = 0, width = None, height = None):
        self.surfaces[surface].fill(color, (x, y, width, height))
        
    def update(self):
        for surface in self.surfaces:
            if surface == 'display':
                continue
            self.render(surface, 0, 0)
        #pygame.display.update()
        
    def tick(self, fps):
        self.clock.tick(fps)
        
    def add_surface(self, name, surface):
        self.surfaces[name] = surface
        
    
    
        