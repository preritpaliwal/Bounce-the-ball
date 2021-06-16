import math 
import cv2
import numpy as np 

kernel=np.ones((3,3),dtype=np.uint8)
x,y=50,50
kx=0
ky=0
sx=5
sy=5
kz=1
score = 0
white = [255,255,255]
red  = [0,0,255]

def compare(a,b):
    z=0
    for i in range(3):
        if a[i] == b[i]:
            z+=1
    if z == 3:
        return 1
    else:
        return 0

def modify(x,y):
    global kx, ky,sx,sy,kz
    t = 0 
    if y+31>=hor.shape[0]:
        kz=0
        return x,y,t
    elif y-31<0:
        ky=0
    if x+31>= hor.shape[1] :
        kx=1
    elif x-31<0 :
        kx=0
    if kx==0:
        x= x+sx
    elif kx==1:
        x=x-sx
    if ky==1:
        y=y-sy
    elif ky==0:
        y=y+sy
    # print(x,y,kz)
    # print(hor.shape)
    if compare(hor[y+29][x],white):
        ky = 1
        t = 1
    return x,y,t

def show(x,y):
    cv2.circle(hor,(x,y),30,red,thickness=-1)

def remove(x,y):
     cv2.circle(hor,(x,y),30,(0,0,0),thickness=-1)

img1= np.zeros((300,1200,3), dtype=np.uint8)
cap = cv2.VideoCapture(0)

while(cap.isOpened()):
    ret, img = cap.read()
    crop_img = cv2.resize(img,(1200,350), interpolation=cv2.INTER_AREA)
    # crop_img= cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    crop_img=cv2.morphologyEx(crop_img,cv2.MORPH_GRADIENT,kernel)
    ret, crop_img=cv2.threshold(crop_img,20,255,cv2.THRESH_BINARY)
    hor= np.concatenate((img1,crop_img),axis = 0)
    show(x,y)
    # cv2.namedWindow('woww', cv2.WINDOW_NORMAL)
    cv2.imshow('woww',hor)
    remove(x,y)
    x,y,t=modify(x,y)
    score +=t
    if kz == 0:
        hor=cv2.putText(hor, "GAME OVER", (250,300), cv2.FONT_HERSHEY_COMPLEX, 3.0, red, thickness=10)
        hor=cv2.putText(hor, f"score : {score}", (290,400), cv2.FONT_HERSHEY_COMPLEX, 3.0,red, thickness=10)
        cv2.imshow('woww',hor)
        cv2.waitKey(0)
        break
    if cv2.waitKey(1) == 27:
        break