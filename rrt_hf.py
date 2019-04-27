from helper_functions import *
from global_vars import *
from functools import *

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
    node = node.parent
    tmp = []
    while node.parent != None:
        tmp.append(node)
        node = node.parent
    return tmp
    
    
def update_nearest_nodes(node, tree, obstacles):
    for n in tree.nodes:
        if distance(node, n) < radius:
            # Only add nearest neighbors that are collision free
            if not collision_detection(node.xy, n.xy, obstacles):
                n.nearest.add(node)
                node.nearest.add(n)
        
 
def propogate_changes(q):
    while len(q) != 0:
    # always pop the smallest cost item off the queue
        q.sort(key=lambda n: n.cost)
        el = q.pop(0)
        # key stuff not implemented rn
        # if key(el) > best_cost then
        #    break
        for nbh in el.nearest:
            if nbh.cost > el.cost + distance(el, nbh):
                nbh.cost = el.cost + distance(el, nbh)
                nbh.parent = el
                q.append(nbh)
        for c in el.get_descendents:
            c.cost = el.cost + distance(el, c)
            q.append(c)
        

def draw_all_nodes(tree, screen):
    for node in tree.nodes:
        draw_node(node, screen)
    
def update_children(node):
    temp = node
    while temp.parent != None:
        temp.parent.children.add(node)
        temp = temp.parent


def optimize_parent(node):
    current = node.cost # Current distance
    parent = node.parent # Current parent assigned to node
    node.parent.children.remove(node) # Remove the node from the parent's children before calculating new parent 
    for nbh in parent.nearest:
        # The child node might be in the nearest neighbor list so don't do nearest neighbor with itself.
        if nbh.xy == node.xy:
            continue
        if distance(nbh, node) + nbh.cost < current:
            current = distance(nbh, node) + nbh.cost
            parent = nbh
    
    node.parent = parent # Set the new parent
    node.parent.children.add(node) # Add the node to the children's set of the parent. Note that this may be the same parent from before
    node.cost = current # Update the cost of the new node
    
def sum_costs(tree):
    pass

def gradient_descent(b):
    pass

def isLeaf(node):
    if len(node.children) == 0:
        return True
    return False