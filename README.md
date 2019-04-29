# RRT-Simulation
RRT Path Planning simulation using PyGame GUI library for Python

## Installation

### Note
There is a known problem within the Pygame community of pygame not properly displaying on the newest Mac update (OSX Mojave)
Run this code only on a Windows (I am running Windows10) or Linux (Ubuntu works) machine. 

### Requirements:
Requires Python 3 (I am running Python3.7.3) and pip3 (pip should come installed with python)

#### Pip modules
You can install from the requirements.txt by running `pip3 install -r requirements.txt`
If this does not work please individually install:
`numpy`
`pygame`

## Using the simulator
* To run the simulator simply run the command `python simulator.py` from your terminal while in the code's directory. 
* Once in the simulator you can click `Run Algo` to run the currently selected algorithm in the currently loaded environment.
* If you want to change the algorithm that is running check the `global_vars.py` method and modify the `PLANNER` variable there with one of the three options specified in the document. 
* For reference `ROS` is RRT One Side, `ROP` is RRT Optimize Parent, `DRRT` is modified DRRT.
* To change the start and goal positions simply change the `START` and `GOAL` global variables also listed in this file. The valid area to select within is (`800,600`).
* Clicking the `RESET` button will clear the screen and allow you to set up a new obstacle pattern. 
* To create obstacles simply click once for where you want the top left corner of the obstacle to be and click again to select where you want the bottom right of the obstacle to be. 
* Those are all of the basic features of the simulator as of right now. 
* After you exit the simulation you should see a line in the terminal that outputs the number of nodes and the total cost of the path for the given path. 
## Sources:
* [Line/Line collision detection logic](http://www.jeffreythompson.org/collision-detection/line-line.php)
* [Box/Line collision detection logic](http://www.jeffreythompson.org/collision-detection/line-rect.php)
* [LaTex help](https://tex.stackexchange.com/questions/219816/algorithm-in-ieee-format\)
