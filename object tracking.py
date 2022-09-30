import cv2
import cvzone
from djitellopy import tello

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
cap = cv2.VideoCapture(0)
def object_detection(img):
    x = img.shape[1]
    y = img.shape[0]
    classIds, confs, bbox = net.detect(img, confThreshold=thres, nmsThreshold=nmsThres)
    cv2.line(img, (int(x/3), 0), (int(x/3), y), (255, 0, 0))
    cv2.line(img, (int(2*x/3), 0), (int(2*x/3), y), (255, 0, 0))
    try:
        for classId, conf, box in zip(classIds.flatten(), confs.flatten(), bbox):
            #if classNames[classId - 1].lower() == 'laptop':
                cvzone.cornerRect(img, box)
                cv2.circle(img, (int(box[0]+box[2]/2), int(box[1]+box[3])), 6, [0, 255, 0], 15)
                cv2.putText(img, f'{classNames[classId - 1].upper()} {round(conf * 100, 2)}',
                            (box[0] + 10, box[1] + 30), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                            1, (0, 255, 0), 2)
                print("Object being detected is: ", classNames[classId - 1])
                cv2.imshow("Image", img)
                cv2.waitKey(1)
                return (box[0]+box[2]/2, box[1]+box[3]/2), (box[0]-box[2])*(box[1]-box[3])/(img.shape[0]*img.shape[1])
    except:
        cv2.imshow("Image", img)
        cv2.waitKey(1)
        return (0, 0), 0

def tracker(x):
    bb, area = object_detection(x)
    print(area)
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 30
    if bb[0] > x.shape[1] / 3 and bb[0] < 2 * (x.shape[1]) / 3:
        print('optimum yaw, mkc')
    elif bb[0] < x.shape[1] / 3 and bb[0]>0:
        print('MOVE TO DA LEFT')
        yv = speed
    elif bb[0] > 2 * (x.shape[1]) / 3:
        print("Move to the Right bc")
        yv = - speed
    elif bb[0]==0:
        print('exceptional case, object not in sight')
        #add code to make a full rotation
    if area >= 0.4 and area <0.8:
        print('optimum distance, changing yaw')
    elif area < 0.4 and area > 0:
        print('TOO FAR, APPROACHING OBJECT')
        fb = speed

    elif area > 0.95:
        print('TOO CLOSE, MOVING BACK')
        fb = -speed
    elif area <= 0:
        print('exceptional case, probably no object in sight')

    me.send_rc_control(lr, fb, ud, yv)


me.takeoff()
while True:
 try:
    ret, img = cap.read()
    tracker(img)
 except KeyboardInterrupt as e:
     print('MISSION ABORT')
     me.land()


