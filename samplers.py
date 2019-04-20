import helper_functions
from structures import *
from helper_functions import *

# Rapidly Exploring Random Tree Algorithm
def rrt(screen, sampler, start, end, tree, obstacles):
    # Sample point in the Free Space
    point = sampler.sample()
    temp = Node(point[0], point[1], None)
    # Find nearest node to that sampled point
    nearest = nearest_node(temp, tree)
    collision_free = collision_detection(point, (nearest.x, nearest.y), obstacles)
    
    # Do collision detection on the point and resample if collision between point and nn exists
    while collision_free:
        print("collision detection loop")
        point = sampler.sample()
        temp = Node(point[0], point[1], None)
        nearest = nearest_node(temp, tree)
        collision_free = collision_detection(point, (nearest.x, nearest.y), obstacles)
    print("exited collision detection")
    # draw the node and connect it to the edge and add it to the tree
    temp.parent = nearest
    tree.nodes.append(temp)
    draw_node(temp, screen)
    
    # If the node is within the goal threshold draw the node and path back to start and end the simulation
    if distance(temp, end) < 5:
        end.parent = temp
        SOLUTION_FOUND = True
        draw_node(end, screen)
        highlight_solution(end, screen)
        pygame.display.flip()
        pygame.time.delay(20000) 
        return True
    return False
