import sys
import numpy as np
import cv2

src = sys.argv[1]

print src

img = cv2.imread(src)
gray = cv2.imread(src,0)

orig = cv2.imread(src)

# img = cv2.multiply(img, np.array([1,2,3]))
# img = cv2.reshape(1)

ret,thresh = cv2.threshold(gray,128,255,1)


# imgAdThreshold = cv2.Mat(imgInput.cols, imgInput.rows, IPL_DEPTH_8U, 1);

# ret,thresh = cv2.adaptativeThreshold(gray, )

contours,h = cv2.findContours(thresh,1,2)

for cnt in contours:
    approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
    print len(approx)
    if len(approx)==5:
        print "pentagon"
        cv2.drawContours(img,[cnt],0,255,-1)
    elif len(approx)==3:
        print "triangle"
        cv2.drawContours(img,[cnt],0,(0,255,0),-1)
    elif len(approx)==4:
        print "square"
        cv2.drawContours(img,[cnt],0,(0,0,255),-1)
    elif len(approx) == 9:
        print "half-circle"
        cv2.drawContours(img,[cnt],0,(255,255,0),-1)
    elif len(approx) > 15:
        print "circle"
        cv2.drawContours(img,[cnt],0,(0,255,255),-1)

cv2.imshow('gray',gray)
cv2.waitKey(0)
cv2.imshow('thresh',thresh)
cv2.waitKey(0)
cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()