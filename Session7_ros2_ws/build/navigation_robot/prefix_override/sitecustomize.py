import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/mohamad/Inmind/Robotics-Session7-Assignment/Session7_ros2_ws/install/navigation_robot'
