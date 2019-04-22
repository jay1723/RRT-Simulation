from structures import *
from helper_functions import *

# Rapidly Exploring Random Tree Algorithm
def rrt_one_side(screen, sampler, start, end, tree, obstacles):
    # Sample point in the Free Space
    point = sampler.sample()
    temp = Node(point[0], point[1], None)
    # Find nearest node to that sampled point
    nearest, dist = nearest_node(temp, tree)
    collision_free = collision_detection(point, (nearest.x, nearest.y), obstacles)
    
    # Do collision detection on the point and resample if collision between point and nn exists
    while collision_free:
        #print("collision detection loop")
        point = sampler.sample()
        temp = Node(point[0], point[1], None)
        nearest, dist = nearest_node(temp, tree)
        collision_free = collision_detection(point, (nearest.x, nearest.y), obstacles)
    #print("exited collision detection")
    # draw the node and connect it to the edge and add it to the tree
    temp.parent = nearest
    temp.cost = dist + temp.parent.cost
    tree.nodes.append(temp)
    draw_node(temp, screen)
    
    # If the node is within the goal threshold draw the node and path back to start and end the simulation
    if distance(temp, end) < 5:
        end.parent = temp
        end.cost = temp.cost + distance(temp,end)
        SOLUTION_FOUND = True
        draw_node(end, screen)
        highlight_solution(end, screen)
        pygame.display.flip()
        return True, end.cost
    return False, end.cost
