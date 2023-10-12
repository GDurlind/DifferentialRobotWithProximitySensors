#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from demo_programs.msg import prox_sensor
from demo_programs.msg import line_sensor
import math
import time

move = Twist()
set_turn = 0

def feedback(messages):
    
    Front_left = messages.prox_front_left
    Front = messages.prox_front
    Front_right = messages.prox_front_right
    Back_left_left = messages.prox_back_left_left
    Back_right_right = messages.prox_back_right_right
    Front_left_left = messages.prox_front_left_left
    Front_right_right = messages.prox_front_right_right
    move.angular.z = 0
    
    # Turns robot relative to walls infront
    if Front_left_left > Front_right_right:
        move.angular.z = 1.8     
        move.linear.x = 0.4
        
    if  Front_right_right > Front_left_left:
        move.angular.z = -1.8 
        move.linear.x = 0.4
        

    # Solo back sensors turning oppositely     
    if Back_left_left > 0 and Front_left_left == 0 and \
        Back_right_right == 0 and Front == 0:
            move.angular.z = 2.0
            move.linear.x = 0.5
        
    if Back_right_right > 0 and Front_right_right == 0 and \
        Back_left_left == 0 and Front == 0:
            move.angular.z = -2.0
            move.linear.x = 0.5 
        
    # Keeps robot moving forward along walls
    if Front_right_right > 0 and Back_right_right > 0:
        move.angular.z = -10.0
        move.linear.x = 0.5
    
    if Front_left_left > 0 and Back_left_left > 0:
        move.angular.z = 3.7
        move.linear.x = 0.5 
        
    # Creates sharp turns if the robot finds itself cornered by the obstacle course
    if Front_right > 0 and Back_right_right > 0:
        move.angular.z = -4.0
        move.linear.x = 0.5

    if Front_left > 0 and Back_left_left > 0:
        move.angular.z = 4.0
        move.linear.x = 0.5
        
    if Front_right > 0 and Back_right_right > 0 and Front_right_right > 0:
        move.angular.z = -30
        move.linear.x = 0.4

    if Front_left > 0 and Back_left_left > 0 and Front_left_left > 0:
        move.angular.z = 30
        move.linear.x = 0.4
        
    if Front == 0:
        move.linear.x = 0.5
 
    
def feedback2(messages):
# If the Line sensor receives a message, freeze the robot
    Line = messages.line_middle
    if  Line == True:
        while(True):
            move.angular.z = 0 
            move.linear.x = 0
    
    
def subscriber():
    rospy.Subscriber("/cop/prox_sensors", prox_sensor, feedback, queue_size=1)
    rospy.Subscriber("/cop/line_sensors", line_sensor, feedback2)
    
    
if __name__ == '__main__':
    rospy.init_node("robot_controller")
    rospy.loginfo("Node has been started")
    rate = rospy.Rate(0.1)

    pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
    subscriber()

    while not rospy.is_shutdown():

        pub.publish(move)

    rospy.spin()
