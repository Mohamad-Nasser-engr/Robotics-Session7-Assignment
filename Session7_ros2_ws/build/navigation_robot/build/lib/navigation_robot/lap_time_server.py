import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan  # Assuming laser scan data is used to detect walls
from custom_interfaces.action import MeasureLapTime
import math

class LapTimeServer(Node):

    def __init__(self):
        super().__init__('lap_time_server')

        # Action Server
        self.action_server = ActionServer(
            self,
            MeasureLapTime,
            'measure_lap_time',
            self.execute_callback
        )

        # Subscriptions
        self.odom_sub = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )
        self.laser_sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.laser_callback,
            10
        )

        # Other attributes
        self.start_position_x = None
        self.start_position_y = None
        self.start_time = None
        self.current_time = None
        self.leaved_starting_position = False
        self.near_wall = False
        self.wall_distance_threshold = 0.3  # Adjust based on your environment

    def odom_callback(self, msg):
        # Update current position and time
        self.current_position_x = msg.pose.pose.position.x
        self.current_position_y = msg.pose.pose.position.y
        self.current_time = msg.header.stamp.sec + 1e-9 * msg.header.stamp.nanosec

    def laser_callback(self, msg):
        # Check if any laser scan distance is below the threshold, indicating proximity to a wall
        if any(distance < self.wall_distance_threshold for distance in msg.ranges):
            self.near_wall = True
        else:
            self.near_wall = False

    def execute_callback(self, goal_handle):
        self.get_logger().info('Received request to measure lap time.')

        # Wait until the robot is near a wall
        while not self.near_wall:
            rclpy.spin_once(self, timeout_sec=0.1)

        # Now wait for valid odometry data to set the starting position
        while self.start_position_x is None or self.start_position_y is None:
            rclpy.spin_once(self, timeout_sec=0.1)
            self.start_position_x = self.current_position_x
            self.start_position_y = self.current_position_y
            self.start_time = self.current_time

        self.leaved_starting_position = False
        feedback_msg = MeasureLapTime.Feedback()

        # Wait until the robot moves away from the starting position
        while not self.leaved_starting_position:
            rclpy.spin_once(self, timeout_sec=0.1)
            distance_from_start = math.sqrt(
                (self.current_position_x - self.start_position_x) ** 2 +
                (self.current_position_y - self.start_position_y) ** 2
            )
            if distance_from_start > 0.1:  # Example threshold to consider the robot has left the start
                self.leaved_starting_position = True

        # Wait until the robot returns to the starting position
        while True:
            rclpy.spin_once(self, timeout_sec=0.1)
            feedback_msg.elapsed_time = self.current_time - self.start_time
            goal_handle.publish_feedback(feedback_msg)

            distance_from_start = math.sqrt(
                (self.current_position_x - self.start_position_x) ** 2 +
                (self.current_position_y - self.start_position_y) ** 2
            )
            if distance_from_start < 0.1:  # Check if robot returned to starting area
                break

        # Compute the total lap time
        result = MeasureLapTime.Result()
        result.total_time = self.current_time - self.start_time
        goal_handle.succeed()
        return result

def main(args=None):
    rclpy.init(args=args)
    lap_time_server = LapTimeServer()

    try:
        rclpy.spin(lap_time_server)
    except KeyboardInterrupt:
        pass

    lap_time_server.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
