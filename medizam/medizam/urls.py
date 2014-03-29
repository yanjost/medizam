import django.conf
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

# urlpatterns = patterns('',
#     # Examples:
#     # url(r'^$', 'medizam.views.home', name='home'),
#     # url(r'^blog/', include('blog.urls')),
#     url(
#         r'^$', 'django.contrib.staticfiles.views.serve', kwargs={
#             'path': '/front/index.html',}),
#
#     url(r'^admin/', include(admin.site.urls)),
# )
urlpatterns = patterns(
    'django.contrib.staticfiles.views',
    url(r'^(?:index.html)?$', 'serve', kwargs={'path': 'index.html'}),
    url(r'^(?P<path>fonts/.*)$', 'serve'),
    url(r'^(?P<path>templates/.*)$', 'serve'),
    url(r'^(?P<path>scripts/.*)$', 'serve'),
    url(r'^(?P<path>styles/.*)$', 'serve'),
    url(r'^(?P<path>views/.*)$', 'serve'),
    url(r'^(?P<path>libs/.*)$', 'serve'),
    url(r'^(?P<path>images/.*)$', 'serve'),
    url(r'^api', include('front.urls')),
    )