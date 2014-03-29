import sys
import numpy as np
import cv2

src = sys.argv[1]

print src


im = cv2.imread(src)
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

cv2.imshow('gray',imgray)
cv2.waitKey(0)

# ret,thresh = cv2.threshold(imgray,127,255,0)

thresh = cv2.adaptiveThreshold(imgray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)

cv2.imshow('thresh',thresh)
cv2.waitKey(0)


image, contours = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

img = cv2.drawContours(im, contours, -1, (0,255,0), 3)


cv2.imshow('gray',img)
cv2.waitKey(0)
