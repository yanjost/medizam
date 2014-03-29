import collections
import json
import time
import django.http
from django.shortcuts import render

from django.http import HttpResponse, HttpResponseNotFound

# Create your views here.
import django.views.generic

from django.views.decorators.csrf import csrf_exempt

from django.core.urlresolvers import reverse

import os

import cv2

import numpy

import emm

def get_medoc(id):
    # import pdb;pdb.set_trace()
    global medocs
    for m in medocs :
        if m.id == id :
            return m


@csrf_exempt
def get_reference_picture(request, id):
    global medocs

    path = get_medoc(id).image_path

    # import pdb; pdb.set_trace()

    import os.path
    import mimetypes
    mimetypes.init()

    try:
        file_path = path
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



def get_nearest_medoc(medocs, pic_path):
    scores = {}

    best_medoc = "unknown"
    best_score = 100000
    best_med=None

    # import pdb;pdb.set_trace()

    for med in medocs:
        score = emm.emm(med.image_path, pic_path)
        scores[med.name]=score

        print med.name, score

        if score < best_score:
            best_score=score
            best_medoc=med.name
            best_med = med

    return best_medoc, best_score, best_med

ScoredMedoc = collections.namedtuple('ScoredMedoc',['medoc','score','best'])

def get_scored_medoc(medocs, pic_path):
    results = []

    best_medoc = "unknown"
    best_score = 100000
    best_med=None

    # import pdb;pdb.set_trace()

    for med in medocs:
        score = emm.emm(med.image_path, pic_path)

        scored = ScoredMedoc(medoc=med, score=score, best=False)

        results.append(scored)

    results.sort(key=lambda x:x.score)

    results[0] = ScoredMedoc(medoc=results[0].medoc,score=results[0].score,best=True)

    return results

@csrf_exempt
def upload(request):
    global  medocs
    # import pdb;
    # pdb.set_trace()
    response_data = {}
    response_data['result'] = 'OK'


    pic_path = "tmp/received.jpg"

    if os.path.exists(pic_path):
        os.remove(pic_path)

    try :
        image_field_bytes = request.FILES['file'].read()
    except KeyError:
        print "NOT FOUND in FILES"

        image_field_bytes = request.body

    f = open(pic_path,"w")
    f.write(image_field_bytes)
    f.close()

    # image_field_bytes = normalize(image_field_bytes)

    file_bytes = numpy.asarray(bytearray(image_field_bytes), dtype=numpy.uint8)
    img_data_ndarray = cv2.imdecode(file_bytes, cv2.CV_LOAD_IMAGE_UNCHANGED)


    path, contours = process_picture(img_data_ndarray)

    shape_name = identify_shape(contours)

    response_data['preview'] = reverse('get_processed')

    response_data['shape'] = shape_name

    # ref_doliprane='private/samples/1N_top_low.jpg'
    # ref_spasfon='private/samples/4N_top_low.jpg'

    # dist_doli = emm.emm(ref_doliprane, pic_path)
    # dist_spasf = emm.emm(ref_spasfon, pic_path)

    # response_data["medoc_name"]="doliprane" if dist_doli < dist_spasf else "spasfon"

    medocs = load_medocs()

    # name, score, med = get_nearest_medoc(medocs,pic_path)

    # response_data["medoc_name"]=name
    # response_data["medoc_score"]=score
    # response_data["medoc_url"]=med.vidal_url

    scored = get_scored_medoc(medocs, pic_path)

    results = []

    for sm in scored :
        results.append({
            "name" : sm.medoc.name,
            "accuracy": 100 - (100*sm.score/16.0),
            "score": sm.score,
            "image":reverse('reference_picture', kwargs={"id":sm.medoc.id}),
            "id": sm.medoc.id,
            "best":sm.best
        })

    response_data["results"]=results

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


def process_picture(data):
    import cv2
    import numpy as np


    contours = None


    img = data

    print "IMG SHAPE : {}".format(img.shape)

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # gray = normalize(gray)

    # ret,gray = cv2.threshold(gray,128,255,1)

    cv2.imwrite("tmp/grey.jpg",gray)

    blur = cv2.GaussianBlur(gray,(5,5),0)

    # cv2.namedWindow('input',cv2.WINDOW_AUTOSIZE)

    thresh = 50
    max_thresh = 255

    edges = cv2.Canny(blur,thresh,thresh*2)
    # drawing = np.zeros(img.shape,np.uint8)     # Image to draw the contours
    contours,hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        color = np.random.randint(0,255,(3)).tolist()  # Select a random color
        cv2.drawContours(gray,[cnt],0,color,2)

    current = os.getcwd()

    out_path = 'tmp/processed.jpg'

    out_path = os.path.join(current, out_path)

    cv2.imwrite(out_path,gray)

    print out_path

    return out_path, contours

def identify_shape(contours):

    # print contours

    biggest_cnt_len = 0
    biggest_cnt_name = "unknown"

    # import pdb;pdb.set_trace()

    for cnt in contours:
        # print cnt
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

def normalize(img):
    return cv2.equalizeHist(img)

def calc_hist(img):
    import numpy as np
    hsv_map = np.zeros((180, 256, 3), np.uint8)
    h, s = np.indices(hsv_map.shape[:2])
    hsv_map[:,:,0] = h
    hsv_map[:,:,1] = s
    hsv_map[:,:,2] = 255
    hsv_map = cv2.cvtColor(hsv_map, cv2.COLOR_HSV2BGR)
    # cv2.imshow('hsv_map', hsv_map)

    # cv2.namedWindow('hist', 0)
    # hist_scale = 10
    # def set_scale(val):
    #     global hist_scale
    #     hist_scale = val
    # cv2.createTrackbar('scale', 'hist', hist_scale, 32, set_scale)
    #
    # try:
    #     fn = sys.argv[1]
    # except:
    #     fn = 0
    # cam = video.create_capture(fn, fallback='synth:bg=../cpp/baboon.jpg:class=chess:noise=0.05')

    # while True:
    #     flag, frame = cam.read()
    #     cv2.imshow('camera', frame)

    small = cv2.pyrDown(frame)

    hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)
    dark = hsv[...,2] < 32
    hsv[dark] = 0
    h = cv2.calcHist( [hsv], [0, 1], None, [180, 256], [0, 180, 0, 256] )


    h = np.clip(h*0.005*hist_scale, 0, 1)
    vis = hsv_map*h[:,:,np.newaxis] / 255.0
    # cv2.imshow('hist', vis)

    # ch = 0xFF & cv2.waitKey(1)
    # if ch == 27:
    #     break
    # cv2.destroyAllWindows()


class Medoc(object):
    def __init__(self):
        self.id = 0
        self.name = ""
        self.dci=""
        self.dose=""
        self.shape=""
        self.color1=""
        self.color2=""
        self.generic=False
        self.details=""
        self.vidal_url=""
        self.image_path=""

    def load_image(self):
        import glob
        zg = "/Users/yannick/Documents/programmation/medizam/medizam/private/pictures/{}*.jpg".format(self.id)
        print zg
        self.image_path = glob.glob(zg)[0]
        print "Loading {}".format(self.image_path)
        self.image = cv2.imread(self.image_path)




def load_medocs():
    import csv

    # import pdb;pdb.set_trace()

    ret=[]

    skip=True

    with open('private/medoc.csv', 'Ur') as f:
        for rec in csv.reader(f, delimiter=','):
            if skip:
                skip=False
                continue

            data = rec
            print data
            med = Medoc()
            med.id,med.name,med.dci,med.dose,med.shape,med.color1,med.color2,med.generic,med.details,med.vidal_url=data
            med.load_image()
            med.id = med.id.strip()
            ret.append(med)

    return ret

# global medocs
medocs = load_medocs()