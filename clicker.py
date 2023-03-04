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
        self.average_fps = []
 
    def render(self, display, x, y, value = None):
        if value is not None:
            self.text = self.font.render(str(value), True, BLACK)
        else:
            self.average_fps.append(self.clock.get_fps())
            if(len(self.average_fps) > 60 * 10):
                self.average_fps.pop(0)
            average_fps = sum(self.average_fps) / len(self.average_fps)
            self.text = self.font.render(str(round(average_fps,2)), True, BLACK)
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

font = pygame.font.SysFont(None, 18)

info_string = 'Left mouse creates a node. Right mouse toggles connections. Middle mouse (scroll click) resets.'
info_string2 = "S toggles everything, but doesn't delete any nodes."
    
img = font.render(info_string, True, (255, 255, 255))
img2 = font.render(info_string2, True, (255, 255, 255))
    
render_connections = True
show_elements = True

points_surface = pygame.Surface((640, 480), pygame.SRCALPHA)
lines_surface = pygame.Surface((640, 480), pygame.SRCALPHA)


def render_point(coords):
    pygame.draw.circle(points_surface, (255, 0, 0), coords, 5)
    
def render_line(coords):
    for node in nodes:
        pygame.draw.line(lines_surface, (128, 64, 255), coords, node, 1)
        
last_frames = []
has_anything_changed = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            coords = event.pos
            mouse_button = event.button
            if mouse_button == 1:
                if coords not in nodes:
                    nodes.append(coords)
                    render_point(coords)
                    render_line(coords)
            elif mouse_button == 2:
                nodes = []
                points_surface.fill((0, 0, 0, 0))
                lines_surface.fill((0, 0, 0, 0))
                coords = '(0, 0)'
            elif mouse_button == 3:
                current_cycle += 1
                render_connections = not render_connections
            has_anything_changed = True
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                show_elements = not show_elements
            has_anything_changed = True
            
    if has_anything_changed: 
        screen.fill((0, 0, 0))
    
        if show_elements:
            if render_connections: screen.blit(lines_surface, (0, 0))
            screen.blit(points_surface, (0, 0))
        
        total_nodes = len(nodes)
        connections     =   ((total_nodes * (total_nodes - 1))/2)
        concordance     = ' node, ' if total_nodes == 1 else ' nodes, '
        concordance2    = ' connection ' if connections == 1 else ' connections '
    
        fps.render(screen, 220, 10, str(total_nodes) + concordance + str(round(connections)) + concordance2)
        fps.render(screen, 100, 10, coords)
        
        screen.blit(img, (10, 40))
        screen.blit(img2, (10, 60))


        
    has_anything_changed = False
    
    screen.fill((0, 0, 0), (0, 0, 100, 33))
    fps.render(screen, 10, 10)
    pygame.display.update()
    fps.clock.tick(10000)
    