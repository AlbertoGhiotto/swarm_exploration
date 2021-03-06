# Fixed-Map Exploration Through a Robotic Swarm

The aim of this project was to build a simulation with up to 4 robots implementing the Node counting algorithm (a simple graph-traversal method) in order to **autonomously map** the fixed-lenght environment in which they are spawned, along with the obstacles contained in it, to a fully connected graph shared representation. The architecture implements a **distributed control** approach, with the only centralized node which integrates the data sent by each autonoumous robot.

**Note**: a `demo.mkv` demonstration video is available in the main folder.

![alt text](https://github.com/Davidelanz/expro_asmt1/blob/master/demo.png)

## Implementation
### Assumptions
In order to implement this architecture some assumptions were made:
1. The map and the corresponding graph are constructed by the robots as they explore their surrounding environment, by placing a -1 in the position of the obstacle detected.
1. The distances between nodes is equal to 1 meter.
1. A node is set as "visited" if the robot is at a distance > 0.2 meter from the node.
1. At the beginning of the simulation, the robots could be in random positions, but thery are always outside the graph.
1. All free nodes should be visited by at least one robot.
1. The algorithm has to be robust to variation of the maps (size and obstacles), of the starting position of the robot and of the number of robots.
1. The robots use to detect obstacoles in run-time, and they are not informed of the position of other robots by the centralized node

## Ros Package

The developed package is divided in the following folders:
1. `urdf` folder with `.xacro` robot description
1. `launch` folder with relative launchfiles setting up the simulation environment with different number of robots (empty world), taking as input the starting position of each robot (a launch file for each different number of robots). 
1. `src` code implementing the algorithm (taking as input a text file with the map/graph description).

### Software prerequisites:
1. ROS kinetic, to download it follow [this guide](http://wiki.ros.org/kinetic/Installation/Ubuntu).
1. GAZEBO robotic simulator for ROS, to download it follow [this guide](http://gazebosim.org/tutorials?tut=ros_installing). 

### How to run the project

1. Clone this repository in your workspace through the command 
	```bash
    git clone
    ```
2. Launch the desired launchfile through one of the following command
	##### 1 robot
	```bash
	roslaunch node_counting_alg spawn1-hol.launch
	```
	##### 4 robots
	```bash
	roslaunch node_counting_alg spawn4-hol.launch
	```



## Authors
* Davide Lanza       - davidel96@hotmail.it
* Alberto Ghiotto    - alberto.ghiotto@hotmail.it
* Alberto Grillo     - albogrillo@gmail.com



EMARO Advanced Robotics Master - 2nd year  
University of Genoa
