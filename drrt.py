from structures import *
from helper_functions import *
from rrt_hf import *
from global_vars import *

#DRRT Algorithm

def drrt(screen, sampler, start, end, tree, obstacles):
    # Sample point in the Free Space
    point = sampler.sample()
    temp = Node(point[0], point[1], None)
    # Find nearest node to that sampled point
    nearest, dist = nearest_node(temp, tree)
    collision_detected = collision_detection(point, nearest.xy, obstacles)
    
    # Do collision detection on the point and resample if collision between point and nn exists
    while collision_detected:
        point = sampler.sample()
        temp = Node(point[0], point[1], None)
        nearest, dist = nearest_node(temp, tree)
        collision_detected = collision_detection(point, nearest.xy, obstacles)
    # Link the temp node to its expected parent and update its cost
    temp.parent = nearest
    temp.parent.children.add(temp)
    temp.cost = distance(temp, temp.parent) + temp.parent.cost
    update_nearest_nodes(temp, tree, obstacles)


    # Optimize the parent to be the nearest nbh that minimizes the total cost for the new node
    optimize_parent(temp, obstacles)
    tree.nodes.append(temp)

    # Get the branch, which is just the internal nodes from leaf -> root
    b = branch(temp, tree.root)

    # Optimize the internal nodes of the branch
    b_copy = optimize_branch(b, tree, obstacles)
    
    found_diff = False
    for i in range(len(b_copy)):
        if b_copy[i].xy != b[i].xy:
            print(b_copy[i].xy, b[i].xy)
    for i in range(len(b_copy)):
        if found_diff:
            break
        if b_copy[i].xy != b[i].xy:
            update_tree_costs(tree)
            found_diff = True
            
    # If the node is within the goal threshold draw the node and path back to start and end the simulation    
    if distance(temp, end) < 5:
        # print("I am here")
        end.parent = temp
        end.parent.children.add(end)
        end.cost = end.parent.cost + distance(end.parent,end)
        update_nearest_nodes(end, tree, obstacles)
        optimize_parent(end, obstacles)
        b = branch(end, tree.root)
        b_copy = optimize_branch(b, tree, obstacles)
        found_diff = False
        for i in range(len(b_copy)):
            if found_diff:
                break
            if b_copy[i].xy != b[i].xy:
                update_tree_costs(tree)
                found_diff = True
        print(end.cost)
        
        tree.nodes.append(end)
        #SOLUTION_FOUND = True
        draw_all_nodes(tree, screen)
        highlight_solution_with_collision_print(end, screen, obstacles)
        pygame.display.flip()
        return True, end.cost
    return False, end.cost