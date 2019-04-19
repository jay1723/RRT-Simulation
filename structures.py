import numpy as np
import math

class Obstacles:
    def __init__(self):
        self.obstacles = []
        
    def add_obstacle(self, points):
        self.obstacles.append(points)
    
    
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
    def __init__(self, xmax, ymax, goal, goalBias):
        self.xmax = xmax
        self.ymax = ymax
        self.goal = goal
        self.gb = goalBias
              
    # Samples random point or goal with some probability. 
    # Sampling goal with some probability was adapted from the OMPL implementation of RRT where they do the same. 
    def sample(self):
        if np.random.rand(1)[0] <= self.gb:
            return (self.goal.x, self.goal.y)
        else:
            xrand = np.random.rand(1)[0] * self.xmax
            yrand = np.random.rand(1)[0] * self.ymax
            return (math.floor(xrand), math.floor(yrand)) # If the goal is in the top right corner of the screen it will never be reached
