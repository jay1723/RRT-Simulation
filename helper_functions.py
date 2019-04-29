from global_vars import *
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
    den = ((x2-x1) * (y4-y3)) - ((y2-y1)*(x4-x3))
    n1 =  ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3))
    n2 = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3))
    if den < 0:
        den = -den
        n1 = -n1
        n2 = -n2
    # Avoid the divide by 0 possibility    
    if 0.0 < n1 and n1 < den and 0.0 < n2 and n2 < den:
        A = n1 / den
        B = n2 / den
        iX = x1 + (A * (x2-x1))
        iY = y1 + (A * (y2-y1))
        return True, iX, iY
    return False, 100000, 100000 # Change these values to sys.maxsize if the size of board > 10^5
    
# Box line collision detection modified from http://www.jeffreythompson.org/collision-detection/line-rect.php
# Returns true if there is a collision between the line and the rectangle
def line_rect_collision(p1,p2, rect):
    x1,y1 = p1
    x2,y2= p2
    rx,ry = rect.topleft
    rw = rect.width
    rh = rect.height
    left, lx, ly = line_line_collision((x1,y1,x2,y2), (rx,ry,rx, ry+rh))
    right, rix, riy = line_line_collision((x1,y1,x2,y2), (rx+rw,ry, rx+rw,ry+rh))
    top, tx, ty = line_line_collision((x1,y1,x2,y2), (rx,ry, rx+rw,ry))
    bottom, bx, by = line_line_collision((x1,y1,x2,y2), (rx,ry+rh, rx+rw,ry+rh))
    if left or right or top or bottom:
        return True, (lx, ly), (rix, riy), (bx, by), (tx, ty)
        
    return False, (100000, 100000), (100000, 100000), (100000, 100000), (100000, 100000)

# Returns true if a collision is detected between line and any obstacle in the simulation
def collision_detection(p1, p2, obstacles):
    for obstacle in obstacles.obs:
        col = line_rect_collision(p1,p2, obstacle)
        if col[0]:
            return True
    return False
    
    
def round(point):
    return int(point + .5)
   
def draw_obstacles(screen, obstacles):
    for ob in obstacles.obs:
        pygame.draw.rect(screen, BLUE, ob)
        pygame.display.update()


# Euclidean distance
def distance(n1, n2):
    return math.sqrt((n1.x - n2.x)**2 + (n1.y - n2.y)**2)

def distance_point(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2) 
# Calculate the nearest neighbor by iterating through all of the nodes in the node list and checking for smallest Euclidean distance
def nearest_node(node, tree):
    nearest = tree.root
    dist = 0
    for neighbor in tree.nodes:
        neighbor_to_node = distance(neighbor,node)
        nearest_to_node = distance(nearest, node)
        if neighbor_to_node < nearest_to_node:
            nearest = neighbor
            dist = neighbor_to_node
    return nearest, dist

# Return midpoint of a line. Input is Tuples (x,y)
def midpoint(p1, p2):
    x1,y1 = p1
    x2,y2 = p2
    x1 = float(x1)
    x2 = float(x2)
    y1 = float(y1)
    y2 = float(y2)
    return (int(abs(x2 + x1) / 2),int(abs(y2 + y1) / 2))
    
# Draw the node to the screen and if the node has a parent, draw a line between the two
def draw_node(node, screen, color=BLACK, linecolor=RED, size=DOT_SIZE):
    circle = pygame.draw.circle(screen, color, (node.x, node.y), size, size)
    pygame.display.update(circle)
    if node.parent != None:
        pygame.draw.line(screen, linecolor, (node.x, node.y), (node.parent.x, node.parent.y))
    return circle
# Starting from the last node, highlight the solution path from start -> end
def highlight_solution(final_node, screen):
    current = final_node
    while current.parent != None:
        pygame.draw.line(screen, GREEN, (current.x, current.y), (current.parent.x, current.parent.y), 3)
        current = current.parent  
       

def draw_dot(point, screen):
    circle = pygame.draw.circle(screen, BLUE, (point[0], point[1]), 1, 1)
    pygame.display.update(circle)

def draw_polygon(points):
    pass
