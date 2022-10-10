#!/usr/bin/env python

# Copyright (c) 2011, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the Willow Garage, Inc. nor the names of its
#      contributors may be used to endorse or promote products derived from
#       this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import time

import rospy
from geometry_msgs.msg import Twist

BURGER_MAX_LIN_VEL = 0.22
BURGER_MAX_ANG_VEL = 2.84

LIN_VEL_STEP_SIZE = 0.01
ANG_VEL_STEP_SIZE = 0.1

msg = "-- Turtlebot3_Teleop by CYCU-ICE --"

e = """
Communications Failed
"""


class Turtlebot3_Teleop:
    def __init__(self):
        rospy.init_node("turtlebot3_teleop")
        self.pub = rospy.Publisher("cmd_vel", Twist, queue_size=10)
        self.target_linear_vel = 0.0
        self.target_angular_vel = 0.0
        self.control_linear_vel = 0.0
        self.control_angular_vel = 0.0

    def PrintVels(self):
        print(
            "currently:\tlinear vel %s\t angular vel %s "
            % (
                self.target_linear_vel,
                self.target_angular_vel,
            )
        )

    def MakeSimpleProfile(output, input, slop):
        if input > output:
            output = min(input, output + slop)
        elif input < output:
            output = max(input, output - slop)
        else:
            output = input

        return output

    def Constrain(input, low, high):
        if input < low:
            input = low
        elif input > high:
            input = high
        else:
            input = input

        return input

    def checkLinearLimitVelocity(self, vel):
        vel = self.Constrain(vel, -BURGER_MAX_LIN_VEL, BURGER_MAX_LIN_VEL)
        return vel

    def checkAngularLimitVelocity(self, vel):
        vel = self.Constrain(vel, -BURGER_MAX_ANG_VEL, BURGER_MAX_ANG_VEL)
        return vel

    def Set_Linear_Velocity(self, target_linear_vel):
        self.target_linear_vel = self.CheckLinearLimitVelocity(
            target_linear_vel + LIN_VEL_STEP_SIZE
        )
        self.PublishTopic()

    def Set_Angular_Velocity(self, target_angular_vel):
        self.arget_angular_vel = self.CheckAngularLimitVelocity(
            target_angular_vel + ANG_VEL_STEP_SIZE
        )
        self.PublishTopic()

    def Reset_All_Velocity(self):
        self.target_linear_vel = 0.0
        self.control_linear_vel = 0.0
        self.target_angular_vel = 0.0
        self.control_angular_vel = 0.0
        self.PublishTopic()

    def PublishTopic(self):
        twist = Twist()

        self.control_linear_vel = self.MakeSimpleProfile(
            self.control_linear_vel, self.target_linear_vel, (LIN_VEL_STEP_SIZE / 2.0)
        )
        twist.linear.x = self.control_linear_vel
        twist.linear.y = 0.0
        twist.linear.z = 0.0

        self.control_angular_vel = self.MakeSimpleProfile(
            self.control_angular_vel, self.target_angular_vel, (ANG_VEL_STEP_SIZE / 2.0)
        )
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = self.control_angular_vel

        self.PrintVels()
        self.pub.publish(twist)


if __name__ == "__main__":
    turtlebot3_model = rospy.get_param("model", "burger")
    teleop = Turtlebot3_Teleop()
    print(msg)

    try:
        while not rospy.is_shutdown():
            # here are some examples
            teleop.Set_Linear_Velocity(1.0)
            # use sleep as a timer to maintain the speed
            time.sleep(5)
            teleop.Reset_All_Velocity()

    except:
        print(e)