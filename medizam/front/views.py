import json
import django.http
from django.shortcuts import render

# Create your views here.
import django.views.generic


def upload(request):
    response_data = {}
    response_data['result'] = 'failed'
    response_data['message'] = 'You messed up'
    return django.http.HttpResponse(json.dumps(response_data), content_type="application/json", status=400)
