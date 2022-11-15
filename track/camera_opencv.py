import os
import cv2
from base_camera import BaseCamera
import numpy as np
import time
import servo
import RPi.GPIO as GPIO
import GUImove as move

colorUpper = np.array([20, 255, 255])
colorLower = np.array([0, 0, 0])
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
            # read current frame
            _, img = camera.read()
            
            threshold=60
            img2 = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            ret, img2 = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
            
            
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(img2, colorLower, colorUpper)
            
            img2 = cv2.rectangle(img2,(0,0),(640,250),(255,255,255),-1)
            
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
                print('Target color object detected')
                print('X:%d'%X)
                print('Y:%d'%Y)
                print('-------')
                ##tuika##
                if 250<X<350:
                    servo.turnMiddle()
                    move.move(60,'forward')
                elif 250>X:
                    servo.turnRight()
                    move.move(60,'forward')
                elif 350<X:
                    servo.turnLeft()
                    move.move(60,'forward')
                ### 
                cv2.putText(img,'Target Detected',(40,60), font, 0.5,(255,255,255),1,cv2.LINE_AA)
                cv2.rectangle(img,(int(box_x-radius),int(box_y+radius)),(int(box_x+radius),int(box_y-radius)),(255,255,255),1)
            #elif len(cnts) > 2:
                #print(cnts)
            else:
                servo.turnMiddle()
                move.move(60,'backward')
                cv2.putText(img,'Target Detecting',(40,60), font, 0.5,(255,255,255),1,cv2.LINE_AA)
                print('No target color object detected')
                
                
            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()

