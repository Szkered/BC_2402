from django.conf.urls import patterns, url
from stocks.views import *

urlpatterns = patterns('',
               url(r'^donation/$', donation),
    
)
