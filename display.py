import pygame
from pygame.locals import *

class Display:
    surfaces = {}
    components = {}
    average_fps = [0]
    
    
    def __init__(self, width, height):
        self.width  = width
        self.height = height
        self.display = pygame.display.set_mode((width, height))
        self.surfaces['display']  = self.display
        
        self.clock  = pygame.time.Clock()

        
    def render(self, surface, component):
        x = component.get_x()
        y = component.get_x()
        self.surfaces[surface].blit(component.component, (x, y))
        pygame.display.update()
        
    def render_surface(self, surface):

        self.display.blit(self.surfaces[surface], (0, 0))
        pygame.display.update()
        
    def fill(self, surface, color, x = 0, y = 0, width = None, height = None):
        self.surfaces[surface].fill(color, (x, y, width, height))
        
    def update(self, surface = None):
        if surface is not None:
            self.render_surface(surface)
                
        for component in self.components:
            surface = self.components[component]['surface']
            element = self.components[component]['component']
            self.render(surface, element)
        
        
    def tick(self, fps):
        self.average_fps.append(self.clock.get_fps())
        if(len(self.average_fps) > 60 * 10):
            self.average_fps.pop(0)
        self.clock.tick(fps)
        
    def get_fps(self):
        average_fps = sum(self.average_fps) / len(self.average_fps)
        return average_fps
        
    def add_surface(self, name, surface):
        self.surfaces[name] = surface
    
    def add_component(self, name, component, surface = 'components'):
        self.render(surface, component)
        self.components[name] = {'component': component, 'surface': surface}
        
    def update_component(self, name, component):
        self.components[name]['component'] = component
        self.render(self.components[name]['surface'], component)
        self.render_surface(self.components[name]['surface'])
        
    
    
        