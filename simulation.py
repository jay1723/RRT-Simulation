# Jay Rao
import pygame
import numpy as np
import sys
import math

pygame.init()
winner_font = pygame.font.SysFont("Ubuntu", 30)
## Global Variables ##
SIZE = (800,600)
SOLUTION_FOUND = 0
WHITE = (255,255,255)
BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)
YELLOW = (255,255,0)
BLACK = (0,0,0)

START = (400, 300)
GOAL = (600, 200)
SAMPLE_GOAL_PROB = .05
######################

class Node:
    def __init__(self, x, y, parent):
        self.x = x
        self.y = y
        self.parent = parent
        # Potentially add cost here

class Tree:
    def __init__(self, root):
        self.root = root
        self.nodes = []
        self.nodes.append(self.root)
    
    def num_nodes(self):
        return len(self.nodes)

class Random_Sampler:
    def __init__(self, xmax, ymax, goal):
        self.xmax = xmax
        self.ymax = ymax
        self.goal = goal
        
    # Samples random point or goal with some probability. 
    # Sampling goal with some probability was adapted from the OMPL implementation of RRT where they do the same. 
    def sample(self):
        if np.random.rand(1)[0] <= SAMPLE_GOAL_PROB:
            return (goal.x, goal.y)
        else:
            xrand = np.random.rand(1)[0] * self.xmax
            yrand = np.random.rand(1)[0] * self.ymax
            return (math.floor(xrand), math.floor(yrand)) # If the goal is in the top right corner of the screen it will never be reached
        
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
def draw_node(node, screen, color=BLACK, linecolor=RED, size=1):
    circle = pygame.draw.circle(screen, color, (node.x, node.y), size, size)
    pygame.display.update(circle)
    if node.parent != None:
        pygame.draw.line(screen, linecolor, (node.x, node.y), (node.parent.x, node.parent.y))

# Starting from the last node, highlight the solution path from start -> end
def highlight_solution(final_node):
    current = final_node
    while current.parent != None:
        pygame.draw.line(screen, GREEN, (current.x, current.y), (current.parent.x, current.parent.y), 3)
        current = current.parent       



pygame.display.set_caption("Sampling Simulation")
screen = pygame.display.set_mode(SIZE)

screen.fill(WHITE)


# Define start and goal, draw the start node to the screen
root = Node(START[0], START[1], None)
end = Node(GOAL[0], GOAL[1], None)
draw_node(end, screen, color=GREEN, size=5)
draw_node(root, screen, color=BLUE, size=5)
tree = Tree(root)
sampler = Random_Sampler(SIZE[0], SIZE[1], end)

while not SOLUTION_FOUND:
    for event in pygame.event.get():
        if event.type == pygame.QUIT : sys.exit()
    
    point = sampler.sample()
    temp = Node(point[0], point[1], None)
    nearest = nearest_node(temp, tree)
    temp.parent = nearest
    tree.nodes.append(temp)
    draw_node(temp, screen)
    if distance(temp, end) < 5:
        end.parent = temp
        SOLUTION_FOUND = True
        draw_node(end, screen)
        tsrf = winner_font.render("END FOUND", False, (0,0,0))
        highlight_solution(end)
        screen.blit(tsrf,(0,0))
        pygame.display.flip()
        pygame.time.delay(20000)
        break
    else:
        pygame.display.flip()
        val+= 1
    
    



    
    
    
    
    
