import sys
import numpy as np
import cv2

src = sys.argv[1]

print src

# img = cv2.imread(src)
# gray = cv2.imread(src,0)

# orig = cv2.imread(src)

img = cv2.imread(src,0)
img = cv2.medianBlur(img,5)
 
ret,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,2)
th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)


cv2.imshow('gray',img)
cv2.waitKey(0)

cv2.imshow('global',th1)
cv2.waitKey(0)

cv2.imshow('adatpt mean',th1)
cv2.waitKey(0)


cv2.imshow('gaussian',th3)
cv2.waitKey(0)