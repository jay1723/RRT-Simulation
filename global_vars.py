## Global Variables ##
SIZE = (800,650)
VALID_AREA = (800, 600)
SOLUTION_FOUND = False
PLANNER = "ROP" # (ROS, ROP, DRRT)
RUN_SAMPLER = False
## COLORS ##
WHITE = (255,255,255)
BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)
YELLOW = (255,255,0)
BLACK = (0,0,0)
DOT_SIZE = 1
######################
START = (0, 600)
GOAL = (800, 0)
SAMPLE_GOAL_PROB = .0005
MAX_LENGTH = 50.0
######################

## Gradient Descent ##
alpha = 0.01
radius = 50
g_desc_rad = 10

## Obstacle Events ###
corner_pressed = False
corner_pos = (0,0)


### Testing Events ###
narrow_test = True
sparse_test = False
sparse_test2 = False
