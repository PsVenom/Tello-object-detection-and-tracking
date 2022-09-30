import geopy
import geopy.distance
#from math import *
import numpy as np
import cv2
import cvzone
#from calc_gps import gps
import time
import torch
import pandas
import json

from djitellopy import tello
import keyboard as kp
from time import sleep

me = tello.Tello()
me.connect()
print(me.get_battery())
me.streamon()

thres = 0.5
nmsThres = 0.2
classNames = []
classFile = 'coco.names'
with open(classFile, 'rt') as f:
    classNames = f.read().split('\n')
print(classNames)
configPath = 'yolo.pbtxt'
weightsPath = "frozen_inference_graph.pb"

net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320, 320)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 30
    key = kp.read_key()
    #if kp.getKey("e"):
    if key == 'a':
        yv = -speed
    elif key == 'd':
        yv = speed
    if key == 'j':
        lr = -speed
    elif key == 'l':
        lr = speed
    if key == 'i':
        fb = speed
    elif key == 'k':
        fb = -speed
    if key == 'w':
        ud = speed
    elif key == 's':
        ud = -speed
    if key == 'q':
        me.land()
        sleep(3)
    if key == 't':
        me.takeoff()
    
    return [lr, fb, ud, yv]

def update_cordinates(cordinates):
    fileObject = open('/home/rithwick11111/Desktop/GlobalHawks/coordinates.json', 'w+')
    jsonData = json.dumps(cordinates)
    fileObject.write(jsonData)
    fileObject.close()

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
            cv2.imshow("Image", img)
            cv2.waitKey(1)
            centroid = int(box[0]+box[2]/2), int(box[1]+box[3]/2)
            if centroid==[]:
                update_cordinates([0,0])
                return [0,0]
            else:
                update_cordinates(centroid)
                return centroid

    except:
        cv2.imshow("Image", img)
        cv2.waitKey(1)
        return [0,0]

while True:
    vals = getKeyboardInput()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    img = me.get_frame_read().frame
    img = cv2.resize(img, (640,480))
    cv2.imshow("Image", img)
    #sleep(0.1)
    count = 0
    count = count + 1
    if count == 1:
        count+=1
        a = object_detection(img)
        print('centroid coordinates:',a[0],a[1])
    elif count == 2:
        a = object_detection_target(img)
        print('centroid coordinates:',a[0],a[1])


