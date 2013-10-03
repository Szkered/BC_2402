from django.conf.urls import patterns, include, url
from sydb.views import current_datetime
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       (r'^test/$', current_datetime), #test page
                       (r'^stocks/', include('stocks.urls', namespace="stocks")),
                       url(r'^admin/', include(admin.site.urls)),                     
    # Examples:
    # url(r'^$', 'sydb.views.home', name='home'),
    # url(r'^sydb/', include('sydb.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
  
)
