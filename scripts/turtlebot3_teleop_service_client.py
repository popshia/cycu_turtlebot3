#!/usr/bin/env python
# client side

import sys

import rospy

from ros_turtlebot3_teleop.srv import Velocity, VelocityResponse

e = """
Communications Failed
"""


def Set_Velocities_Client(linear_velocity, angular_velocity):
    rospy.wait_for_service("set_velocities")
    try:
        set_velocities = rospy.ServiceProxy("set_velocities", Velocity)
        response = set_velocities(linear_velocity, angular_velocity)
        print(response)
    except:
        print(e)


def usage():
    return """
    -- Turtlebot3_Teleop by CYCU-ICE --
    --    Linear Velocity: +- 0.22   --
    --   Angular Velocity: +- 2.84   --
    """


if __name__ == "__main__":
    if len(sys.argv) == 2:
        linear_vel = float(sys.argv[1])
        angular_vel = float(sys.argv[2])
    else:
        print(usage())
        sys.exit(1)

    print(f"Requesting (linear:{linear_vel}, angular:{angular_vel})")
    Set_Velocities_Client(linear_vel, angular_vel)