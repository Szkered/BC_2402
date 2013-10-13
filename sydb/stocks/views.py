#shortcuts
from django.shortcuts import render, get_object_or_404
# redirect for submission
from django.http import HttpResponseRedirect, HttpResponse
# RequestContext for csrf validation
from django.template import RequestContext, loader
# JSON
from django.utils import simplejson
# generic views
from django.views.generic.base import RedirectView
# formset
from django.forms.formsets import formset_factory, BaseFormSet

# models & forms
from stocks.models import *
from stocks.forms import *

# This class is used to require forms in the formset not to be empty
class RequiredFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super(RequiredFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False # self.forms[0].empty_permitted = False
            
StockInFormSet = formset_factory(StockInForm, max_num=10, formset=RequiredFormSet)


def thanks(request):
    return render(request, 'thanks.html')


def donation(request):
    # Autocomplete (work in progress)
    if(request.is_ajax()):
        q = request.GET.get('term', '')
        donors = Donor.objects.filter(name__icontains = q)[:20]
        results = []
        for donor in donors:
            donor_json = {}
            # donor_json['id'] = donor.address
            donor_json['label'] = donor.name
            # donor_json['value'] = donor.name
            results.append(donor_json)
        data = simplejson.dumps(results)
        mimetype = 'application/json'

    # When the form is submitted
    else:
        if(request.method == 'POST'):    
            donor_form = DonorForm(request.POST)
            donate_formset = StockInFormSet(request.POST)
            date_form = DateForm(request.POST)
            if(donor_form.is_valid() and donate_formset.is_valid() and date_form.is_valid()):
                d, created = Donor.objects.get_or_create(**donor_form.cleaned_data)
                for donate_form in donate_formset:
                    s, created = Stock.objects.get_or_create(
                        name=donate_form.cleaned_data['stock_name'],
                        unit_price=donate_form.cleaned_data['unit_price'],
                        unit_measure=donate_form.cleaned_data['unit_measure']
                    )
                    donate = Donate.objects.create(
                        date=date_form.cleaned_data['date'],
                        quantity=donate_form.cleaned_data['quantity'],
                        stock=s,
                        donor=d
                    )
                return HttpResponseRedirect('thanks')
        else:
            donor_form = DonorForm()
            date_form = DateForm()
            donate_formset = StockInFormSet()
        context = RequestContext(request, {'donor_form': donor_form,
                                           'date_form': date_form,
                                           'donate_formset': donate_formset})
        template = loader.get_template('donation.html')
        data = template.render(context)
        mimetype = "text/html; charset=utf-8"
    return HttpResponse(data, mimetype)
                  
def purchase(request):
    # Autocomplete 
    if(request.is_ajax()):
        q = request.GET.get('term', '')
        vendors = Vendor.objects.filter(name__icontains = q)[:20]
        results = []
        for vendor in vendors:
            vendor_json = {}
            vendor_json['label'] = vendor.name
            results.append(vendor_json)
        data = simplejson.dumps(results)
        mimetype = 'application/json'

    # When the form is submitted
    else:
        if(request.method == 'POST'):    
            vendor_form = VendorForm(request.POST)
            purchase_formset = StockInFormSet(request.POST)
            date_form = DateForm(request.POST)
            confirm_form = ConfirmForm(request.POST)
            if(vendor_form.is_valid() and purchase_formset.is_valid()
               and date_form.is_valid() and confirm_form.is_valid()):
                v, created = Vendor.objects.get_or_create(**vendor_form.cleaned_data)
                for purchase_form in purchase_formset:
                    s, created = Stock.objects.get_or_create(
                        name=purchase_form.cleaned_data['stock_name'],
                        unit_price=purchase_form.cleaned_data['unit_price'],
                        unit_measure=purchase_form.cleaned_data['unit_measure']
                    )
                    purchase = Purchase.objects.create(
                        date=date_form.cleaned_data['date'],
                        quantity=purchase_form.cleaned_data['quantity'],
                        stock=s,
                        vendor=v,
                        confirm=confirm_form.cleaned_data['confirm']
                    )
                return HttpResponseRedirect('thanks')
        else:
            vendor_form = VendorForm()
            date_form = DateForm()
            purchase_formset = StockInFormSet()
            confirm_form = ConfirmForm()
        context = RequestContext(request, {'vendor_form': vendor_form,
                                           'date_form': date_form,
                                           'confirm_form': confirm_form,
                                           'purchase_formset': purchase_formset})
        template = loader.get_template('purchase.html')
        data = template.render(context)
        mimetype = "text/html; charset=utf-8"
    return HttpResponse(data, mimetype)
    
    
    
def donor(request):
    categorys = Category.objects.all()
    cate_list = {categorys[0].name: categorys[0].stock.name}
    return render(request, 'donor.html',
                  RequestContext(request, {'cate_list': cate_list}))


