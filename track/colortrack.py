import cv2
import os
from base_camera import BaseCamera
import numpy as np
import time
import servo
import RPi.GPIO as GPIO
import GUImove as move
import GUImove as motorStop
import ultra
#import move
colorUpper = np.array([100, 255, 200])
colorLower = np.array([85, 200, 100])
font = cv2.FONT_HERSHEY_SIMPLEX

class Camera(BaseCamera):
    video_source = 0
    
    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super(Camera, self).__init__()
        
    def setup():
        move.setup()
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(Camera.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')
        
        while True:
            _, img = camera.read()
            
            #hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, colorLower, colorUpper)
            #img2 = cv2.rectangle(img2,(0,0),(640,250),(255,255,255),-1)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
            center = None 
            if len(cnts) > 0:
                c = max(cnts, key=cv2.contourArea)
                ((box_x, box_y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                X = int(box_x)
                Y = int(box_y)
                #print('Target color object detected')
                print('X:%d'%X)
                #print('Y:%d'%Y)
                #print('-------')
                ##tuika##
                kk = int(ultra.ultra())
                #print(kk)
                Xc=X-600
                pam =  (Xc/400) * 180 + 270
                if kk > 13:
                    if pam > 450:
                        ang = 450
                        servo.cameraturn(ang)
                        move.move(80,'forward')
                    elif pam < 270:
                        ang = 270
                        servo.cameraturn(ang)
                        move.move(80,'forward')
                    else:
                        ang = int(pam)
                        servo.cameraturn(ang)
                        move.move(80,'forward')
                else:
                    move.move(0,'no')
                ### 
                cv2.putText(img,'Target Detected',(40,60), font, 0.5,(255,255,255),1,cv2.LINE_AA)
                cv2.rectangle(img,(int(box_x-radius),int(box_y+radius)),(int(box_x+radius),int(box_y-radius)),(255,255,255),1)
            #elif len(cnts) > 2:
                #print(cnts)
            else:
                servo.turnMiddle()
                #move.move(60,'backward')
                cv2.putText(img,'Target Detecting',(40,60), font, 0.5,(255,255,255),1,cv2.LINE_AA)
                print('No target color object detected')
                
                
            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()