import json
import django.http
from django.shortcuts import render

# Create your views here.
import django.views.generic

from django.views.decorators.csrf import csrf_exempt

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

    return django.http.HttpResponse(json.dumps(response_data), content_type="application/json", status=200)


def process_picture():
    import cv2
    import numpy as np
    import sys

    src = sys.argv[1]

    def thresh_callback(thresh):
        edges = cv2.Canny(blur,thresh,thresh*2)
        drawing = np.zeros(img.shape,np.uint8)     # Image to draw the contours
        contours,hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            color = np.random.randint(0,255,(3)).tolist()  # Select a random color
            cv2.drawContours(drawing,[cnt],0,color,2)
            # cv2.imshow('output',drawing)
        # cv2.imshow('input',img)

    img = cv2.imread(src)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)

    # cv2.namedWindow('input',cv2.WINDOW_AUTOSIZE)

    thresh = 100
    max_thresh = 255

    # cv2.createTrackbar('canny thresh:','input',thresh,max_thresh,thresh_callback)

    thresh_callback(thresh)

    # if cv2.waitKey(0) == 27:
    #     cv2.destroyAllWindows()

    cv2.imwrite('tmp.jpg',img)