import rclpy
import time
from rclpy.node import Node
from std_srvs.srv import Trigger
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from custom_interfaces.srv import FindClosestWall

class WallFollowerNode(Node):
    def __init__(self):
        super().__init__('wall_follower_node')
        
        # Create a service client to call FindClosestWall
        self.find_closest_wall_client = self.create_client(FindClosestWall, 'find_closest_wall')
        while not self.find_closest_wall_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')
        
        # Create a publisher for /cmd_vel
        self.cmd_vel_publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # Create a subscription to /scan
        self.scan_subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )
        self.twist =Twist()
        self.forward_distance = float('inf')
        self.left_distance = float('inf')
        self.right_distance = float('inf')
        self.target_distance = 0.5 # Target distance to the wall in meters
        
        req = FindClosestWall.Request()
        future = self.find_closest_wall_client.call_async(req)
        rclpy.spin_until_future_complete(self, future)
        response = future.result()
        if response.success:
            self.get_logger().info('Successfully moved to the closest wall.')
            # Create a subscription to /scan after robot arrives at the first wall
            self.scan_subscription = self.create_subscription(LaserScan,'/scan',self.scan_callback,10)
        else:
            self.get_logger().error('Failed to move to the closest wall.')         

    def scan_callback(self, msg):
        if msg.ranges[0] <0.5:
            self.twist.linear.x = 0.0
            self.twist.angular.z = -0.35
        elif msg.ranges[25] <0.55:
            self.twist.linear.x = 0.0
            self.twist.angular.z = -0.15
        else:
            self.twist.linear.x = 0.5
            self.twist.angular.z = 0.0
        self.cmd_vel_publisher.publish(self.twist)

def main(args=None):
    rclpy.init(args=args)
    node = WallFollowerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
