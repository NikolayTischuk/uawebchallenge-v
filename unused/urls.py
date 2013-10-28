from django.conf.urls import patterns, include, url

urlpatterns = patterns('unused.views',
   url(r'^$', 'home'),
   url(r'^task/$', 'task'),
   url(r'^get/(?P<type>pages|website)$', 'get'),
)
