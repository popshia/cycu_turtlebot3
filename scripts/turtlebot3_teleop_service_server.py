#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

from ros_turtlebot3_teleop.srv import Velocity, VelocityResponse

BURGER_MAX_LIN_VEL = 0.22
BURGER_MAX_ANG_VEL = 2.84

LIN_VEL_STEP_SIZE = 0.01
ANG_VEL_STEP_SIZE = 0.1


class Server:
    def __init__(self):
        rospy.init_node("set_velocities_server")
        self.srv = rospy.Service("set_velocities", Velocity, self.Set_Velocities)
        self.pub = rospy.Publisher("cmd_vel", Twist, queue_size=10)
        print("Ready to set velocities (linear:+-0.22, angular:+-2.84):")
        rospy.spin()

    def MakeSimpleProfile(self, output, input, slop):
        if input > output:
            output = min(input, output + slop)
        elif input < output:
            output = max(input, output - slop)
        else:
            output = input

        return output

    def Set_Velocities(self, request):
        control_linear_vel = 0.0
        control_angular_vel = 0.0

        print(
            "Setting velocities (linear:{0} angular:{1})".format(
                request.linear_velocity, request.angular_velocity
            )
        )

        twist = Twist()

        control_linear_vel = self.MakeSimpleProfile(
            control_linear_vel, request.linear_velocity, (LIN_VEL_STEP_SIZE / 2.0)
        )
        twist.linear.x = control_linear_vel
        twist.linear.y = 0.0
        twist.linear.z = 0.0

        control_angular_vel = self.MakeSimpleProfile(
            control_angular_vel, request.angular_velocity, (ANG_VEL_STEP_SIZE / 2.0)
        )
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = control_angular_vel

        self.pub.publish(twist)
        return VelocityResponse("Velocities Set.")


if __name__ == "__main__":
    Server = Server()