from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='navigation_robot',  
            executable='wall_finder',  
            name='wall_finder_service'
    
        ),
        Node(
            package='navigation_robot',  
            executable='robot_driver',  
            name='robot_driver'
    
        ),
        Node(
            package='navigation_robot',  
            executable='lap_time_server',  
            name='lap_time_server'
    
        ),
        Node(
            package='navigation_robot',  
            executable='lap_time_client',  
            name='lap_time_client'
    
        )
    ])
