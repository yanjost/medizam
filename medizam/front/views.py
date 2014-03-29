import json
import django.http
from django.shortcuts import render

from django.http import HttpResponse, HttpResponseNotFound

# Create your views here.
import django.views.generic

from django.views.decorators.csrf import csrf_exempt

from django.core.urlresolvers import reverse

import os

import cv2


@csrf_exempt
def upload(request):
    # import pdb;
    # pdb.set_trace()
    response_data = {}
    response_data['result'] = 'OK'

    # print request.FILES
    #
    # uploaded_file = request.FILES["file"]
    #
    # response_data['filename'] = uploaded_file.name
    # response_data['filesize'] = uploaded_file.size

    open("received.jpg","w").write(request.body)

    path, contours = process_picture("received.jpg")

    shape_name = identify_shape(contours)

    response_data['preview'] = reverse('get_processed')

    response_data['shape'] = shape_name

    return django.http.HttpResponse(json.dumps(response_data), content_type="application/json", status=200)

@csrf_exempt
def get_processed(request):
    import os.path
    import mimetypes
    mimetypes.init()

    try:
        file_path = '/Users/yannick/Documents/programmation/medizam/medizam/tmp/processed.jpg'
        fsock = open(file_path,"r")
        #file = fsock.read()
        #fsock = open(file_path,"r").read()
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        print "file size is: " + str(file_size)
        mime_type_guess = mimetypes.guess_type(file_name)
        if mime_type_guess is not None:
            response = HttpResponse(fsock, mimetype=mime_type_guess[0])
        response['Content-Disposition'] = 'attachment; filename=' + file_name
    except IOError:
        response = HttpResponseNotFound()
    return response


def process_picture(path):
    import cv2
    import numpy as np
    import sys

    src = path

    contours = None

    # def thresh_callback(thresh):
    #     edges = cv2.Canny(blur,thresh,thresh*2)
    #     drawing = np.zeros(img.shape,np.uint8)     # Image to draw the contours
    #     contours,hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #     for cnt in contours:
    #         color = np.random.randint(0,255,(3)).tolist()  # Select a random color
    #         cv2.drawContours(img,[cnt],0,color,2)
    #         # cv2.imshow('output',drawing)
    #     # cv2.imshow('input',img)

    img = cv2.imread(src)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)

    # cv2.namedWindow('input',cv2.WINDOW_AUTOSIZE)

    thresh = 100
    max_thresh = 255

    # cv2.createTrackbar('canny thresh:','input',thresh,max_thresh,thresh_callback)

    # thresh_callback(thresh)


        # def thresh_callback(thresh):
    edges = cv2.Canny(blur,thresh,thresh*2)
    drawing = np.zeros(img.shape,np.uint8)     # Image to draw the contours
    contours,hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        color = np.random.randint(0,255,(3)).tolist()  # Select a random color
        cv2.drawContours(img,[cnt],0,color,2)
        # cv2.imshow('output',drawing)
    # cv2.imshow('input',img)

    # if cv2.waitKey(0) == 27:
    #     cv2.destroyAllWindows()

    current = os.getcwd()

    out_path = 'tmp/processed.jpg'

    out_path = os.path.join(current, out_path)

    cv2.imwrite(out_path,img)

    print out_path

    return out_path, contours

def identify_shape(contours):

    # print contours

    biggest_cnt_len = 0
    biggest_cnt_name = "unknown"

    # import pdb;pdb.set_trace()

    for cnt in contours:
        print cnt
        approx = cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)
        length = len(approx)
        shape = "polygon".format(length)
        if len(approx)==5:
            shape = "pentagon"
            # cv2.drawContours(img,[cnt],0,255,-1)
        elif len(approx)==3:
            shape = "triangle"
            # cv2.drawContours(img,[cnt],0,(0,255,0),-1)
        elif len(approx)==4:
            shape = "square"
            # cv2.drawContours(img,[cnt],0,(0,0,255),-1)
        elif len(approx) == 9:
            shape = "half-circle"
            # cv2.drawContours(img,[cnt],0,(255,255,0),-1)
        elif len(approx) > 12:
            shape = "circle"
            # cv2.drawContours(img,[cnt],0,(0,255,255),-1)

        shape = "{} {}".format(shape, length)

        if length > biggest_cnt_len :
            biggest_cnt_len = length
            biggest_cnt_name = shape
    return biggest_cnt_name
