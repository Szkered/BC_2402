from django.conf.urls import patterns, url
from django.views.generic import RedirectView
from stocks.views import *

urlpatterns = patterns('',
                       url(r'^donation/$', donation, name="donation"),
                       url(r'.?/thanks/$', thanks),
                       url(r'^donor/$', donor),
                       url(r'^purchase/$', purchase),
    
)
