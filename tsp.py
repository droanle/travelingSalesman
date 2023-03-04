import itertools
import math
import pygame

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Define the list of nodes as a list of (x, y) coordinate tuples
nodes = [(100, 100), (200, 100), (200, 200), (100, 200), (300, 300), (400, 300), (400, 400), (300, 400)]

# Compute the distances between all pairs of nodes
distances = {}
for node1, node2 in itertools.combinations(nodes, 2):
    dist = math.sqrt((node1[0] - node2[0])**2 + (node1[1] - node2[1])**2)
    distances[(node1, node2)] = dist
    distances[(node2, node1)] = dist

# Find the shortest path using brute-force search
shortest_path = None
shortest_distance = float('inf')
for path in itertools.permutations(nodes):
    distance = sum(distances[(path[i], path[i+1])] for i in range(len(nodes)-1))
    if distance < shortest_distance:
        shortest_distance = distance
        shortest_path = path

# Draw the nodes and the shortest path
font = pygame.font.Font(None, 36)
for i, node in enumerate(nodes):
    pygame.draw.circle(screen, WHITE, node, 10)
    label = font.render(str(i), True, BLACK)
    label_rect = label.get_rect(center=node)
    screen.blit(label, label_rect)
for i in range(len(shortest_path)-1):
    pygame.draw.line(screen, RED, shortest_path[i], shortest_path[i+1], 3)

# Update the display
pygame.display.flip()

# Wait for the user to close the window
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    clock.tick(60)
