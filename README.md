# Description 
This ROS2 project implements a robot driver that navigates the robot to the nearest wall and then make it lap around the walls. Additionally, this project will calculate the time it takes the robot to complete one lap. 

## Functionalities
1. Wall finder service:
- This node will locate the closest wall to the robot and then navigate it to it.
2. Robot driver:
- This node will first call the wall finder service to make sure that the robot is near a wall. After that this node will make the robot do laps around the four walls. 
3. Lap time action server:
- This action server node will calculate the total time it takes the robot to complete one lap.
4. Lap time client:
- This node will call the lap time action server and recieve feedback (elapsed time) and the result (total time) from it.
5. Launch file:
- The launch file will be used to run the four previously discussed nodes at the same time.

## Usage
- clone the repository:
```bash
git clone git@github.com:Mohamad-Nasser-engr/Robotics-Session7-Assignment.git
```
- Build the workspace:
```bash
cd Robotics-Session7-Assignment/Session7_ros2_ws
```
```bash
colcon build
```
- source ROS2 and bashrc:
```bash
source /opt/ros/humble/setup.bash
```
```bash
source install/setup.bash
```
- launch the simulation environment in gazebo:
```bash
ros2 launch turtlebot3_gazebo turtlebot3_dqn_stage1.launch.py
```
- launch the nodes:
```bash
ros2 launch launch/Robot_navigation_launch.py 
```
