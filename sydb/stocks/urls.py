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
                       url(r'^adjust/$', adjust),
                       url(r'^init/$', initialization),
                       url(r'^history/$', historical_amt),
                       url(r'^merge_stock/$', merge_stock),
                       #edit
                       url(r'^donation_edit/$', donation_edit),
                       url(r'^d_edit/(?P<d_id>\d+)/$', donate_edit),
                       url(r'^order_edit/$', order_edit),
                       url(r'^p_edit/(?P<o_id>\d+)/$', purchase_edit),
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
                       #
                       url(r'^purchase_order/$', purchase_order),
                       url(r'^p_order/(?P<o_id>\d+)/$', purchase_order_generate),
                       url(r'^thank_you_letter/$', thank_you_letter),
                       url(r'^d_letter/(?P<d_id>\d+)/$',letter_generate),
)

