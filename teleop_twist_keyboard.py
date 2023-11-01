import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys
if sys.platform != 'win32':
    import termios
    import tty


def getKey(settings):
    if sys.platform == 'win32':
        # getwch() returns a string on Windows
        key = msvcrt.getwch()
    else:
        tty.setraw(sys.stdin.fileno())
        # sys.stdin.read() returns a string on Linux
        key = sys.stdin.read(1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


def saveTerminalSettings():
    if sys.platform == 'win32':
        return None
    return termios.tcgetattr(sys.stdin)


def restoreTerminalSettings(old_settings):
    if sys.platform == 'win32':
        return
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


class KeyboardNode(Node):
    def __init__(self):
        super().__init__('keyboard_node')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer_ = self.create_timer(0.1, self.publish_twist)
        self.twist_ = Twist()
        self.previous_twist_ = Twist()
        self.key_received = False

    def publish_twist(self):
        self.get_logger().info('publishing...')
        self.publisher_.publish(self.twist_)

    def run(self):
        settings = saveTerminalSettings()
        while rclpy.ok():
            key = getKey(settings)

            if key == 'w':
                self.get_logger().info('getting inputs')
                self.twist_.linear.x = 0.05
                self.twist_.angular.z = 0.0
                self.publisher_.publish(self.twist_)
            elif key == 's':
                self.get_logger().info('getting inputs')
                self.twist_.linear.x = -0.05
                self.twist_.angular.z = 0.0
                self.publisher_.publish(self.twist_)
            elif key == 'a':
                self.get_logger().info('getting inputs')
                self.twist_.linear.x = 0.0
                self.twist_.angular.z = 0.05
                self.publisher_.publish(self.twist_)
            elif key == 'd':
                self.get_logger().info('getting inputs')
                self.twist_.linear.x = 0.0
                self.twist_.angular.z = -0.05
                self.publisher_.publish(self.twist_)
            elif key == 'q':
                break
            # elif key == '':
            #     self.get_logger().info('waiting inputs, press q to exit')
            #     self.twist_.linear.x = 0.0
            #     self.twist_.angular.z = 0.0
            #     self.publisher_.publish(self.twist_)

        restoreTerminalSettings(settings)


def main(args=None):
    rclpy.init(args=args)
    node = KeyboardNode()
    node.run()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
