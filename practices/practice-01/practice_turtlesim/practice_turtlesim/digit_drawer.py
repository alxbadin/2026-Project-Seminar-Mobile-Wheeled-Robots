import math

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from turtlesim.msg import Pose


def angle_difference(target, current):
    d = target - current

    while d > math.pi:
        d -= 2 * math.pi

    while d < -math.pi:
        d += 2 * math.pi

    return d


class DigitDrawer(Node):

    def __init__(self):
        super().__init__('digit_drawer')

        self.declare_parameter('turtle', 'turtle1')
        self.declare_parameter('digit', '0')

        self.turtle = self.get_parameter('turtle').value
        self.digit = self.get_parameter('digit').value

        self.publisher = self.create_publisher(
            Twist,
            '/' + self.turtle + '/cmd_vel',
            10
        )

        self.subscription = self.create_subscription(
            Pose,
            '/' + self.turtle + '/pose',
            self.pose_callback,
            10
        )

        self.pose = None
        self.action_number = 0
        self.started = False
        self.start_x = 0.0
        self.start_y = 0.0

        if self.digit == '0':
            self.actions = [
                ('move', 2.5),
                ('turn', math.pi / 2),
                ('move', 5.0),
                ('turn', math.pi),
                ('move', 2.5),
                ('turn', -math.pi / 2),
                ('move', 5.0),
            ]
        else:
            self.actions = [
                ('move', 5.0),
            ]

        self.timer = self.create_timer(0.05, self.move_turtle)

    def pose_callback(self, msg):
        self.pose = msg

    def move_turtle(self):
        if self.pose is None:
            return

        msg = Twist()

        if self.action_number >= len(self.actions):
            self.publisher.publish(msg)
            return

        action, value = self.actions[self.action_number]

        if action == 'move':
            if not self.started:
                self.start_x = self.pose.x
                self.start_y = self.pose.y
                self.started = True

            distance = math.sqrt(
                (self.pose.x - self.start_x) ** 2 +
                (self.pose.y - self.start_y) ** 2
            )

            if distance < value:
                msg.linear.x = 1.0
            else:
                self.action_number += 1
                self.started = False

        if action == 'turn':
            difference = angle_difference(value, self.pose.theta)

            if abs(difference) > 0.03:
                if difference > 0:
                    msg.angular.z = 1.0
                else:
                    msg.angular.z = -1.0
            else:
                self.action_number += 1

        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)

    node = DigitDrawer()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()
