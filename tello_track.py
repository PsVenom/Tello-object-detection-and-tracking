import cv2
import cvzone
from calc_gps import gps
import time
import numpy as np
import keyboard
from djitellopy import Tello
from threading import Thread
tello = Tello()
tello.connect()
tello.streamon()
frame_read = tello.get_frame_read()
thres = 0.55
nmsThres = 0.2
classNames = []
classFile = 'coco.names'
with open(classFile, 'rt') as f:
    classNames = f.read().split('\n')
print(classNames)
configPath = 'model_mobilenet.pbtxt'
weightsPath = "frozen_inference_graph.pb"

net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320, 320)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)
def object_detection(img):
    classIds, confs, bbox = net.detect(img, confThreshold=thres, nmsThreshold=nmsThres)
    try:
        for classId, conf, box in zip(classIds.flatten(), confs.flatten(), bbox):
            cvzone.cornerRect(img, box)
            cv2.circle(img, (int(box[0]+box[2]/2),int(box[1]+box[3]/2)), 10, [0,255,0], 15)
            cv2.putText(img, f'{classNames[classId - 1].upper()} {round(conf * 100, 2)}',
                        (box[0] + 10, box[1] + 30), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                        1, (0, 255, 0), 2)
            print("Object being detected is: ", classNames[classId - 1])
            cv2.imshow("drone", img)
            return (box[0]+box[2]/2, box[1]+box[3]/2)

    except:
        cv2.imshow("drone", img)
        return (-1,-1)
def show():
    while True:
        img = frame_read.frame

        object_detection(img)
        cv2.waitKey(1)
def key():
    while True:
        # In reality you want to display frames in a seperate thread. Otherwise
        #  they will freeze while the drone moves.
      try:
        if keyboard.is_pressed('t'):
            tello.connect()
            tello.takeoff()
        elif keyboard.is_pressed('enter'):
            tello.land()
        elif keyboard.is_pressed('w'):
            print('w')
            tello.move_forward(30)
        elif keyboard.is_pressed('s'):
            print('s')
            tello.move_back(10)
        elif keyboard.is_pressed('a'):
            print('a')
            tello.move_left(10)
        elif keyboard.is_pressed('d'):
            print('d')
            tello.move_right(10)
        elif keyboard.is_pressed('e'):
            print('d')
            tello.rotate_clockwise(10)
        elif keyboard.is_pressed('q'):
            print('q')
            tello.rotate_counter_clockwise(10)
        elif keyboard.is_pressed('r'):
            print('r')
            tello.move_up(10)
        elif keyboard.is_pressed('f'):
            print('f')
            tello.move_down(10)
      except Exception as e:
          print('command exception, shutting down')
          tello.land()
          continue


a = Thread(target = key)
b = Thread(target = show)
a.start()
b.start()
a.join()
b.join()
