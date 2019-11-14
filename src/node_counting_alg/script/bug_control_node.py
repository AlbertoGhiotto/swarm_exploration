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

#_____________________________________________________________________

srv_client_go_to_point_ = None
srv_client_wall_follower_ = None
yaw_ = 0
yaw_error_allowed_ = 5 * (math.pi / 180) # 5 degrees
position_ = Point()
desired_position_ = Point()
desired_position_.x = rospy.get_param('des_pos_x')
desired_position_.y = rospy.get_param('des_pos_y')
desired_position_.z = 0
regions_ = None
state_desc_ = ['Go to point', 'wall following']
state_ = 0
# 0 - go to point
# 1 - wall following

#_____________________________________________________________________

# callbacks
def clbk_odom(msg):
    global position_, yaw_
    
    # position
    position_ = msg.pose.pose.position
    
    # yaw
    quaternion = (
        msg.pose.pose.orientation.x,
        msg.pose.pose.orientation.y,
        msg.pose.pose.orientation.z,
        msg.pose.pose.orientation.w)
    euler = transformations.euler_from_quaternion(quaternion)
    yaw_ = euler[2]

def clbk_laser(msg):
    global regions_
    regions_ = {
        'right':  min(min(msg.ranges[0:143]), 10),
        'fright': min(min(msg.ranges[144:287]), 10),
        'front':  min(min(msg.ranges[288:431]), 10),
        'fleft':  min(min(msg.ranges[432:575]), 10),
        'left':   min(min(msg.ranges[576:719]), 10),
    }

def change_state(state):
    global state_, state_desc_
    global srv_client_wall_follower_, srv_client_go_to_point_
    state_ = state
    rospy.loginfo("state changed: %s" , state_desc_[state])
    if state_ == 0:
        resp = srv_client_go_to_point_(True)
        resp = srv_client_wall_follower_(False)
    if state_ == 1:
        resp = srv_client_go_to_point_(False)
        resp = srv_client_wall_follower_(True)
        

def normalize_angle(angle):
    if(math.fabs(angle) > math.pi):
        angle = angle - (2 * math.pi * angle) / (math.fabs(angle))
    return angle


#_____________________________________________________________________

def main():
    global regions_, position_, desired_position_, state_, yaw_, yaw_error_allowed_
    global srv_client_go_to_point_, srv_client_wall_follower_
    
    rospy.init_node('bug_control')
    rospy.loginfo("bug_control node started in state: %s" % state_desc_[state_])
    
    sub_laser = rospy.Subscriber('front_laser/scan', LaserScan, clbk_laser)
    sub_odom = rospy.Subscriber('odom', Odometry, clbk_odom)
    
    srv_client_go_to_point_ = rospy.ServiceProxy('go_to_point_switch', SetBool)
    srv_client_wall_follower_ = rospy.ServiceProxy('wall_follower_switch', SetBool)
    
    rospy.wait_for_service('go_to_point_switch')
    rospy.wait_for_service('wall_follower_switch')

    # initialize going to the point
    change_state(0)
    
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        if regions_ == None:
            continue
        
        if state_ == 0:
            if regions_['front'] > 0.01 and regions_['front'] < 0.4:
                rospy.loginfo("OBSTACLE DETECTED\n")
                change_state(1)
        
        elif state_ == 1:
            desired_yaw = math.atan2(desired_position_.y - position_.y, desired_position_.x - position_.x)
            err_yaw = normalize_angle(desired_yaw - yaw_)

            if(err_yaw > math.pi):
                err_yaw=err_yaw-2*math.pi

            if(err_yaw < -math.pi):
                err_yaw=err_yaw+2*math.pi

            if regions_['front'] > 2 and math.fabs(err_yaw)<0.05:
                rospy.loginfo("TOO FAR FROM WALL: not following anymore\n")
                change_state(0)
            
        rate.sleep()

if __name__ == "__main__":
    main()