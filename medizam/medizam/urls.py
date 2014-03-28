import django.conf
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'medizam.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(
        r'^$', 'django.contrib.staticfiles.views.serve', kwargs={
            'path': '/front/index.html',}),
    url(r'^admin/', include(admin.site.urls)),
)
