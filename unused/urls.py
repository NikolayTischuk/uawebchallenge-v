from django.conf.urls import patterns, include, url

urlpatterns = patterns('unused.views',
   url(r'^$',             'home'),
   url(r'^task/$',        'task'),
   url(r'^get/pages$',    '_pages',   name="pages"),
   url(r'^get/website$',  '_website', name="website"),
)
