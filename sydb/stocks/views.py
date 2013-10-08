from django.shortcuts import render, get_object_or_404
# redirect for submission
from django.http import HttpResponseRedirect
# RequestContext for csrf validation
from django.template import RequestContext, loader
# from django.core.urlresolvers import reverse

# generic views
from django.views.generic.base import RedirectView
# formset
from django.forms.formsets import formset_factory, BaseFormSet

# models & forms
from stocks.models import *
from stocks.forms import *



def thanks(request):
    return render(request, 'thanks.html')


def donation(request):
    # This class is used to require forms in the formset not to be empty
    class RequiredFormSet(BaseFormSet):
        def __init__(self, *args, **kwargs):
            super(RequiredFormSet, self).__init__(*args, **kwargs)
            for form in self.forms:
                form.empty_permitted = False # self.forms[0].empty_permitted = False
    DonateFormSet = formset_factory(DonateForm, max_num=10, formset=RequiredFormSet)
    # When the form has been submitted
    if(request.method == 'POST'):
        donor_form = DonorForm(request.POST)
        donate_formset = DonateFormSet(request.POST)
        
        if(donor_form.is_valid() and donate_formset.is_valid()):
            d, created = Donor.objects.get_or_create(**donor_form.cleaned_data)
            for donate_form in donate_formset:
                s, created = Stock.objects.get_or_create(
                    name=donate_form.cleaned_data['stock_name'],
                    unit_price=donate_form.cleaned_data['unit_price'],
                    unit_measure=donate_form.cleaned_data['unit_measure']
                )
                donate = Donate.objects.create(
                    date=donate_form.cleaned_data['date'],
                    quantity=donate_form.cleaned_data['quantity'],
                    stock=s,
                    donor=d
                )
            return HttpResponseRedirect('thanks')
    else:
        donor_form = DonorForm()
        donate_formset = DonateFormSet()
    return render(request, 'donation.html',
                  RequestContext(request, {'donor_form': donor_form,
                                           'donate_formset': donate_formset}))

def donor(request):
    donor_list = Donor.objects.all()
    return render(request, 'donor.html',
                  RequestContext(request, {'donor_list': donor_list}))
        

