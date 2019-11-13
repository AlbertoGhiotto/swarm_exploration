#! /usr/bin/env python

import rospy
# import ros message
from geometry_msgs.msg import Point
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from tf import transformations
# import ros service
from std_srvs.srv import *

# other imports
import math

# _____________________________________________________________________

srv_client_bug_alg_ = None
position_ = Point()
yaw_ = 0
state_desc_ = ['Go to node', 'Obstacle detected']
state_ = 0
# 0 - do "bug_algorith" (Go to node)
# 1 - obstacle detected

# _____________________________________________________________________

# # callbacks
# def clbk_odom(msg):
#     global position_, yaw_

#     # position
#     position_ = msg.pose.pose.position

#     # yaw
#     quaternion = (
#         msg.pose.pose.orientation.x,
#         msg.pose.pose.orientation.y,
#         msg.pose.pose.orientation.z,
#         msg.pose.pose.orientation.w)
#     euler = transformations.euler_from_quaternion(quaternion)
#     yaw_ = euler[2]

# def clbk_laser(msg):
#     global regions_
#     regions_ = {
#         'right':  min(min(msg.ranges[0:143]), 10),
#         'fright': min(min(msg.ranges[144:287]), 10),
#         'front':  min(min(msg.ranges[288:431]), 10),
#         'fleft':  min(min(msg.ranges[432:575]), 10),
#         'left':   min(min(msg.ranges[576:719]), 10),
#     }


def change_state(state):
    global state_, state_desc_
    global srv_client_bug_alg_ # srv_client_objdetected???_
    state_ = state
    rospy.loginfo("state changed: %s", state_desc_[state])
    if state_ == 0:
        resp = srv_client_bug_alg_(True)
    #    resp = srv_obstacle_detection_(False)
    if state_ == 1:
        resp = srv_client_bug_alg_(False)
    #    resp = srv_obstacle_detection_(true)


# _____________________________________________________________________

def main():
    global regions_, position_, desired_position_, state_, yaw_, yaw_error_allowed_
    global srv_client_bug_alg_

    rospy.init_node('robot_control')
    rospy.loginfo("robot_control node started in state: %s" %
                  state_desc_[state_])

    #sub_laser = rospy.Subscriber('front_laser/scan', LaserScan, clbk_laser)
    #sub_odom = rospy.Subscriber('odom', Odometry, clbk_odom)

    srv_client_bug_alg_ = rospy.ServiceProxy('bug_alg_switch', SetBool)

    rospy.wait_for_service('bug_alg_switch')

    # initialize in "do bug_algorithm" state
    change_state(0)

    rate = rospy.Rate(20)
    while not rospy.is_shutdown():

        if state_ == 0:
            # doing bug algoritm
            # UNLESS SOME CONDITION
            # then
            # change_state(1)
            continue

        elif state_ == 1:
            # obstacle detected
            # do smth UNTIL SOME CONDITION
            # then
            # change_state(0)
            continue

        rate.sleep()


if __name__ == "__main__":
    main()