from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'/upload', 'front.views.upload'),
)