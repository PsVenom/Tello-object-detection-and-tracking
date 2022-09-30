import geopy
import geopy.distance
import math
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
configPath = 'model_mobilenet.pbtxt'
weightsPath = "frozen_inference_graph.pb"

net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320, 320)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)


def calc_coord(P_x, P_y, alti, fov_x=67.14791 , fov_y=59.7846, f_h=720, f_w=960):
    h=alti
    #Pixel coordinates to coordinates from origin
    f_x=P_x-f_w/2
    f_y=f_h-P_y
    #Degrees to radians
    theta_x = fov_x*math.pi/180
    theta_y = fov_y*math.pi/180
    #Calculate real world coordinates
    x= (2*h*f_h*math.tan(theta_x/2)*f_x)/(f_w*(f_h-2*f_y)*math.tan(theta_y/2))
    y= (h*f_h)/(math.tan(theta_y/2)*(f_h-2*f_y))
    print("Coordinates of object:",x,y)
    return (x,y)

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
    if key == 'p':
        me.stop()
    
    return [lr, fb, ud, yv]

def object_detection(img):
    classIds, confs, bbox = net.detect(img, confThreshold=thres, nmsThreshold=nmsThres)
    try:
        for classId, conf, box in zip(classIds.flatten(), confs.flatten(), bbox):
         if classNames[classId - 1].lower() == 'laptop':
            cvzone.cornerRect(img, box)
            cv2.circle(img, (int(box[0]+box[2]/2),int(box[1]+box[3]/2)), 10, [0,255,0], 15)
            cv2.putText(img, f'{classNames[classId - 1].upper()} {round(conf * 100, 2)}',
                        (box[0] + 10, box[1] + 30), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                        1, (0, 255, 0), 2)
            print("Object being detected is: ", classNames[classId - 1])
            cv2.imshow("Image", img)
            cv2.waitKey(1)
            return (box[0]+box[2]/2, box[1]+box[3]/2)
         else:
             cv2.imshow("Image", img)
             cv2.waitKey(1)
             return(0,0)
    except:
        cv2.imshow("Image", img)
        cv2.waitKey(1)
        return (0,0)

while True:
    #vals = getKeyboardInput()
    #me.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    img = me.get_frame_read().frame
    cv2.imshow("Image", img)
    #alti= me.get_height()
    alti = 15
    print("Height: ",alti)
    a = object_detection(img)
    calc_coord(a[0],a[1],alti)
    print('centroid coordinates:',a[0],a[1])

