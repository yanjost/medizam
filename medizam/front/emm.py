#Import OpenCv library
from cv2 import *

import sys

### HISTOGRAM FUNCTION #########################################################
def calcHistogram(src):
    # Convert to HSV
    hsv = cv.CreateImage(cv.GetSize(src), 8, 3)
    cv.CvtColor(src, hsv, cv.CV_BGR2HSV)

    # Extract the H and S planes
    size = cv.GetSize(src)
    h_plane = cv.CreateMat(size[1], size[0], cv.CV_8UC1)
    s_plane = cv.CreateMat(size[1], size[0], cv.CV_8UC1)
    cv.Split(hsv, h_plane, s_plane, None, None)
    planes = [h_plane, s_plane]

    #Define numer of bins
    h_bins = 30
    s_bins = 32

    #Define histogram size
    hist_size = [h_bins, s_bins]

    # hue varies from 0 (~0 deg red) to 180 (~360 deg red again */
    h_ranges = [0, 180]

    # saturation varies from 0 (black-gray-white) to 255 (pure spectrum color)
    s_ranges = [0, 255]

    ranges = [h_ranges, s_ranges]

    #Create histogram
    hist = cv.CreateHist([h_bins, s_bins], cv.CV_HIST_ARRAY, ranges, 1)

    #Calc histogram
    cv.CalcHist([cv.GetImage(i) for i in planes], hist)

    cv.NormalizeHist(hist, 1.0)

    #Return histogram
    return hist

### EARTH MOVERS ############################################################
def calcEM(hist1,hist2,h_bins,s_bins):

    #Define number of rows
    numRows = h_bins*s_bins

    sig1 = cv.CreateMat(numRows, 3, cv.CV_32FC1)
    sig2 = cv.CreateMat(numRows, 3, cv.CV_32FC1)

    for h in range(h_bins):
        for s in range(s_bins):
            bin_val = cv.QueryHistValue_2D(hist1, h, s)
            cv.Set2D(sig1, h*s_bins+s, 0, cv.Scalar(bin_val))
            cv.Set2D(sig1, h*s_bins+s, 1, cv.Scalar(h))
            cv.Set2D(sig1, h*s_bins+s, 2, cv.Scalar(s))

            bin_val = cv.QueryHistValue_2D(hist2, h, s)
            cv.Set2D(sig2, h*s_bins+s, 0, cv.Scalar(bin_val))
            cv.Set2D(sig2, h*s_bins+s, 1, cv.Scalar(h))
            cv.Set2D(sig2, h*s_bins+s, 2, cv.Scalar(s))

    #This is the important line were the OpenCV EM algorithm is called
    return cv.CalcEMD2(sig1,sig2,cv.CV_DIST_L2)

def equalizeRgb(img):
    #import pdb;pdb.set_trace()
    ycrcb = cvtColor(cv2array(img), cv.CV_RGB2YCrCb)
    channels = split(ycrcb)

    equalizeHist(channels[0], channels[0])

    merge(channels, ycrcb)

    return array2cv(cvtColor(ycrcb, cv.CV_YCrCb2RGB))
    # import numpy as np
    # r,g,b = split(img)
    # equalizeHist(r,r)
    # equalizeHist(g,g)
    # equalizeHist(b,b)
    #
    # blank_image = np.zeros((img.height,img.width,3), np.uint8)
    #
    # merge([r,g,b],blank_image)
    #
    # return blank_image

### MAIN ########################################################################
def emm(src1,src2):
    # #Load image 1
    src1 = cv.LoadImage(src1)
    #
    # #Load image 2
    src2 = cv.LoadImage(src2)

    #normalize

    # cv.EqualizeHist(src1,src1)
    # cv.EqualizeHist(src2,src2)
    #src1 = equalizeRgb(src1)
    #src2 = equalizeRgb(src2)

    imwrite("tmp/equalized.jpg",cv2array(src2))

    # Get histograms
    histSrc1= calcHistogram(src1)
    histSrc2= calcHistogram(src2)

    # Compare histograms using earth mover's
    histComp = calcEM(histSrc1,histSrc2,30,32)

    #Print solution
    return histComp


def cv2array(im):
    import numpy as np

    depth2dtype = {
        cv.IPL_DEPTH_8U: 'uint8',
        cv.IPL_DEPTH_8S: 'int8',
        cv.IPL_DEPTH_16U: 'uint16',
        cv.IPL_DEPTH_16S: 'int16',
        cv.IPL_DEPTH_32S: 'int32',
        cv.IPL_DEPTH_32F: 'float32',
        cv.IPL_DEPTH_64F: 'float64',
    }

    arrdtype = im.depth
    a = np.fromstring(
        im.tostring(),
        dtype=depth2dtype[im.depth],
        count=im.width * im.height * im.nChannels)
    a.shape = (im.height, im.width, im.nChannels)
    return a


def array2cv(a):
    dtype2depth = {
        'uint8': cv.IPL_DEPTH_8U,
        'int8': cv.IPL_DEPTH_8S,
        'uint16': cv.IPL_DEPTH_16U,
        'int16': cv.IPL_DEPTH_16S,
        'int32': cv.IPL_DEPTH_32S,
        'float32': cv.IPL_DEPTH_32F,
        'float64': cv.IPL_DEPTH_64F,
    }
    try:
        nChannels = a.shape[2]
    except:
        nChannels = 1
    cv_im = cv.CreateImageHeader((a.shape[1], a.shape[0]),
                                 dtype2depth[str(a.dtype)], nChannels)
    cv.SetData(cv_im, a.tostring(), a.dtype.itemsize * nChannels * a.shape[1])
    return cv_im