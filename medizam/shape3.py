import sys
import numpy as np
import cv2

src = sys.argv[1]

print src

# img = cv2.imread(src)
# gray = cv2.imread(src,0)

# orig = cv2.imread(src)

img = cv2.imread(src,0)

thumbnail = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
# cv2.Resize(img, thumbnail)

img = thumbnail

img = cv2.medianBlur(img,5)
 
ret,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,2)
th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)



use = th3

cv2.imshow('used',use)
cv2.waitKey(0)


contours,h = cv2.findContours(use,1,2)

for cnt in contours:
    approx = cv2.approxPolyDP(cnt,0.1*cv2.arcLength(cnt,True),True)
    print len(approx)
    if len(approx)==5:
        print "pentagon"
        cv2.drawContours(use,[cnt],0,255,-1)
    elif len(approx)==3:
        print "triangle"
        cv2.drawContours(use,[cnt],0,(0,255,0),-1)
    elif len(approx)==4:
        print "square"
        cv2.drawContours(use,[cnt],0,(0,0,255),-1)
    elif len(approx) == 9:
        print "half-circle"
        cv2.drawContours(use,[cnt],0,(255,255,0),-1)
    elif len(approx) > 15:
        print "circle"
        cv2.drawContours(use,[cnt],0,(0,255,255),-1)

# im = cv2.imread(src)
# imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
# ret,thresh = cv2.threshold(imgray,127,255,0)
#
# image, contours, hierarchy = cv2.findContours(th3,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#
# img = cv2.drawContour(img, contours, -1, (0,255,0), 3)


cv2.imshow('gray',img)
cv2.waitKey(0)

cv2.imshow('global',th1)
cv2.waitKey(0)

cv2.imshow('adatpt mean',th1)
cv2.waitKey(0)


cv2.imshow('gaussian',th3)
cv2.waitKey(0)

cv2.imshow('used',use)
cv2.waitKey(0)