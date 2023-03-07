import pygame
from pygame.locals import *
from datetime import datetime
import itertools
import math
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
info_string3 = "N runs a Nearest Neighbour solver. T brute forces the search."
    
img = font.render(info_string, True, (255, 255, 255))
img2 = font.render(info_string2, True, (255, 255, 255))
img3 = font.render(info_string3, True, (255, 255, 255))
    
render_connections = True
show_elements = True

points_surface = pygame.Surface((640, 480), pygame.SRCALPHA)
lines_surface = pygame.Surface((640, 480), pygame.SRCALPHA)


def render_point(coords):
    pygame.draw.circle(points_surface, (255, 0, 0), coords, 5)
    
def render_line(coords):
    for node in nodes:
        pygame.draw.line(lines_surface, (128, 64, 255), coords, node, 2)
        

tsp_timed_out = False
tsp_limit = 15
def travelling_salesman():
    distances = {}
    for node1, node2 in itertools.combinations(nodes, 2):
        dist = math.sqrt((node1[0] - node2[0])**2 + (node1[1] - node2[1])**2)
        distances[(node1, node2)] = dist
        distances[(node2, node1)] = dist
    return distances
        
last_frames = []
has_anything_changed = True
tsp_ran = False
clean_lines = True
solver = ''
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
                    clean_lines = True
 
                    if clean_lines: 
                        lines_surface.fill((0, 0, 0, 0))
                        for node in nodes:
                            render_line(node)
                    else:
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
            clean_lines = False
            tsp_ran = False
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                show_elements = not show_elements
            if event.key == pygame.K_n:    
                solver = 'N'
                tsp_ran = True
                show_elements = True
                render_connections = True
            if event.key == pygame.K_t:
                solver = 'T'
                tsp_ran = True
                show_elements = True
                render_connections = True
            has_anything_changed = True
            
    if has_anything_changed: 
        screen.fill((0, 0, 0))
    
        if show_elements:
            if render_connections: screen.blit(lines_surface, (0, 0))
            screen.blit(points_surface, (0, 0))
            
            if tsp_ran:
                if solver == 'T':
                    exit_tsp = False
                    start_time = time.time()
                    distances = travelling_salesman()
                    
                    shortest_path = None
                    shortest_distance = float('inf')
                    first_distance = 0
                    times = 0
                    for path in itertools.permutations(nodes):
                        times += 1
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.display.quit()
                                pygame.quit()
                                run = False
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_t:
                                    exit_tsp = True
                        if exit_tsp:
                            break
                        distance = sum(distances[(path[i], path[i+1])] for i in range(len(nodes)-1))
                        if shortest_distance > 0 and first_distance == 0:
                            first_distance = distance
                        if distance < shortest_distance:
                            shortest_distance = distance
                            shortest_path = path
                            

                            
                        current_time = time.time()
                        ran = current_time - start_time
                        screen.fill((0, 0, 0), (0, 80, width, 25))
                        screen.fill((128, 128, 128), (0, 102, width, 25))
                        fps.render(screen, 0, 102, 'TSP runtime: ' + str(round(ran, 4)) + 's')
                        screen.fill((128, 128, 128), (0, 122, width, 25))
                        fps.render(screen, 0, 122, 'Initial distance: ' + str(round(first_distance, 4)))
                        
                        screen.fill((0, 0, 0), (0, 0, width, 80))
                        total_nodes = len(nodes)
                        connections     =   ((total_nodes * (total_nodes - 1))/2)
                        concordance     = ' node, ' if total_nodes == 1 else ' nodes, '
                        concordance2    = ' connection ' if connections == 1 else ' connections '
                    
                        fps.render(screen, 220, 10, str(total_nodes) + concordance + str(round(connections)) + concordance2)
                        fps.render(screen, 100, 10, coords)
                        
                        fps.render(screen, 10, 10)
                        
                        screen.blit(img, (10, 40))
                        screen.blit(img2, (10, 60))
                        screen.blit(img3, (10, 80))
                        
                        fps.render(screen, width/2, 102, 'Searched paths ' + str(times) + ' times.')
                        fps.render(screen, width/2, 122, 'Distance: ' + str(round(shortest_distance, 4)))
                        if(ran > tsp_limit):
                            tsp_timed_out = True
                            break
                        
                        lines_surface.fill((0, 0, 0, 0))
                        for node in nodes:
                            render_line(node)
                        if(len(shortest_path) > 1):
                            for i in range(len(shortest_path)-1):
                                pygame.draw.line(lines_surface, (32, 32, 255), shortest_path[i], shortest_path[i+1], 2)
                    
                        screen.blit(lines_surface, (0, 0))
                        for node in range(len(nodes)):
                            x = nodes[node][0]
                            y = nodes[node][1]
                            fps.render(screen, x, y, node)
                        pygame.display.update()
                    if tsp_timed_out or exit_tsp:
                        screen.fill((128, 128, 128), (0, 122, width, 25))
                        fps.render(screen, 0, 122, 'TSP: forced exit with best path as ' + str(round(shortest_distance, 4)))
                        tsp_timed_out = False
                    else:
                        screen.fill((128, 128, 128), (0, 122, width, 25))
                        fps.render(screen, 0, 122, 'TSP: Best path found: ' + str(round(shortest_distance, 4)))
                        tsp_timed_out = False
                if solver == 'N':
                    exit_tsp = False
                    start_time = time.time()
                    distances = travelling_salesman()
                    
                    unvisited_nodes = set(nodes)
                    current_node = nodes[0]
                    shortest_path = [current_node]
                    shortest_distance = 0
                    unvisited_nodes.remove(current_node)
    
                    first_distance = 0
                    times = 0
                    
                    while unvisited_nodes:
                        times += 1
                        nearest_neighbor = min(unvisited_nodes, key=lambda node: distances[(current_node, node)])
                        shortest_path.append(nearest_neighbor)
                        shortest_distance += distances[(current_node, nearest_neighbor)]
                        unvisited_nodes.remove(nearest_neighbor)
                        current_node = nearest_neighbor
    
                        if times == 1:
                            first_distance = shortest_distance
    
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.display.quit()
                                pygame.quit()
                                run = False
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_t:
                                    exit_tsp = True
                        if exit_tsp:
                            break
                            
                        current_time = time.time()
                        ran = current_time - start_time
                        
                        screen.fill((0, 0, 0), (0, 80, width, 25))
                        screen.fill((128, 128, 128), (0, 102, width, 25))
                        fps.render(screen, 0, 102, 'TSP runtime: ' + str(round(ran, 4)) + 's')
                        screen.fill((128, 128, 128), (0, 122, width, 25))
                        fps.render(screen, 0, 122, 'Initial distance: ' + str(round(first_distance, 4)))
                        
                        screen.fill((0, 0, 0), (0, 0, width, 80))
                        total_nodes = len(nodes)
                        connections     =   ((total_nodes * (total_nodes - 1))/2)
                        concordance     = ' node, ' if total_nodes == 1 else ' nodes, '
                        concordance2    = ' connection ' if connections == 1 else ' connections '
                    
                        fps.render(screen, 220, 10, str(total_nodes) + concordance + str(round(connections)) + concordance2)
                        fps.render(screen, 100, 10, coords)
                        
                        fps.render(screen, 10, 10)
                        
                        screen.blit(img, (10, 40))
                        screen.blit(img2, (10, 60))
                        screen.blit(img3, (10, 80))
                        
                        fps.render(screen, width/2, 102, 'Searched paths ' + str(times) + ' times.')
                        fps.render(screen, width/2, 122, 'Distance: ' + str(round(shortest_distance, 4)))
                        if(ran > tsp_limit):
                            tsp_timed_out = True
                            break
                        
                        lines_surface.fill((0, 0, 0, 0))
                        for node in nodes:
                            render_line(node)
                        if(len(shortest_path) > 1):
                            for i in range(len(shortest_path)-1):
                                pygame.draw.line(lines_surface, (32, 32, 255), shortest_path[i], shortest_path[i+1], 2)
    
                        screen.blit(lines_surface, (0, 0))
                        for node in range(len(nodes)):
                            x = nodes[node][0]
                            y = nodes[node][1]
                            fps.render(screen, x, y, node)
                        pygame.display.update()
                    shortest_distance += distances[(shortest_path[-1], shortest_path[0])]
                    if tsp_timed_out or exit_tsp:
                        screen.fill((128, 128, 128), (0, 122, width, 25))
                        fps.render(screen, 0, 122, 'TSP: forced exit with best path as ' + str(round(shortest_distance, 4)))
                        tsp_timed_out = False
                    else:
                        screen.fill((128, 128, 128), (0, 122, width, 25))
                        fps.render(screen, 0, 122, 'TSP: Best path found: ' + str(round(shortest_distance, 4)))
                        tsp_timed_out = False
                            
        
        total_nodes = len(nodes)
        connections     =   ((total_nodes * (total_nodes - 1))/2)
        concordance     = ' node, ' if total_nodes == 1 else ' nodes, '
        concordance2    = ' connection ' if connections == 1 else ' connections '
    
        fps.render(screen, 220, 10, str(total_nodes) + concordance + str(round(connections)) + concordance2)
        fps.render(screen, 100, 10, coords)
        
        for node in range(len(nodes)):
            x = nodes[node][0]
            y = nodes[node][1]
            fps.render(screen, x, y, node)
        
        screen.blit(img, (10, 40))
        screen.blit(img2, (10, 60))
        screen.blit(img3, (10, 80))

    has_anything_changed = False
    
    screen.fill((0, 0, 0), (0, 0, 100, 33))
    fps.render(screen, 10, 10)

    pygame.display.update()
    fps.clock.tick(10000)
    