import cv2
import numpy as np
# from matplotlib import pyplot as plt

import sys


img = cv2.imread(sys.argv[1])
hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

# hist, xbins, ybins = np.histogram2d(hsv[0].ravel(),hsv[1].ravel(),[180,256],[[0,180],[0,256]])
#
# print hist
#
# print xbins
#
# print ybins

hist = cv2.calcHist([hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])


import pdb

pdb.set_trace()