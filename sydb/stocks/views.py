from django.shortcuts import render, get_object_or_404
# redirect for submission
from django.http import HttpResponseRedirect
# RequestContext for csrf
from django.template import RequestContext, loader
# from django.core.urlresolvers import reverse

# models & forms
from stocks.models import *
from stocks.forms import *


def donation(request):
    if(request.method == 'POST'):
        donor_form = DonorForm(request.POST)
        donate_form = DonateForm(request.POST)
        if form.is_valid():
            d, created = Donor.objects.get_or_create(
                name=form.cleaned_data['donor_name'],
                address=form.cleaned_data['donor_address'],
                contact_no=form.cleaned_data['donor_contact_no'],
                mailing=form.cleaned_data['donor_mailing'],
                referral=form.cleaned_data['donor_referral']       
                )
            s, created = Stock.objects.get_or_create(
                description=form.cleaned_data['stock_description'],
                unit_measure=form.cleaned_data['stock_unit_measure'],
                unit_price=form.cleaned_data['stock_unit_price'],
                purchase_sum=0.00,
                donate_sum=0.00,
                transfer_sum=0.00,
                distribute_sum=0.00
                )
            donate = Donate(
                date=form.cleaned_data['donate_date'],
                quantity=form.cleaned_data['donate_quantity'],
                stock=s,
                donor=d
                )
            return HttpResponseRedirect('thanks/')
    else:
        donor_form = DonorForm()
        donate_form = DonateForm()
    return render(request, 'donation.html',
                  RequestContext(request, {'donor_form': donor_form,
                                           'donate_form': donate_form}))
