from django.conf.urls import patterns, url
from django.views.generic import RedirectView
from stocks.views import *

urlpatterns = patterns('',
                       #pages
                       url(r'^donation/$', donation, name="donation"),
                       url(r'^purchase/$', purchase),
                       url(r'^distribution/$', distribution),
                       url(r'^transfer/$', transfer),
                       url(r'.?/thanks/$', thanks),
                       url(r'^donor/$', donor),
                       #autocomplete
                       url(r'^get_donors/$', get_donors, name="get_donors"),
                       url(r'^get_stocks/$', get_stocks, name="get_stocks"),
                       url(r'^get_categorys/$', get_categorys, name="get_categorys"),
                       url(r'^get_vendors/$', get_vendors, name="get_vendors"),
                       #reports
                       url(r'^stock_summary_report/$', stock_summary_report),
                       url(r'^donation_report/$', donation_report),
                       url(r'^purchase_report/$', purchase_report),
                       url(r'^distribution_report/$', distribution_report),
                       url(r'^transfer_out_report/$', transfer_out_report),
                       url(r'^vendor_report/$', vendor_report),
                       url(r'^donor_report/$', donor_report),
                       url(r'^current_stock/$', current_stock),
)
