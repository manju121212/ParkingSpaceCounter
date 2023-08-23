import cv2
import pickle

# img = cv2.imread('carParkImg.png') --       # if we put img over here then once we assign anything on that cannot be deleted
                                              # and we don't want that but basically in web camera we can delete it because every time
                                              # img is generated but now we want this img to be called repeately in program so we will place
                                              # this position in while loop.
try:
   with open('CarParkPos', 'rb') as f:        # what this will do is all previous files data if present then it will store in posList so due to this
       posList = pickle.load(f)                # all files will remain intact
except:
   posList=[]                                # every position in parking space we are going to put over here
                                             # and every position will have x,y coordinate.
width,height=107,48


def mouseClick(events,x,y,flags,params) :
    if events == cv2.EVENT_LBUTTONDOWN:        #left click to mark position in img and append in poslist.
        posList.append((x,y))
    if events==cv2.EVENT_RBUTTONDOWN:          # right click to delete possition in img and in poslist.
        for i,pos in enumerate(posList):       # if we mark already that position then if we left click then it should
           x1,y1=pos;                          # delete that position if we already marked.
           if x1<x<x1+width and y1<y<y1+height: # if position is already marked then we need to delete but we want
               posList.pop(i)                   # position in poslist so we need (enumerate) so that it can tell position


    with open('CarParkPos','wb') as f:
        pickle.dump(posList,f)        # copy all values from poslist and store in file using pickle obj(dump)
                                      # but one problem is that when we are re-running the program file is overwriting
                                      # to avoid this we will store all values before running again program
while True:
    # cv2.rectangle(img,(50,192),(157,240),(255,0,255),2) -- it was demo to identify Perfect size rectangle for
    # parking spot.
    img = cv2.imread('carParkImg.png')
    for pos in posList:
        cv2.rectangle(img, pos,(pos[0] + width,pos[1] + height),(255,0,255),2)

    cv2.imshow("Image",img)
    cv2.setMouseCallback("Image" , mouseClick)
    cv2.waitKey(50)

