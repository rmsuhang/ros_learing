#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

class TurtleController:
    def __init__(self):
        rospy.init_node('turtle_controller', anonymous=True)
        # Publisher to control the turtle's velocity
        self.velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        # Subscriber to get the turtle's current pose
        self.pose_subscriber = rospy.Subscriber('/turtle1/pose', Pose, self.update_pose)
        self.pose = Pose()
        # Set the loop rate
        self.rate = rospy.Rate(10)

    def update_pose(self, data):
        # Callback function to update the turtle's pose
        self.pose = data

    def move_forward(self, distance):
        vel_msg = Twist()
        # Set linear vel 0.5 m/s
        vel_msg.linear.x = 0.5
        # Record the start time
        t0 = rospy.Time.now().to_sec()
        current_distance = 0
        # forward 
        while current_distance < distance:
            self.velocity_publisher.publish(vel_msg)
            t1 = rospy.Time.now().to_sec()
            current_distance = 0.5 * (t1 - t0)
            self.rate.sleep()

        # Stop 
        vel_msg.linear.x = 0
        self.velocity_publisher.publish(vel_msg)

    def rotate(self, angle):
        vel_msg = Twist()
        # Set angular vel to 0.05 rad/s
        vel_msg.angular.z = 0.05
        # Record the start time
        t0 = rospy.Time.now().to_sec()
        current_angle = 0
        # rotate 
        while current_angle < math.radians(angle):
            self.velocity_publisher.publish(vel_msg)
            t1 = rospy.Time.now().to_sec()
            current_angle = 0.05 * (t1 - t0)
            self.rate.sleep()

        # Stop the turtle
        vel_msg.angular.z = 0
        self.velocity_publisher.publish(vel_msg)

    def move_in_hexagon(self):
        # Side length of the hexagon
        side_length = 2
        # Angle to rotate 
        angle = 60
        # Main loop to move in a hexagon shape
        while not rospy.is_shutdown():
            self.move_forward(side_length)  # Move forward
            self.rotate(angle)  # Rotate

        print(" zhangsuhang 2021010778")

if __name__ == '__main__':
    try:
        controller = TurtleController()
        controller.move_in_hexagon()
    except rospy.ROSInterruptException:
        pass
