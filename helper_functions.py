import global_vars as gv
import pygame
import math

pygame.init()

# Check whether a given sampled point, or edge connect node -> parent is in collision with obstacle. 
# Modified from http://www.jeffreythompson.org/collision-detection/line-line.php
# l1 = (x1, y1, x2, y2) same for l2
def line_line_collision(l1, l2):
    x1,y1,x2,y2 = l1
    x3,y3,x4,y4 = l2
    x1 = float(x1)
    y1 = float(y1)
    x2 = float(x2)
    y2 = float(y2)
    x3 = float(x3)
    y3 = float(y3)
    x4 = float(x4)
    y4 = float(y4)
    #print(x3,y3, x4,y4)
    denominator = ((x2-x1) * (y4-y3)) - ((y2-y1)*(x4-x3))
    numerator1 =  ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3))
    numerator2 = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3))
    if denominator == 0:
        return (numerator1 == 0) and (numerator2 == 0)
    A = numerator1 / denominator
    B = numerator2 / denominator
    
    if A >= 0 and A <= 1 and B >= 0 and B <= 1:
        return True
    return False
    
# Box line collision detection modified from http://www.jeffreythompson.org/collision-detection/line-rect.php
def collision_detection(p1, p2, obstacles):
    x1,y1 = p1
    x2,y2= p2
    for obstacle in obstacles.obs:
        rx,ry = obstacle.topleft
        rw = obstacle.width
        rh = obstacle.height
        left = line_line_collision((x1,y1,x2,y2), (rx,ry,rx, ry+rh))
        right = line_line_collision((x1,y1,x2,y2), (rx+rw,ry, rx+rw,ry+rh))
        top = line_line_collision((x1,y1,x2,y2), (rx,ry, rx+rw,ry))
        bottom = line_line_collision((x1,y1,x2,y2), (rx,ry+rh, rx+rw,ry+rh))
        if left or right or top or bottom:
            return True
    return False

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
    return circle
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
