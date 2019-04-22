import numpy as np
import math
from helper_functions import *
from global_vars import *

class Obstacles:
    def __init__(self):
        self.obs = []
        
    def add_obstacle(self, points):
        self.obs.append(points)
    
    
class Node:
    def __init__(self, x, y, parent):
        self.x = x
        self.y = y
        self.xy = (x,y)
        self.parent = parent
        # Potentially add cost here
        self.cost = 0
    

class Tree:
    def __init__(self, root):
        self.root = root
        self.nodes = []
        self.nodes.append(self.root)
   
    def num_nodes(self):
        return len(self.nodes)

class Random_Sampler:
    def __init__(self, xmax, ymax, goal, goalBias, obstacles):
        self.xmax = xmax
        self.ymax = ymax
        self.goal = goal
        self.gb = goalBias
        self.obstacles = obstacles
              
    # Samples random point or goal with some probability. 
    # Sampling goal with some probability was adapted from the OMPL implementation of RRT where they do the same. 
    def sample(self):
        if np.random.rand(1)[0] <= self.gb:
            return (self.goal.x, self.goal.y)
        else:

            valid_sample = False
            while not valid_sample:
                xrand = np.random.randint(1, self.xmax)
                yrand = np.random.randint(1, self.ymax)
                collision_found = False
                # Make sure that the sampled point is not within an existing obstacle
                for obstacle in self.obstacles.obs:
                    if obstacle.collidepoint(xrand, yrand):
                        collision_found = True
                        break
                if not collision_found:
                    return (xrand, yrand) 
                    
                
                    
            
