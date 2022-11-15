import os
import cv2
from base_camera import BaseCamera
import numpy as np
import time
import servo
import RPi.GPIO as GPIO
import GUImove as move

import cv2 as cv

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
            #hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            #add------------------------------------------------------------------------------------
            grayimg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            custom_cascade = cv.CascadeClassifier('./cascade/dogtest2.xml')
            custom_rect = custom_cascade.detectMultiScale(grayimg, scaleFactor=1.3, minNeighbors=2, minSize=(1, 1))
            print(custom_rect)
            if len(custom_rect) > 0:
                for rect in custom_rect:
                    cv.rectangle(img, tuple(rect[0:2]), tuple(rect[0:2]+rect[2:4]), (0, 0, 255), thickness=3)

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()

