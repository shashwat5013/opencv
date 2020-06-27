import numpy as np
import  cv2

def empty(a):
    pass

############################################
#  FINDING COLOUR OF PEN INFRONT OF CAMERA #
############################################

def findColour(img,myColors,myColorValues):
    imgHsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    count=0
    newPoints=[]
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        print(lower,upper)
        mask = cv2.inRange(imgHsv, lower, upper)
        x,y=getContours(mask)
        colouredmask = cv2.bitwise_and(img, img, mask=mask)
        cv2.circle(imgResult,(x,y),5,myColorValues[count],10,cv2.FILLED)
        if x!=0 or y!=0:
            newPoints.append([x,y,count])
        count+=1
    return newPoints

##################################
# CONTOURS FOR DETECTION OF PENS #
##################################

def getContours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>500:
            cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2,y


##############################
#  DRAWING CIRCLES ON CANVAS #
##############################

def drawOnCanvas(myPoints,myColorValues):
    for point in myPoints:
        cv2.circle(imgResult,(point[0],point[1]),10,myColorValues[point[2]],20,cv2.FILLED)


cap=cv2.VideoCapture(0)
cap.set(3,1080)
cap.set(4,1080)

#######################################################
# SETTING HUE,SATURATION,VALUES OF DIFFERENT OBJECTS  #
#######################################################
myColors=[[20,136,150,33,255,255],[56,75,149,92,155,210],[154,48,146,175,131,217]]
        #       yellow                      green                      pink
myColorValues=[[0,255,255],              [0,255,0],                [102,0,255]]
        #       yellow                      green                      pink
myPoints=[]     # x  y myColorValuesID


while True:
    success,img=cap.read()
    imgResult=img.copy()
    newPoints=findColour(img,myColors,myColorValues)
    if len(newPoints)!=0:
       myPoints.extend(newPoints)
    if len(myPoints)!=0:
        drawOnCanvas(myPoints,myColorValues)
    cv2.imshow("image", imgResult)
    input_ =cv2.waitKey(1)
    if input_ & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()