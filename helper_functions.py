import global_vars as gv
import pygame
import math

pygame.init()

# Check whether a given sampled point, or edge connect node -> parent is in collision with obstacle. 
def collision_detection(point, obstacles):
    #pygame.draw.rect(screen, BLUE, (200, 200, 150, 50))
    #points = [[100,140],[200,220],[310,250],[400,450]]
    #pygame.draw.polygon(screen, BLUE, points)
    pass

# If the distance between a sampled point and its nearest neighbor is too large, linearly interpolate to calculate the best point
def linear_interpolate(n1, n2, maxDistance):
    pass


# Euclidean distance
def distance(n1, n2):
    return math.sqrt((n1.x - n2.x)**2 + (n1.y - n2.y)**2)
    
# Calculate the nearest neighbor by iterating through all of the nodes in the node list and checking for smallest Euclidean distance
def nearest_node(node, tree):
    nearest = tree.root
    for neighbor in tree.nodes:
        if distance(neighbor, node) < distance(nearest, node):
            nearest = neighbor
    return nearest

# Draw the node to the screen and if the node has a parent, draw a line between the two
def draw_node(node, screen, color=gv.BLACK, linecolor=gv.RED, size=1):
    circle = pygame.draw.circle(screen, color, (node.x, node.y), size, size)
    pygame.display.update(circle)
    if node.parent != None:
        pygame.draw.line(screen, linecolor, (node.x, node.y), (node.parent.x, node.parent.y))

# Starting from the last node, highlight the solution path from start -> end
def highlight_solution(final_node, screen):
    current = final_node
    while current.parent != None:
        pygame.draw.line(screen, gv.GREEN, (current.x, current.y), (current.parent.x, current.parent.y), 3)
        current = current.parent       

def draw_dot(point, screen):
    circle = pygame.draw.circle(screen, gv.BLUE, (point[0], point[1]), 1, 1)
    pygame.display.update(circle)

def draw_polygon(points):
    pass
