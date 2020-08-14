import cv2
import numpy as np
cap = cv2.VideoCapture(0)
img = np.zeros((1024,1024,3), np.uint8)
def draw_circle(cnt,x,y):
    if (len(cnt)>0):
        cv2.circle(img,(x,y),10,(0,255,0),-1)
address = "http://192.168.43.1:8080/video"
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap.open(address)
kernel = np.ones((5, 5), np.uint8)
if (cap.isOpened()== False):
    print("Error opening video stream or file")


cv2.namedWindow("frame",cv2.WINDOW_NORMAL)

while(1):
# Take each frame
    _, frame = cap.read()

# Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
# define range of blue color in HSV
    blueLower = np.array([100, 60, 60])
    blueUpper = np.array([140, 255, 255])

    blueMask = cv2.inRange(hsv, blueLower, blueUpper)
    #cv2.imshow('blueMask',blueMask)
    blueMask = cv2.erode(blueMask, kernel, iterations=2)
    #cv2.imshow('blueMask',blueMask)
    blueMask = cv2.morphologyEx(blueMask, cv2.MORPH_OPEN, kernel)
    #cv2.imshow('blueMask',blueMask)
    blueMask = cv2.dilate(blueMask, kernel, iterations=1)
    #cv2.imshow('blueMask',blueMask)

    cnt, hierarchy = cv2.findContours(blueMask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if(len(cnt)>0):
        cnt =max(cnt, key = cv2.contourArea)

        (x,y),radius = cv2.minEnclosingCircle(cnt)
        center = (int(x),int(y))
        radius = int(radius)
        frame = cv2.circle(frame,center,radius,(0,255,0),2)
        draw_circle(cnt,int(x),int(y))
    cv2.imshow('img',img)
    cv2.imshow('frame',frame)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break


cap.release()
cv2.destroyAllWindows()
