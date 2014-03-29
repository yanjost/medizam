from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'/upload', 'front.views.upload'),
    url(r'/get_processed', 'front.views.get_processed', name='get_processed'),
)