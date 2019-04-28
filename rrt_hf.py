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
    # node = node.parent / Uncomment if you don't want to include the leaf node
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
                    if not collision_detection(tnode.xy, child.xy, obstacles):
                        curr_best_x = x_i
                        curr_best_y = y_i
                        oldxy = cnode.xy
                        cnode.set_x(x_i)
                        cnode.set_y(y_i)  
                        occ = child.cost
                        cnode.cost = cnode.parent.cost + distance(cnode, cnode.parent)
                        child.cost = child.parent.cost + distance(child, child.parent)
                        update_remaining_branch(diff, branch, i+1)  
                        #print(occ, child.cost, oldxy, cnode.xy)
    return b_copy

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

# def update_tree(tnode):
    # children = list(tnode.children)
    # while len(children) != 0:
        # for c in children:
            # c.cost = c.parent.cost + distance(c.parent, c)
            # for child in c.children:
                # children.append(child)

def update_remaining_branch(diff, branch, index):
    for i in range(index, len(branch)):
        n = branch[i]
        n.cost -= diff
        
    
# def update_nearest_nodes(node, tree, obstacles):
    # for n in tree.nodes:
        # if distance(node, n) < radius:
            # # Only add nearest neighbors that are collision free
            # if not collision_detection(node.xy, n.xy, obstacles):
                # n.nearest.add(node)
                # node.nearest.add(n)
    # for n in node.nearest:
        # if distance(n, node) > radius:
            # n.nearest.remove(node)
            # node.nearest.remove(n)
            
        
 
# def propogate_changes(q):
    # while len(q) != 0:
    # # always pop the smallest cost item off the queue
        # q.sort(key=lambda n: n.cost)
        # el = q.pop(0)
        # # key stuff not implemented rn
        # # if key(el) > best_cost then
        # #    break
        # for nbh in el.nearest:
            # if nbh.cost > el.cost + distance(el, nbh):
                # nbh.cost = el.cost + distance(el, nbh)
                # nbh.parent = el
                # q.append(nbh)
        # for c in el.get_descendents:
            # c.cost = el.cost + distance(el, c)
            # q.append(c)
        
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
    
def sum_costs(tree):
    pass

def gradient_descent_approx(b, obstacles):
    b_copy = b[:]
    for node in b[::-1]:
        xs, ys, xe, ye = get_sampling_range(b.x, b.y, g_desc_rand)
        for x in range(xs, xe):
            for y in range(ys, ye):
                pass
                
def cost_with_new_sample(node_to_replace, new_xy, branch):
    desc = node_to_replace.get_descendents()
    # Use copies so don't mess up any of the pointers and cost values of the original nodes
    desc_c = [n.copy() for n in desc]
    child = [n.copy() for n in list(node_to_replace.children)]
    parent = node.parent.copy()
    x,y = new_xy
    for node in child:
        pass
        
    pass
    
def gradient_descent(b):
    b_copy = b[:]
    for node in b:
        # Do the gradient descent
        t = 1
        while True: 
            continue
    for i in range(len(b)):
        if b[i] != b_copy[i]:
            # Update in nearest neighbor datastructure
            continue
    pass

def isLeaf(node):
    if len(node.children) == 0:
        return True
    return False