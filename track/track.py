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
        
        tracker = cv2.TrackerMedianFlow_create()
        tracker_name = str(tracker).split()[0][1:]

        #webカメラの軌道に時間がかかる場合
        #time.sleep(1)

        et, frame = camera.read()

        roi = cv2.selectROI(frame, False)

        ret = tracker.init(frame, roi)

        while True:

            ret, frame = camera.read()

            success, roi = tracker.update(frame)

            (x,y,w,h) = tuple(map(int,roi))
    
            if success:
                p1 = (x, y)
                p2 = (x+w, y+h)
                cv2.rectangle(frame, p1, p2, (0,255,0), 3)
            else :
                cv2.putText(frame, "Tracking failed!!", (500,400), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),3)
                move.move(0,'no')
            #cv2.imshow(tracker_name, frame)
            
            '''tuika ultra @ servo'''
            kk = int(ultra.ultra())
            xx = x + (w/2)
            xx = 600-xx
            print(kk)
            pam =  (xx/400) * 180 + 270
            if kk > 13:
                if pam > 450:
                    ang = 450
                    servo.cameraturn(ang)
                    move.move(60,'forward')
                elif pam < 270:
                    ang = 270
                    servo.cameraturn(ang)
                    move.move(60,'forward')
                else:
                    ang = int(pam)
                    servo.cameraturn(ang)
                    move.move(60,'forward')
            else:
                move.move(0,'no')
                #move.motorStop()
            ''''''
            
            k = cv2.waitKey(1) & 0xff
            if k == 27 :
                break
            
            yield cv2.imencode('.jpg', frame)[1].tobytes()

        camera.release()