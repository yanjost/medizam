from django.conf.urls import patterns, url
import front.views

urlpatterns = patterns('',
    url(r'/upload', 'front.views.upload'),
    url(r'/get_processed', 'front.views.get_processed', name='get_processed'),
    url(r'^/reference_picture/(?P<id>\d+)$', front.views.get_reference_picture, name='reference_picture'),
)