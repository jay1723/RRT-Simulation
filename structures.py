import numpy as np
import math
from helper_functions import *
from global_vars import *

class Obstacles:
    def __init__(self):
        self.obs = []
        
    def add_obstacle(self, points):
        self.obs.append(points)
    
    def clear(self):
       del self.obs[:]
    

# From paper: x_n = (x,y), parent, list of children, cost from start to n, list of nearest neighbors
class Node:
    def __init__(self, x, y, parent):
        self.x = x
        self.y = y
        self.xy = (x,y)
        self.parent = parent
        self.children = set()
        self.nearest = set()
        self.cost = 0
        
    def get_descendents(self):
        if len(self.children) == 0:
            return [self]
        else:
            out = []
            for node in self.children:
                out += [node] + get_descendents(node)
        return out

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
        self.sampled_points = set()
        self.count = 0
    
    def clear(self):
        self.sampled_points.clear()
        self.count = 0
        self.gb = SAMPLE_GOAL_PROB
        
          
    # Samples random point or goal with some probability. 
    def sample(self):
        # As more nodes are added, make sure to increase the goal bias
        if self.count == 1000:
            self.gb += .005
            self.count = 0
            print(self.gb)
        if np.random.rand(1)[0] <= self.gb:
            self.sampled_points.add((self.goal.x, self.goal.y))
            return (self.goal.x, self.goal.y)
        else:
            while True:
                xrand = np.random.randint(1, self.xmax)
                yrand = np.random.randint(1, self.ymax)
                if (xrand, yrand) in self.sampled_points:
                    continue
                collision_found = False
                # Make sure that the sampled point is not within an existing obstacle
                for obstacle in self.obstacles.obs:
                    if obstacle.collidepoint(xrand, yrand):
                        collision_found = True
                        break
                if not collision_found:
                    self.sampled_points.add((xrand, yrand))
                    self.count += 1
                    
                    return (xrand, yrand) 
                    
                
                    
            
