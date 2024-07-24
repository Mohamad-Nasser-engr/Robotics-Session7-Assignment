import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from custom_interfaces.srv import FindClosestWall

class WallFinderService(Node):
    def __init__(self):
        super().__init__('wall_finder_service')
        
        # Create a service
        self.service = self.create_service(
            FindClosestWall,
            'find_closest_wall',
            self.handle_find_closest_wall
        )
        
        # Create a publisher for cmd_vel
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # Create a subscription for laser scan data
        self.scan_sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )

        # Initialize Twist message and distance variable
        self.twist = Twist()
        self.distance = float('inf')
        self.get_logger().info('Service Started')

    def handle_find_closest_wall(self, request, response):
        # Start moving forward
        self.twist.linear.x = 0.5
        self.cmd_vel_pub.publish(self.twist)
        
        # Create a timer to periodically check the distance
        self.timer = self.create_timer(0.1, self.check_distance)
        self.get_logger().info('Moving forward to find the wall')
        
        # Set the response to true to indicate the service call was received
        response.success = True
        return response

    def check_distance(self):
        # Check the distance and stop if needed
        if self.distance <= 0.5:
            self.twist.linear.x = 0.0
            self.cmd_vel_pub.publish(self.twist)
            self.get_logger().info('Stopped, wall detected')
            self.timer.cancel()  # Stop the timer

    def scan_callback(self, msg):
        # Ensure msg.ranges is not empty and get the minimum distance
        if len(msg.ranges) > 0:
            self.distance = min(msg.ranges)
        self.get_logger().info(f"Distance: {self.distance}")

def main(args=None):
    rclpy.init(args=args)
    wall_finder_service = WallFinderService()
    rclpy.spin(wall_finder_service)
    wall_finder_service.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
