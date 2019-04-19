import helper_functions
from structures import *
from helper_functions import *
def rrt(screen, sampler, start, end, tree):
    point = sampler.sample()
    temp = Node(point[0], point[1], None)
    nearest = nearest_node(temp, tree)
    temp.parent = nearest
    tree.nodes.append(temp)
    draw_node(temp, screen)
    if distance(temp, end) < 5:
        end.parent = temp
        SOLUTION_FOUND = True
        draw_node(end, screen)
        highlight_solution(end, screen)
        pygame.display.flip()
        pygame.time.delay(20000) 
        return True
    return False
