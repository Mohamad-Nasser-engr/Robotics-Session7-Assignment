import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from custom_interfaces.action import MeasureLapTime 

class LapTimeActionClient(Node):
    def __init__(self):
        super().__init__('lap_time_action_client')
        self._action_client = ActionClient(self, MeasureLapTime, 'measure_lap_time')
        self.send_goal()

    def send_goal(self):
        self.get_logger().info('Sending goal to action server...')
        goal_msg = MeasureLapTime.Goal()

        # Wait for the action server to be ready
        self._action_client.wait_for_server()

        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected by the action server.')
            return

        self.get_logger().info('Goal accepted by the action server.')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback_msg):
        elapsed_time = feedback_msg.feedback.elapsed_time
        self.get_logger().info(f'Elapsed time: {elapsed_time:.2f} seconds')

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Lap completed in {result.total_time:.2f} seconds')
        rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    action_client = LapTimeActionClient()
    rclpy.spin(action_client)

if __name__ == '__main__':
    main()
