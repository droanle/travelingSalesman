import pygame
from pygame.locals import *
from surfaceStruture import SurfaceStruture


class Display:
    surfaces = {}
    components = {}

    average_fps = [0]

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.display = pygame.display.set_mode((width, height))
        self.surfaces['display'] = self.display

        self.strutures = SurfaceStruture(width, height)

        self.clock = pygame.time.Clock()

    def render(self, surface, component):
        x = component.get_x()
        y = component.get_x()
        self.surfaces[surface].blit(component.component, (x, y))
        pygame.display.update()

    def render_surface(self, surface, point=(0, 0)):
        self.display.blit(self.surfaces[surface], point)
        pygame.display.update()

    def fill(self,
             surface,
             color=None,
             x=None,
             y=None,
             width=None,
             height=None):
        struture = self.strutures.get(surface)

        if not struture == False:
            color = struture["fillColor"]
            x = struture["local"][0]
            y = struture["local"][1]
            width = struture["width"]
            height = struture["height"]

        self.surfaces[surface].fill(color, (x, y, width, height))

    def update(self, surface=None):
        if surface is not None:
            self.render_surface(surface)

        for component in self.components:
            surface = self.components[component]['surface']
            element = self.components[component]['component']
            self.render(surface, element)

    def tick(self, fps):
        self.average_fps.append(self.clock.get_fps())
        if (len(self.average_fps) > 60 * 10):
            self.average_fps.pop(0)
        self.clock.tick(fps)

    def get_fps(self):
        average_fps = sum(self.average_fps) / len(self.average_fps)
        return average_fps

    def add_surface(self, name, surface, surfaceDisplayConfg=None):
        if surfaceDisplayConfg != None:
            self.strutures.add_struture(name, surfaceDisplayConfg)

        self.surfaces[name] = surface

    def add_component(self, name, component, surface='components'):
        self.render(surface, component)
        self.components[name] = {'component': component, 'surface': surface}

    def update_component(self, name, component):
        self.components[name]['component'] = component
        self.render(self.components[name]['surface'], component)
        self.render_surface(self.components[name]['surface'])

    def strutures(self):
        return self.strutures
