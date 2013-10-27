from django.conf.urls import patterns, url
from django.views.generic import RedirectView, TemplateView
from stocks.views import *

urlpatterns = patterns('',
                       #pages
                       url(r'^donation/$', donation, name="donation"),
                       url(r'^purchase/$', purchase),
                       url(r'^distribution/$', distribution),
                       url(r'^transfer/$', transfer),
                       url(r'.?/thanks/$', thanks),
                       url(r'^confirmation', confirmation),
                       url(r'^adjust/$', adjust),
                       #edit
                       url(r'^donate_edit/$', donate_edit),
                       url(r'^purchase_edit/$', purchase_edit),
                       url(r'^transfer_edit/$', transfer_edit),
                       url(r'^distribute_edit/$', distribute_edit),
                       url(r'^vendor_edit/$', vendor_edit),
                       url(r'^donor_edit/$', donor_edit),
                       url(r'^stock_edit/$', stock_edit),
                       #reports
                       url(r'^stock_summary/$', stock_summary),
                       url(r'^donation_summary/$', donation_summary),
                       url(r'^purchase_summary/$', purchase_summary),
                       url(r'^distribution_summary/$', distribution_summary),
                       url(r'^transfer_out_summary/$', transfer_out_summary),
                       url(r'^vendor_summary/$', vendor_summary),
                       url(r'^donor_summary/$', donor_summary),
                       #autocomplete
                       url(r'^get_donors/$', get_donors, name="get_donors"),
                       url(r'^get_stocks/$', get_stocks, name="get_stocks"),
                       url(r'^get_categorys/$', get_categorys, name="get_categorys"),
                       url(r'^get_vendors/$', get_vendors, name="get_vendors"),
                       url(r'^get_destination/$', get_destination, name="get_destination"),
                       #reports
                       url(r'^stock_report/download/$', stock_summary_report),
                       url(r'^donation_report/download/$', donation_report),
                       url(r'^purchase_report/download/$', purchase_report),
                       url(r'^distribution_report/download/$', distribution_report),
                       url(r'^transfer_out_report/download/$', transfer_out_report),
                       url(r'^vendor_report/download/$', vendor_report),
                       url(r'^donor_report/download/$', donor_report),
)

