#!/usr/bin/env python

import rospy
from mavros_msgs.srv import CommandBool, CommandTOL
from mavros_msgs.msg import State
import time

current_state = State()

def state_cb(state):
    global current_state
    current_state = state

rospy.init_node('arming_takeoff_node')
rate = rospy.Rate(10)  # Hz


# wait for mavros node to get live
time.sleep(3)

# Subscribe to MAVROS state topic
state_sub = rospy.Subscriber("mavros/state", State, state_cb)
# Set up services for arming and takeoff
arming_service = rospy.ServiceProxy("mavros/cmd/arming", CommandBool)
takeoff_service = rospy.ServiceProxy("mavros/cmd/takeoff", CommandTOL)

# Wait for connection to the MAVROS node
while not rospy.is_shutdown() and current_state.connected:
    rate.sleep()

# Arm the drone
rospy.loginfo("Arming...")
arming_service(True)
while not rospy.is_shutdown() and not current_state.armed:
    rate.sleep()

# Take off to a height of 3 meters
rospy.loginfo("Taking off...")
takeoff_service(altitude=3)
while not rospy.is_shutdown() and current_state.mode != "GUIDED" and not rospy.is_shutdown():
    rate.sleep()

rospy.loginfo("Drone armed and took off successfully")
