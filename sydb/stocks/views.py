from django.shortcuts import render, get_object_or_404
# redirect for submission
from django.http import HttpResponseRedirect
# RequestContext for csrf validation
from django.template import RequestContext, loader
# from django.core.urlresolvers import reverse

# generic views
from django.views.generic.base import RedirectView

# models & forms
from stocks.models import *
from stocks.forms import *



def thanks(request):
    return render(request, 'thanks.html')


def donation(request):
    if(request.method == 'POST'):
        donor_form = DonorForm(request.POST)
        donate_form = DonateForm(request.POST)
        if donor_form.is_valid() and donate_form.is_valid():
            d, created = Donor.objects.get_or_create(
                name=donor_form.cleaned_data['name'],
                address=donor_form.cleaned_data['address'],
                contact_no=donor_form.cleaned_data['contact_no'],
                mailing=donor_form.cleaned_data['mailing'],
                referral=donor_form.cleaned_data['referral']       
                )
            s, created = Stock.objects.get_or_create(
                name=donate_form.cleaned_data['stock_name'],
                unit_measure=donate_form.cleaned_data['unit_measure'],
                unit_price=donate_form.cleaned_data['unit_price']
                )
            donate = Donate.objects.create(
                date=donate_form.cleaned_data['date'],
                quantity=donate_form.cleaned_data['quantity'],
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

# def donation_detail(request):
#     if(request.method == 'GET'):

def donor(request):
    donor_list = Donor.objects.all()
    return render(request, 'donor.html',
                  RequestContext(request, {'donor_list': donor_list}))
        

