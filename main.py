import cv2
import pickle
import cvzone
import numpy as np

# video feed
cap = cv2.VideoCapture('carPark.mp4')    # upload the video using cv2 library

with open('CarParkPos', 'rb') as f:   # we will need stored position of car so that's why we will need the file
    posList = pickle.load(f)

width, height = 107, 48


def checkParkingSpace(imgProcessed):           # this will help us to crop the image and show us if car is present in that position
    spaceCounter=0
    for pos in posList:
        x,y = pos

        imgCrop = imgProcessed[y:y+height,x:x+width]   # crop the image
        #cv2.imshow(str(x*y),imgCrop)                  # this will separately show each and every img position present in img/video
        count=cv2.countNonZero(imgCrop)               # this will give count of pixel
        cvzone.putTextRect(img,str(count),(x,y+height-3),scale=1.5,thickness=2, offset=0,colorR=(0,0,255))         # we will show count of pixel on every box

        if count <900:              # car is not present
           color = (0,255,0)      # change the color were car is not present
           thickness=10
           spaceCounter +=1       # this will count number of vacant places
        else:
           color = (0,0,255)
           thickness = 2


        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height),color, 2)      #it will display the img with position width height color after all img processing is done
        cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1.5, thickness=2, offset=0, colorR=color)
        cvzone.putTextRect(img, f'Free : {spaceCounter}/{len(posList)}',(100,50), scale=3, thickness=5, offset=20, colorR=(0, 200, 0))   # this will display spacecounter
while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):    # this will tell us frame position and total count of frames present in video
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)                                        # reset the frames to original position and restart the video

    success, img = cap.read()
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)   # this will convert or change color
    imgBlur = cv2.GaussianBlur(imgGray,(3,3),1)       #blur the img
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                          cv2.THRESH_BINARY_INV, 25,16)               # this will convert img to binary format and this will convert  block present in img into binary format
    imgMedian = cv2.medianBlur(imgThreshold ,5)
    kernel = np.ones((3,3),np.uint8)   # this will extract important portion of img and also  it can detect the edge of img  we cannot directly access kernel so to access we have to use numpy
    imgDilate= cv2.dilate(imgMedian,kernel,iterations=1)   # this will make pixel thicker so that we can able to differentiate vacant or not vacant

    checkParkingSpace(imgDilate)  # we will pass imgDilate to this function so this will crop this imgDilate and this is what we want to do


    cv2.imshow("Image", img)         # it will read the image and show the image contionusly
    #cv2.imshow("ImageBlur", imgBlur) # this are some operation we have to do which will help us to know if car is present or not and here img will display in gray color
    #cv2.imshow("ImageThreshold", imgThreshold)   # we first convert img into blur img and in gray then we convert img into some black type picture using adaptive Threshold and taking some values of gausssian threshold adaptive and due to this we saw that ,In output were car is present there is high pixel and were car is not present there are low pixel and hence this will be very useful to identify whether car is present or not
    #cv2.imshow("ImageMedian", imgMedian)       # we saw in imgThreshold that there are some unnecessary pixel prsent in img so toremove it we will use imgMrdian  this will remove unwanted pixel
    cv2.waitKey(3)                   # delay the video