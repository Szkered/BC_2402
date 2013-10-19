from django.conf.urls import patterns, url
from django.views.generic import RedirectView
from stocks.views import *

urlpatterns = patterns('',
                       url(r'^donation/$', donation, name="donation"),
                       url(r'.?/thanks/$', thanks),
                       url(r'^donor/$', donor),
                       url(r'^purchase/$', purchase),
                       url(r'^distribution/$', distribution),
                       url(r'^transfer/$', transfer),
                       url(r'^stock_summary_report/$', stock_summary_report),
                       url(r'^donation_report/$', donation_report),
                       url(r'^purchase_report/$', purchase_report),
                       url(r'^distribution_report/$', distribution_report),
                       url(r'^transfer_out_report/$', transfer_out_report),
                       url(r'^vendor_report/$', vendor_report),
                       url(r'^donor_report/$', donor_report),

                       url(r'^current_stock/$', current_stock),
)
