#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from mavros_msgs.msg import WaypointReached
from mavros_msgs.msg import MountControl
from sensor_msgs.msg import Image

from cv_bridge import CvBridge 
import cv2
import numpy as np
import tensorflow as tf
from std_msgs.msg import String
from matplotlib import pyplot 


class Cap_imag:
    
    def __init__(self):
        rospy.loginfo("init node")
        rospy.Subscriber("/mavros/mission/reached",WaypointReached,self.Waypoint_Reached_Calback)
        rospy.Subscriber("/iris_gimbal/usb_cam/image_raw", Image, self.Image_Calback)
        self._cv_bridge=CvBridge()
        self.last_id=0
        self.capture_image=0
        self.pub=rospy.Publisher('/mavros/mount_control/command', MountControl, queue_size=10)
        self.cmd=MountControl()
        
                                        
    def Image_Calback(self,image):
        if self.capture_image:
            self.capture_image=0
            cv_image=self._cv_bridge.imgmsg_to_cv2(image, "bgr8")
            cv_image=cv2.resize(cv_image,(227,227))
            name="/home/andres1407/Capture_px4/pradera_1_0/Captura_No_"+str(self.last_id)+".png"
            cv2.imwrite(name,cv_image)
            rospy.loginfo("captura de imagen "+str(self.last_id))
    
    def Waypoint_Reached_Calback(self,waypoint):
        if((self.last_id!=waypoint.wp_seq) and (self.capture_image==0)):
            self.last_id=waypoint.wp_seq
            self.capture_image=1
    def upload(self):
        self.cmd.header.stamp=rospy.Time.now()
        self.cmd.header.frame_id="map"
        self.cmd.mode=2
        self.cmd.pitch=90
        
def capture_for_px4():
    rospy.init_node('capture_for_px4', anonymous=True)
    cap=Cap_imag()
    rate=rospy.Rate(1)
    while not rospy.is_shutdown():
        cap.upload()
        rate.sleep()
    
    
if __name__ == '__main__':
    try:
        capture_for_px4()
    except rospy.ROSInterruptException:
        exit()

    
    