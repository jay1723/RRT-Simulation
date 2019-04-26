# Jay Rao
import pygame
import sys

from rrt import *
from rrt_one_side import *
from global_vars import *
from structures import *
from helper_functions import *

# Initialize PyGame and some font surfaces to be rendered to the screen later
pygame.init()
button_font = pygame.font.SysFont("Ubuntu", 20)
ob_srf = button_font.render("RESET", False, (0,0,0))
smpl_srf = button_font.render("Run Algo", False, (0,0,0))

    
# Initialize the screen and set its background to white
pygame.display.set_caption("Sampling Simulation")
screen = pygame.display.set_mode(SIZE)
screen.fill(WHITE)


# Create the buttons at the bottom of the screen
reset_button = pygame.draw.rect(screen, RED, (SIZE[0]/2, SIZE[1]-50, SIZE[0]/2, 50))
run_sampler_button = pygame.draw.rect(screen, GREEN, (0, SIZE[1]-50,SIZE[0]/2, 50))
screen.blit(ob_srf, (reset_button.left, reset_button.centery))
screen.blit(smpl_srf, (run_sampler_button.left, run_sampler_button.centery))
pygame.display.flip()



# Define start and goal, draw the start node to the screen
root = Node(START[0], START[1], None)
end = Node(GOAL[0], GOAL[1], None)
tree = Tree(root)
obstacles = Obstacles()
sampler = Random_Sampler(VALID_AREA[0], VALID_AREA[1], end, SAMPLE_GOAL_PROB, obstacles)


end_circle = draw_node(end, screen, color=GREEN, size=5)
root_circle = draw_node(root, screen, color=BLUE, size=5)



# Action loop
while not SOLUTION_FOUND: 
    for event in pygame.event.get():
    # Quit event, close the program
        if event.type == pygame.QUIT:
            SOLUTION_FOUND = True
            pygame.display.quit()
            pygame.quit()
            sys.exit()    
    # Mouse pressed on the screen
        if event.type == pygame.MOUSEBUTTONDOWN:
            # (X,Y) position of the mouse press
            pos = pygame.mouse.get_pos() 
            # If the button for running the planning algorithm was pressed then run the algorithm
            if run_sampler_button.collidepoint(pos):
                RUN_SAMPLER = True
                print("Run sampler")
            elif reset_button.collidepoint(pos):
                # Reset relevant global variables
                START = sampler.sample()
                GOAL = sampler.sample()
                root = Node(START[0], START[1], None)
                end = Node(GOAL[0], GOAL[1], None)
                tree = Tree(root)
                obstacles = Obstacles()
                # Fill the screen with a blank screen
                screen.fill(WHITE)
                pygame.display.update()
                # Redraw the starting points with the new data and redraw the buttons
                draw_node(end, screen, color=GREEN, size=5)
                draw_node(root, screen, color=BLUE, size=5)
                reset_button = pygame.draw.rect(screen, RED, (SIZE[0]/2, SIZE[1]-50, SIZE[0]/2, 50))
                run_sampler_button = pygame.draw.rect(screen, GREEN, (0, SIZE[1]-50,SIZE[0]/2, 50))
                screen.blit(ob_srf, (reset_button.left, reset_button.centery))
                screen.blit(smpl_srf, (run_sampler_button.left, run_sampler_button.centery))
                pygame.display.update()
                RUN_SAMPLER = False
                
            elif pos[0] < VALID_AREA[0] and pos[1] < VALID_AREA[1]: 
                if not corner_pressed:
                    corner_pressed = True
                    corner_pos = pos
                else:
                    width = pos[0] - corner_pos[0]
                    height = pos[1] - corner_pos[1]
                    if (width < 0 and height < 0):
                        obst = pygame.Rect(pos[0], pos[1], -width, -height)
                    elif (width < 0 and height > 0):
                        obst = pygame.Rect(pos[0], corner_pos[1], -width, height)
                    elif (width > 0 and height < 0):
                        obst = pygame.Rect(corner_pos[0], pos[1], width, -height)
                    else:
                        obst = pygame.Rect(corner_pos[0], corner_pos[1], width, height)
                    if obst.colliderect(root_circle) or obst.colliderect(end_circle):
                        corner_pressed = False
                    else:
                        rect = pygame.draw.rect(screen, BLUE, obst)
                        #print(rect.topleft, rect.width, rect.height)
                        pygame.display.flip()
                        obstacles.add_obstacle(rect)
                        corner_pressed = False      
    if RUN_SAMPLER:
        if PLANNER == "RRT":            
            out, cost = rrt(screen, sampler, root, end, tree, obstacles)
            pygame.display.flip()
            if out:
                winner_font = pygame.font.SysFont("Ubuntu", 30)
                tsrf = winner_font.render("Cost: %d" % cost, False, (0,0,0))
                print(cost)
                screen.blit(tsrf, (0,0))
                SOLUTION_FOUND = out
                RUN_SAMPLER = False
        elif PLANNER == "RRT-ONE-SIDE":
            out, cost = rrt_one_side(screen, sampler, root, end, tree, obstacles)
            pygame.display.flip()
            if out:
                winner_font = pygame.font.SysFont("Ubuntu", 30)
                tsrf = winner_font.render("Cost: %d" % cost, False, (0,0,0))
                print(cost)
                screen.blit(tsrf, (0,0))
                SOLUTION_FOUND = True
        elif PLANNER == "TEST-COLLISION":
            out = test_collision(screen, sampler, root, end, tree, obstacles)
            pygame.display.flip()
            if out:
                SOLUTION_FOUND = True  
            continue
            

def main():
            






    
    
    
    
    
