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
            donor_json['label'] = donor.name
            results.append(donor_json)
        data = simplejson.dumps(results)
        mimetype = 'application/json'

    # form action handling
    else:
        donor_form = DonorForm(request.POST or None)
        donate_formset = StockInFormSet(request.POST or None)
        date_form = DateForm(request.POST or None)
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

    # form action handling
    else:
        vendor_form = VendorForm(request.POST or None)
        purchase_formset = StockInFormSet(request.POST or None)
        date_form = DateForm(request.POST or None)
        if(vendor_form.is_valid() and purchase_formset.is_valid()
           and date_form.is_valid()):
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
                    confirm=False
                )
            return HttpResponseRedirect('thanks')

        context = RequestContext(request, {'vendor_form': vendor_form,
                                           'date_form': date_form,
                                           'purchase_formset': purchase_formset})
        template = loader.get_template('purchase.html')
        data = template.render(context)
        mimetype = "text/html; charset=utf-8"
    return HttpResponse(data, mimetype)
    
def distribution(request):
    # create formset
    standard_list = Category.objects.filter(name="standard")
    standard_item = []
    for item in standard_list:
        standard_item.append(item.stock)
        DistributionFormSet = formset_factory(DistributionForm,
                                              extra = len(standard_item),
                                              formset=RequiredFormSet)
    # form action handling
    family_form = FamilyForm(request.POST or None)
    distribution_formset = DistributionFormSet(request.POST or None)
    date_form = DateForm(request.POST or None)
    if(family_form.is_valid() and
       distribution_formset.is_valid() and
       date_form.is_valid()):
        for s, form in zip(standard_item, distribution_formset):
            distribute = Distribute.objects.create(
                date=date_form.cleaned_data['date'],
                quantity=form.cleaned_data['quantity'],
                family_type=family_form.cleaned_data['family_type'],
                stock=s
                )
        return HttpResponseRedirect('thanks')

    context = RequestContext(request, {'family_form': family_form,
                                       'date_form': date_form,
                                       'distribution_formset': distribution_formset,
                                       'zip': zip(standard_item, distribution_formset)})
    return render(request, 'distribution.html', context)

def transfer(request):
    # create formset
    TransferFormSet = formset_factory(TransferForm, max_num=10, formset=RequiredFormSet)

    # Autocomplete
    if(request.is_ajax()):
        q = request.GET.get('term', '')
        destinations = Destination.objects.filter(name__icontains = q)[:20]
        results = []
        for destination in destinations:
            destination_json = {}
            destination_json['label'] = destination.name
            results.append(destination_json)
        data = simplejson.dumps(results)
        mimetype = 'application/json'
            
    # form action handling    
    else:
        destination_form = DestinationForm(request.POST or None)
        transfer_formset = TransferFormSet(request.POST or None)
        date_form = DateForm(request.POST or None)
        if(destination_form.is_valid() and
           transfer_formset.is_valid() and
           date_form.is_valid()):
            for form in transfer_formset:
                d, created = Destination.objects.get_or_create(**destination_form.cleaned_data)
                s = Stock.objects.get(name=form.cleaned_data['stock_name'],
                                      unit_measure=form.cleaned_data['unit_measure']
                                  )
                transfer = Transfer.objects.create(
                    date=date_form.cleaned_data['date'],
                    quantity=form.cleaned_data['quantity'],
                    destination=d,
                    # remark=form.cleaned_data['remark'],
                    stock=s
                )
            return HttpResponseRedirect('thanks')
        context = RequestContext(request, {'destination_form': destination_form,
                                           'date_form': date_form,
                                           'transfer_formset': transfer_formset})
        template = loader.get_template('transfer.html')
        data = template.render(context)
        mimetype = "text/html; charset=utf-8"
    return HttpResponse(data, mimetype)
        

# def stockEdit(request):
#     stocks = Stock.objects.all()
#     stock_formset = formset_factory(StockForm, formset=RequiredFormSet)
#     for form in stock_formset:
#         form.instance

#     if(start_date_form.is_valid() and end_date_form.is_valid()):
#         start_date = start_date_form.cleaned_data['date']

        
    
def donor(request):
    donor_list = Donor.objects.all()
    return render(request, 'donor.html',
                  RequestContext(request, {'donor_list': donor_list}))


def current_stock(request):
    stocks = Stock.objects.all()
    return render(request, 'current_stock.html',
                  RequestContext(request, {
                      'stocks': stocks
                  }))

    
