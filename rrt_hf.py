from helper_functions import *

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
        
    
def get_nearest_obstacle_collision(point, nearest, obstacles):
    nst = (100000,100000)
    print("I am here")
    for obstacle in obstacles.obs:
        iX, iY = nearest_edge_collision(point, nearest, obstacle)
        
        if distance_point((iX, iY), point) < distance_point(nearest, point):
            nst = (iX, iY)
            
    if nst[0] == 100000 and nst[1] == 100000 or len(obstacles.obs) == 0:
        return False, (-1, -1)
    return True, nst
    
    
def interpolate_to_obstacle(p1, p2, obstacles):
    # If there is an obstacle in the way find the nearest obstacle 
    pass
