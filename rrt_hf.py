from helper_functions import *
from global_vars import *
from structures import *

# Given an obstacle check for a collision and return the point on the nearest edge in which that collision occurs. 
def nearest_edge_collision(point, nearest, rect):
    col, (lx, ly), (rix, riy), (bx, by), (tx, ty) = line_rect_collision(point, nearest, rect)
    ldist = distance_point((lx, ly), (nearest[0], nearest[1]))
    rdist = distance_point((rix, riy), (nearest[0], nearest[1]))
    tdist = distance_point((tx, ty), (nearest[0], nearest[1]))
    bdist = distance_point((bx, by), (nearest[0], nearest[1]))
    mindist = min(ldist, rdist, bdist, tdist)
    if mindist == ldist:
        return (round(lx), round(ly))
    elif mindist == rdist:
        return (round(rix), round(riy))
    elif mindist == tdist:
        return (round(tx), round(ty))
    elif mindist == bdist:
        return (round(bx), round(by))
        

# Returns the point of collision on the first obstacle in collision with the line segment between point and nearest
def get_nearest_obstacle_collision(point, nearest, obstacles):
    nst = (100000,100000)
    print(len(obstacles))
    for obstacle in obstacles.obs:
        iX, iY = nearest_edge_collision(point, nearest, obstacle)
        
        if distance_point((iX, iY), point) < distance_point(nearest, point):
            nst = (iX, iY)
            
    if nst[0] == 100000 and nst[1] == 100000 or len(obstacles.obs) == 0:
        return False, (-1, -1)
    return True, nst
 
    
# Returns branch of internal nodes that does not include the root node or the leaf node
def branch(node, root):
    if node.parent == root:
        return []
    # node = node.parent / Uncomment to remove the leaf node from branch
    tmp = []
    while node.parent != None:
        tmp.insert(0, node) # Pushes onto the list so they are in the correct order
        node = node.parent
    return tmp

# Modifies the branch and returns a copy of the original branch to make propogating the changes easier
def optimize_branch(branch, tree, obstacles):
    b_copy = [n.copy() for n in branch]
    for i in range(len(branch)-1):
        cnode = branch[i]
        childs = find_children(tree, cnode)
        child = branch[i+1]
        xs, ys, xe, ye = get_sampling_range(cnode.x,cnode.y, g_desc_rad)
        curr_best_x = -1
        curr_best_y = -1
        for x_i in range(xs, xe):
            for y_i in range(ys, ye):
                tnode = Node(x_i, y_i, None)
                tnode.children = cnode.children
                tnode.nearest = cnode.nearest
                n_cost = get_new_cost(tnode, cnode.parent, child)
                diff = child.cost - n_cost    
                if n_cost < child.cost:                    
                    collides_with_descendent = False                   
                    for c in childs:
                        if collision_detection(c.xy, tnode.xy, obstacles):
                            collides_with_descendent = True
                            break
                    if collides_with_descendent:
                        continue
                    elif not collision_detection(tnode.xy, child.xy, obstacles):
                        curr_best_x = x_i
                        curr_best_y = y_i
                        oldxy = cnode.xy
                        cnode.set_x(x_i)
                        cnode.set_y(y_i)  
                        occ = child.cost
                        cnode.cost = cnode.parent.cost + distance(cnode, cnode.parent)
                        child.cost = child.parent.cost + distance(child, child.parent)
                        update_remaining_branch(diff, branch, i+1)  
    return b_copy

def find_children(tree, node):
    tmp = []
    for n in tree.nodes:
        if n.parent == node:
            tmp.append(n)
    return tmp
    
def update_children(tree):
    for node in tree.nodes:
        node.children.clear()
    for node in tree.nodes:
        if node.parent!= None:
            node.parent.children.add(node)

def update_tree_costs(tree):
    for node in tree.nodes:
        if node.parent!= None:
            node.cost = node.parent.cost + distance(node.parent, node)
            
def check_point_in_obstacles(point, obstacles):
    for o in obstacles.obs:
        if o.collidepoint(point):
            return True
    return False
    
def get_new_cost(tnode, parent, child):
    return parent.cost + distance(tnode, parent) + distance(child, tnode)

def update_remaining_branch(diff, branch, index):
    for i in range(index, len(branch)):
        n = branch[i]
        n.cost -= diff
        
    
def update_nearest_nodes(node, tree, obstacles):
    for n in tree.nodes:
        if distance(node, n) < radius:
            # Only add nearest neighbors that are collision free
            if not collision_detection(node.xy, n.xy, obstacles):
                n.nearest.add(node)
                node.nearest.add(n)

        
def get_sampling_range(x, y, rad):
    x_start = max(0, x-rad)
    y_start = max(0,y-rad)
    x_end = min(VALID_AREA[0], x + rad)
    y_end = min(VALID_AREA[1], y + rad)
    return x_start, y_start, x_end, y_end
    
def draw_all_nodes(tree, screen):
    for node in tree.nodes:
        draw_node(node, screen)
    
def update_children(node):
    temp = node
    while temp.parent != None:
        temp.parent.children.add(node)
        temp = temp.parent

def optimize_parent(node, obstacles):
    current = node.cost # Current distance
    parent = node.parent # Current parent assigned to node
    node.parent.children.remove(node) # Remove the node from the parent's children before calculating new parent 
    
    for nbh in node.parent.nearest:
        # The child node might be in the nearest neighbor list so don't do nearest neighbor with itself.
        if nbh.xy == node.xy:
            continue
        if distance(nbh, node) + nbh.cost < current:
            if not collision_detection(node.xy, nbh.xy, obstacles):
                current = distance(nbh, node) + nbh.cost
                parent = nbh
    
    node.parent = parent # Set the new parent
    node.parent.children.add(node) # Add the node to the children's set of the parent. Note that this may be the same parent from before
    
    node.cost = current # Update the cost of the new node
    
# def optimize_parent(node, obstacles):
    # # Current distance and parent
    # current = node.cost 
    # parent = node.parent 
    # # Remove the node from the parent's children before calculating new parent 
    # node.parent.children.remove(node) 
    # children = node.parent.children
    
    # for nbh in node.parent.nearest:
        # # The child node might be in the nearest neighbor list so don't do nearest neighbor with itself.
        # if nbh.xy == node.xy:
            # continue
        # if distance(nbh, node) + nbh.cost < current:
            # if not collision_detection(node.xy, nbh.xy, obstacles):
                # current = distance(nbh, node) + nbh.cost
                # parent = nbh
    # # Set the new parent
    # node.parent = parent
    # node.parent.children.add(node) 
    
    # # Update the cost of the new node 
    # node.cost = current 
    
def highlight_solution_with_collision_print(final_node, screen, obstacles):
    current = final_node
    count = 1
    while current.parent != None:
        print(count, collision_detection(current.xy, current.parent.xy, obstacles))
        count += 1
        pygame.draw.line(screen, GREEN, (current.x, current.y), (current.parent.x, current.parent.y), 3)
        current = current.parent  
        

def isLeaf(node):
    if len(node.children) == 0:
        return True
    return False