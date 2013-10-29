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
# model formset
from django.forms.models import modelformset_factory

# regex
import re

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


    
################################################################################
# Page View
################################################################################

def thanks(request):
    current_path = request.get_full_path()
    target_path = current_path.replace('thanks/', '')
    return render(request, 'thanks.html',
                  RequestContext(request, {'target_path': target_path}))

def index(request):
    return render(request, 'index.html')


def donation(request):
    donor_form = DonorForm(request.POST or None)
    donate_formset = StockInFormSet(request.POST or None)
    date_form = DateForm(request.POST or None)
    
    if(donor_form.is_valid() and donate_formset.is_valid() and date_form.is_valid()):
        d, created = Donor.objects.get_or_create(**donor_form.cleaned_data)
        for donate_form in donate_formset:
            s, created = Stock.objects.get_or_create(
                name=donate_form.cleaned_data['stock_name'],
                unit_measure=donate_form.cleaned_data['unit_measure'],
                defaults={'unit_price':donate_form.cleaned_data['unit_price']}
            )
            s.unit_price = donate_form.cleaned_data['unit_price']
            s.save()
            donate = Donate.objects.create(
                date=date_form.cleaned_data['date'],
                quantity=donate_form.cleaned_data['quantity'],
                stock=s,
                donor=d
            )
            category_list = re.split(
                ', | |,|',
                donate_form.cleaned_data['category']
            )
            for item in category_list:
                category, created = Category.objects.get_or_create(
                    stock=s,
                    name=item
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
    vendor_form = VendorForm(request.POST or None)
    purchase_formset = StockInFormSet(request.POST or None)
    date_form = DateForm(request.POST or None)
    if(vendor_form.is_valid() and purchase_formset.is_valid()
       and date_form.is_valid()):
        v, created = Vendor.objects.get_or_create(**vendor_form.cleaned_data)
        o = Order.objects.create(
            date=date_form.cleaned_data['date'],
            confirm=False,
            vendor=v
        )
        for purchase_form in purchase_formset:
            s, created = Stock.objects.get_or_create(
                name=purchase_form.cleaned_data['stock_name'],
                unit_price=purchase_form.cleaned_data['unit_price'],
                unit_measure=purchase_form.cleaned_data['unit_measure']
            )
            purchase = Purchase.objects.create(
                order=o,
                quantity=purchase_form.cleaned_data['quantity'],
                stock=s
            )
            category_list = re.split(
                ', | |,|',
                purchase_form.cleaned_data['category']
            )
            for item in category_list:
                if not item=='':
                    category, created = Category.objects.get_or_create(
                        stock=s,
                        name=item
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
    standard_item = [item.stock for item in Category.objects.filter(name="standard")]
    DistributionFormSet = formset_factory(DistributionForm,
                                          extra = len(standard_item),
                                          formset=RequiredFormSet,)
    # form action handling
    family_form = FamilyForm(request.POST or None)
    distribution_formset = DistributionFormSet(request.POST or None)
    date_form = DateForm(request.POST or None)
    for s, form in zip(standard_item, distribution_formset):
        form.fields['stock_id'].initial = s.pk

    if(family_form.is_valid() and
       distribution_formset.is_valid() and
       date_form.is_valid()):
        for s, form in zip(standard_item, distribution_formset):
            q = form.cleaned_data['quantity']
            if(q > 0):
                distribute = Distribute.objects.create(
                    date=date_form.cleaned_data['date'],
                    quantity=q,
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
            
    # form action handling    
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
        

def confirmation(request):
    OrderFormSet = modelformset_factory(Order, extra=0)
    unconfirmed_order = Order.objects.filter(confirm=False).order_by('date')
    order_formset = OrderFormSet(request.POST or None, queryset=unconfirmed_order)
    if(order_formset.is_valid()):
        order_formset.save()
        return HttpResponseRedirect('thanks')
    return render(request, 'confirmation.html',
                  RequestContext(request, {'order_formset': order_formset,
                                           'unconfirmed_purchases': unconfirmed_order,
                                           'zip': zip(order_formset,
                                                      unconfirmed_order)}))

def adjust(request):
    adjust_form = AdjustForm(request.POST or None)
    if(adjust_form.is_valid()):
        corret_amt = adjust_form.cleaned_data['current_amount']
        target_stock = Stock.objects.get(name=adjust_form.cleaned_data['stock_name'],
                                         unit_measure=adjust_form.cleaned_data['unit_measure'])
        if(corret_amt > target_stock.current_amt()):
            adjustment = corret_amt - target_stock.current_amt()
            super_d, created = Donor.objects.get_or_create(
                name="super",
                address="super",
                contact_no="1",
                mailing=False,
                referral='O',
            )
            Donate.objects.create(
                date=datetime.datetime.now(),
                quantity=adjustment,
                donor=super_d,
                stock=target_stock,
            )
        else:
            adjustment = target_stock.current_amt() - corret_amt
            super_d, created = Destination.objects.get_or_create(
                name="super",
                person_in_charge="super",
                contact_no="1",
            )
            Transfer.objects.create(
                date=datetime.datetime.now(),
                quantity=adjustment,
                stock=target_stock,
                destination=super_d,
            )
        return HttpResponseRedirect('thanks')
    return render(request, 'adjust.html',
                  RequestContext(request, {'adjust_form': adjust_form}))



################################################################################
# Edit
################################################################################

def donate_edit(request):
    DonateFormSet = modelformset_factory(Donate, extra=0)
    start_end_date_form = StartEndDateForm(request.GET or None)
    donor_name = request.GET.get('donor_name', '')
    stock_name = request.GET.get('stock_name', '')
    category = re.split(', | |,|', request.GET.get('category', ''))
    if(category==['']):
        q = Donate.objects.all()
    else:
        cList = Category.objects.filter(name__in=category)
        sList = [c.stock for c in cList]
        q = Donate.objects.filter(stock__in=sList)
    if(stock_name!=''):
        q = q.filter(stock__name=stock_name)
    if(start_end_date_form.is_valid()):
        start_date = start_end_date_form.cleaned_data['start_date']
        end_date = start_end_date_form.cleaned_data['end_date']
        q = q.filter(date__range=[start_date, end_date])
    if(donor_name!=''):
        q = q.filter(donor__name=donor_name)
    donate_formset = DonateFormSet(request.POST or None, queryset=q)
    if(donate_formset.is_valid()):
        donate_formset.save()
        return HttpResponseRedirect('thanks')
    return render(request, 'donate_edit.html',
                  RequestContext(request, {'donate_formset': donate_formset,
                                           'start_end_date_form': start_end_date_form}))

def purchase_edit(request):
    """Edit purchase orders."""
    
    # PurchaseFormSet = modelformset_factory(Purchase, extra=0)
    OrderFormSet = modelformset_factory(Order, extra=0)
    start_end_date_form = StartEndDateForm(request.GET or None)
    
    vendor_name = request.GET.get('vendor_name', '')
    stock_name = request.GET.get('stock_name', '')
    category = re.split(', | |,|', request.GET.get('category', ''))
    
    if(category==['']):
        q = Purchase.objects.all()
    else:
        cList = Category.objects.filter(name__in=category)
        sList = [c.stock for c in cList]
        q = Purchase.objects.filter(stock__in=sList)
        
    if(start_end_date_form.is_valid()):
        start_date = start_end_date_form.cleaned_data['start_date']
        end_date = start_end_date_form.cleaned_data['end_date']
        q = q.filter(order__date__range=[start_date, end_date])
        
    if(stock_name!=''):
        q = q.filter(stock__name=stock_name)
    if(vendor_name!=''):
        q = q.filter(vendor__name=vendor_name)

    orders_id = []
    orders_id = [item.order.pk for item in q if item.order not in orders_id]
    o = Order.objects.filter(pk__in=orders_id)
        
    # purchase_formset = PurchaseFormSet(request.POST or None, queryset=q)
    order_formset = OrderFormSet(request.POST or None, queryset=o)
    
    if(order_formset.is_valid()):
        # purchase_formset.save()
        order_formset.save()
        return HttpResponseRedirect('thanks')
    return render(request, 'purchase_edit.html',
                  RequestContext(request, {
                      # 'purchase_formset': purchase_formset,
                      'order_formset': order_formset,
                      'start_end_date_form': start_end_date_form}))

def transfer_edit(request):
    TransferFormSet = modelformset_factory(Transfer, extra=0)
    start_end_date_form = StartEndDateForm(request.GET or None)
    destination_name = request.GET.get('destination_name', '')
    stock_name = request.GET.get('stock_name', '')
    category = re.split(', | |,|', request.GET.get('category', ''))
    if(category==['']):
        q = Transfer.objects.all()
    else:
        cList = Category.objects.filter(name__in=category)
        sList = [c.stock for c in cList]
        q = Transfer.objects.filter(stock__in=sList)
    if(stock_name!=''):
        q = q.filter(stock__name=stock_name)
    if(start_end_date_form.is_valid()):
        start_date = start_end_date_form.cleaned_data['start_date']
        end_date = start_end_date_form.cleaned_data['end_date']
        q = q.filter(date__range=[start_date, end_date])
    if(destination_name!=''):
        q = q.filter(destination__name=destination_name)
    transfer_formset = TransferFormSet(request.POST or None, queryset=q)
    if(transfer_formset.is_valid()):
        transfer_formset.save()
        return HttpResponseRedirect('thanks')
    return render(request, 'transfer_edit.html',
                  RequestContext(request, {'transfer_formset': transfer_formset,
                                           'start_end_date_form': start_end_date_form}))

def distribute_edit(request):
    DistributeFormSet = modelformset_factory(Distribute, extra=0)
    start_end_date_form = StartEndDateForm(request.GET or None)
    family_form = FamilyForm(request.GET or None)
    stock_name = request.GET.get('stock_name', '')
    category = re.split(', | |,|', request.GET.get('category', ''))
    if(category==['']):
        q = Distribute.objects.all()
    else:
        cList = Category.objects.filter(name__in=category)
        sList = [c.stock for c in cList]
        q = Distribute.objects.filter(stock__in=sList)
    if(stock_name!=''):
        q = q.filter(stock__name=stock_name)
    if(start_end_date_form.is_valid()):
        start_date = start_end_date_form.cleaned_data['start_date']
        end_date = start_end_date_form.cleaned_data['end_date']
        q = q.filter(date__range=[start_date, end_date])
    if(family_form.is_valid()):
        if(family_form.cleaned_data['family_type'] != 'L'):
            q = q.filter(family_type=family_form.cleaned_data['family_type'])
    distribute_formset = DistributeFormSet(request.POST or None, queryset=q)
    if(distribute_formset.is_valid()):
        distribute_formset.save()
        return HttpResponseRedirect('thanks')
    return render(request, 'distribute_edit.html',
                  RequestContext(request, {'distribute_formset': distribute_formset,
                                           'family_form': family_form,
                                           'start_end_date_form': start_end_date_form}))
    
def vendor_edit(request):
    VendorFormSet = modelformset_factory(Vendor, extra=0)
    vendor_name = request.GET.get('id_name', '')
    if(vendor_name==''):
        vendor_formset = VendorFormSet(request.POST or None)
    else:
        q = Vendor.objects.filter(name=vendor_name)
        vendor_formset = VendorFormSet(request.POST or None, queryset=q)
    if(vendor_formset.is_valid()):
        vendor_formset.save()
        return HttpResponseRedirect('thanks')
    return render(request, 'vendor_edit.html',
                  RequestContext(request, {'vendor_formset': vendor_formset}))

def donor_edit(request):
    DonorFormSet = modelformset_factory(Donor, extra=0)
    donor_name = request.GET.get('id_name', '')
    if(donor_name==''):
        donor_formset = DonorFormSet(request.POST or None)
    else:
        q = Donor.objects.filter(name=donor_name)
        donor_formset = DonorFormSet(request.POST or None, queryset=q)
    if(donor_formset.is_valid()):
        donor_formset.save()
        return HttpResponseRedirect('thanks')
    return render(request, 'donor_edit.html',
                  RequestContext(request, {'donor_formset': donor_formset}))

def stock_edit(request):
    StockFormSet = modelformset_factory(Stock, extra=0)
    stock_name = request.GET.get('stock_name', '')
    category = re.split(', | |,|', request.GET.get('category', ''))
    if(category==['']):
        q = Stock.objects.all().order_by('name')
    else:
        cL = Category.objects.filter(name__in=category)
        sList = [c.stock.pk for c in cL]
        q = Stock.objects.filter(pk__in=sList).order_by('name')
    if(stock_name!=''):
        q = q.filter(name=stock_name)
    stock_formset = StockFormSet(request.POST or None, queryset=q)
    cList = [stock.category_slug() for stock in q]
    if(stock_formset.is_valid()):
        stock_formset.save()
        for s in q:
            new_cList = re.split(', | |,|', request.POST.get("%s_%s" % (s.name, s.unit_measure)))
            old_cList = re.split(', | |,|', s.category_slug())
            for item in new_cList:
                if item not in old_cList and item != '':
                    Category.objects.create(
                        stock=s,
                        name=item
                    )
            for item in old_cList:
                if item not in new_cList:
                    Category.objects.get(
                        stock=s,
                        name=item
                    ).delete()
        return HttpResponseRedirect('thanks')
    return render(request, 'stock_edit.html',
                  RequestContext(request, {'zip': zip(stock_formset, cList),
                                           'stock_formset': stock_formset}))



    
    
################################################################################
# Report
################################################################################

def stock_summary(request):
    stock_name = request.GET.get('stock_name', '')
    category = re.split(', | |,|', request.GET.get('category', ''))
    if(category==['']):
        q = Stock.objects.all().order_by('name')
    else:
        cL = Category.objects.filter(name__in=category)
        sList = [c.stock.pk for c in cL]
        q = Stock.objects.filter(pk__in=sList).order_by('name')
    if(stock_name!=''):
        q = q.filter(name=stock_name)
    return render(request, 'stock_summary.html',
                  RequestContext(request, {'stocks': q,
                                           'category': request.GET.get('category', ''),
                                           'stock_name': stock_name}))

def donation_summary(request):
    donor_name = request.GET.get('donor_name', '')
    stock_name = request.GET.get('stock_name', '')
    category = re.split(', | ', request.GET.get('category', ''))

    if(category==['']):
        q = Donate.objects.all().order_by('stock__name')
    else:
        cL = Category.objects.filter(name__in=category)
        sList = [c.stock.pk for c in cL]
        q = Donate.objects.filter(pk__in=sList).order_by('stock__name')
    if(stock_name!=''):
        q = q.filter(stock__name=stock_name)
    if(donor_name!=''):
        q = q.filter(donor__name=donor_name)      
    start_end_date_form = StartEndDateForm(request.GET or None)
    if(start_end_date_form.is_valid()):
        start_date = start_end_date_form.cleaned_data['start_date']
        end_date = start_end_date_form.cleaned_data['end_date']
        q = q.filter(date__range=[start_date, end_date])
        
    return render(request, 'donation_summary.html',
                  RequestContext(request, {'donations': q,
                                           'category': request.GET.get('category', ''),
                                           'stock_name': stock_name,
                                           'donor_name': donor_name,
                                           'start_end_date_form': start_end_date_form}))

def purchase_summary(request):
    vendor_name = request.GET.get('vendor_name', '')
    stock_name = request.GET.get('stock_name', '')
    category = re.split(', | ', request.GET.get('category', ''))

    if(category==['']):
        q = Purchase.objects.all().order_by('stock__name')
    else:
        cL = Category.objects.filter(name__in=category)
        sList = [c.stock.pk for c in cL]
        q = Purchase.objects.filter(pk__in=sList).order_by('stock__name')
    if(stock_name!=''):
        q = q.filter(stock__name=stock_name)
    if(vendor_name!=''):
        q = q.filter(vendor__name=vendor_name)
    start_end_date_form = StartEndDateForm(request.GET or None)
    if(start_end_date_form.is_valid()):
        start_date = start_end_date_form.cleaned_data['start_date']
        end_date = start_end_date_form.cleaned_data['end_date']
        q = q.filter(date__range=[start_date, end_date])
    
    return render(request, 'Purchase_summary.html',
                  RequestContext(request, {'purchases': q,
                                           'category': request.GET.get('category', ''),
                                           'stock_name': stock_name,
                                           'vendor_name': vendor_name,
                                           'start_end_date_form': start_end_date_form}))

def distribution_summary(request):
    family = request.GET.get('family_type', '')
    stock_name = request.GET.get('stock_name', '')
    category = re.split(', | ', request.GET.get('category', ''))

    if(category==['']):
        q = Distribute.objects.all().order_by('stock__name')
    else:
        cL = Category.objects.filter(name__in=category)
        sList = [c.stock.pk for c in cL]
        q = Distribute.objects.filter(pk__in=sList).order_by('stock__name')
    if(stock_name!=''):
        q = q.filter(stock__name=stock_name)
    if(family!=''):
        q = q.filter(family_type=family)
    start_end_date_form = StartEndDateForm(request.GET or None)
    if(start_end_date_form.is_valid()):
        start_date = start_end_date_form.cleaned_data['start_date']
        end_date = start_end_date_form.cleaned_data['end_date']
        q = q.filter(date__range=[start_date, end_date])
    
    return render(request, 'distribution_summary.html',
                  RequestContext(request, {'distributions': q,
                                           'category': request.GET.get('category', ''),
                                           'stock_name': stock_name,
                                           'family_type': family,
                                           'start_end_date_form': start_end_date_form}))

def transfer_out_summary(request):
    destination = request.GET.get('destination', '')
    stock_name = request.GET.get('stock_name', '')
    category = re.split(', | ', request.GET.get('category', ''))

    if(category==['']):
        q = Transfer.objects.all().order_by('stock__name')
    else:
        cL = Category.objects.filter(name__in=category)
        sList = [c.stock.pk for c in cL]
        q = Transfer.objects.filter(pk__in=sList).order_by('stock__name')
    if(stock_name!=''):
        q = q.filter(stock__name=stock_name)
    if(destination!=''):
        q = q.filter(destination__name=destination)
    start_end_date_form = StartEndDateForm(request.GET or None)
    if(start_end_date_form.is_valid()):
        start_date = start_end_date_form.cleaned_data['start_date']
        end_date = start_end_date_form.cleaned_data['end_date']
        q = q.filter(date__range=[start_date, end_date])
    
    return render(request, 'transfer_out_summary.html',
                  RequestContext(request, {'transfers': q,
                                           'category': request.GET.get('category', ''),
                                           'stock_name': stock_name,
                                           'destination': destination,
                                           'start_end_date_form': start_end_date_form}))

def vendor_summary(request):
    vendors = Vendor.objects.all().order_by('name')
    
    return render(request, 'vendor_summary.html',
                  RequestContext(request, {'vendors': vendors}))

def donor_summary(request):
    donors = Donor.objects.all().order_by('name')
    
    return render(request, 'donor_summary.html',
                  RequestContext(request, {'donors': donors}))


    
################################################################################
# Autocomplete
################################################################################
    
def get_donors(request):
    q = request.GET.get('term', '')
    donors = Donor.objects.filter(name__icontains = q)[:20]
    results = [{'label': '%s, tel: %s' % (donor.name, donor.contact_no),
                'name': donor.name,
                'address': donor.address,
                'contact_no': donor.contact_no,
                'mailing': donor.mailing,
                'referral': donor.referral,
            } for donor in donors]
    data = simplejson.dumps(results)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def get_stocks(request):
    q = request.GET.get('term', '')
    stocks = Stock.objects.filter(name__icontains = q)[:20]
    cList = Category.objects.filter(stock__name__icontains = q)
    categorys = set()
    categorys = {c.name for c in cList if c.name not in categorys}
    catSlug = ''
    for category in categorys:
        catSlug += category + ', '
    results = [{'value': '%s - $%s/%s' % (stock.name, stock.unit_price, stock.unit_measure),
                'name': stock.name,
                'unit_measure': stock.unit_measure,
                'unit_price': stock.unit_price,
                'categorys': catSlug,
            } for stock in stocks]
    data = simplejson.dumps(results)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def get_vendors(request):
    q = request.GET.get('term', '')
    vendors = Vendor.objects.filter(name__icontains = q)[:20]
    results = [{'value': '%s, address: %s, tel: %s' % (vendor.name, vendor.address, vendor.contact_no),
                'name': vendor.name,
                'address': vendor.address,
                'contact_no': vendor.contact_no,
            } for vendor in vendors]
    data = simplejson.dumps(results)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def get_categorys(request):
    q = request.GET.get('term', '')
    categorys = Category.objects.filter(name__icontains = q)[:20]
    cList = {}
    cList = {c.name for c in categorys if c.name not in cList}
    results = [{'value': category} for category in cList]
    data = simplejson.dumps(results)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def get_destination(request):
    q = request.GET.get('term', '')
    destinations = Destination.objects.filter(name__icontains = q)[:20]
    results = [{'value': '%s, tel: %s' % (destination.name, destination.contact_no),
                'name': destination.name,
                'person_in_charge': destination.person_in_charge,
                'contact_no': destination.contact_no,
            } for destination in destinations]
    data = simplejson.dumps(results)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)



    
################################################################################
# EXCEL generation
################################################################################

import xlwt3 as xlwt

def stock_summary_report(request):
    stock_name = request.GET.get('stock_name', '')
    category = re.split(', | |,|' , request.GET.get('category', ''))
    stock = Stock.objects.all().order_by('name', 'unit_measure')
    if(category != ['']):
        cL = Category.objects.filter(name__in=category)
        sList = [c.stock.pk for c in cL]
        stock = stock.filter(pk__in=sList)
    if(stock_name != ''):
        stock = stock.filter(name=stock_name)
    
    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet('my_sheet')

    header = ['Name', 'Unit Measure', 'Unit Price','Total']
    for hcol, hcol_data in enumerate(header):
        sheet.write(0, hcol, hcol_data)

    row = 0

    for item in stock:
        row = row + 1
        sheet.write(row, 0, item.name)
        sheet.write(row, 1, item.unit_measure)
        sheet.write(row, 2, item.unit_price)
        sheet.write(row, 3, item.current_amt())
        
    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=stock_summary_report.xls'
    book.save(response)
    return response

def donation_report(request):
    donor_name = request.GET.get('donor_name', '')
    stock_name = request.GET.get('stock_name', '')
    category = re.split(', | ', request.GET.get('category', ''))
    donation = Donate.objects.all().order_by('stock__name','stock__unit_measure')
    
    if(request.GET.get('start_date')!='' and request.GET.get('end_date')!=''):
        start_date = datetime.datetime.strptime(request.GET.get('start_date'), "%b. %d, %Y")
        end_date = datetime.datetime.strptime(request.GET.get('end_date'), "%b. %d, %Y")
        donation = donation.filter(date__range=[start_date, end_date])
    if(category!=['']):
        cL = Category.objects.filter(name__in=category)
        sList = [c.stock.pk for c in cL]
        donation = donation.filter(pk__in=sList).order_by('stock__name')
    if(stock_name!=''):
        donation = donation.filter(stock__name=stock_name)
    if(donor_name!=''):
        donation = donation.filter(donor__name=donor_name)      
    
    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet('my_sheet')

    header = ['Donor', 'Donated Stock', 'Unit Measure', 'Quantity', 'Date']
    for hcol, hcol_data in enumerate(header):
        sheet.write(0, hcol, hcol_data)

    row = 0

    for item in donation:
        row = row + 1
        sheet.write(row, 0, Donor.objects.get(id = item.donor_id).name)
        stock = Stock.objects.get(id = item.stock_id)
        sheet.write(row, 1, stock.name)
        sheet.write(row, 2, stock.unit_measure)
        sheet.write(row, 3, item.quantity)
        sheet.write(row, 4, item.date.strftime("%Y/%m/%d"))
        
    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=donation_report.xls'
    book.save(response)
    return response

def purchase_report(request):
    vendor_name = request.GET.get('vendor_name', '')
    stock_name = request.GET.get('stock_name', '')
    category = re.split(', | ', request.GET.get('category', ''))
    purchase = Purchase.objects.all().order_by('stock__name','stock__unit_measure')

    if(request.GET.get('start_date')!='' and request.GET.get('end_date')!=''):
        start_date = datetime.datetime.strptime(request.GET.get('start_date'), "%b. %d, %Y")
        end_date = datetime.datetime.strptime(request.GET.get('end_date'), "%b. %d, %Y")
        purchase = purchase.filter(date__range=[start_date, end_date])
    if(category!=['']):
        cL = Category.objects.filter(name__in=category)
        sList = [c.stock.pk for c in cL]
        purchase = purchase.filter(pk__in=sList).order_by('stock__name')
    if(stock_name!=''):
        purchase = purchase.filter(stock__name=stock_name)
    if(vendor_name!=''):
        purchase = purchase.filter(vendor__name=vendor_name)
    
    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet('my_sheet')

    header = ['Vendor', 'Purchased Stock', 'Unit Measure','Quantity','Date']
    for hcol, hcol_data in enumerate(header):
        sheet.write(0, hcol, hcol_data)

    row = 0
 
    for item in purchase:
        row = row + 1
        sheet.write(row, 0, Vendor.objects.get(id = item.vendor_id).name)
        stock = Stock.objects.get(id = item.stock_id)
        sheet.write(row, 1, stock.name)
        sheet.write(row, 2, stock.unit_measure)
        sheet.write(row, 3, item.quantity)
        sheet.write(row, 4, item.date.strftime("%Y/%m/%d"))
        
    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Purchase_report.xls'
    book.save(response)
    return response

def distribution_report(request):
    family = request.GET.get('family_type', '')
    stock_name = request.GET.get('stock_name', '')
    category = re.split(', | ', request.GET.get('category', ''))
    distribute = Distribute.objects.all().order_by('stock__name','stock__unit_measure')

    if(request.GET.get('start_date')!='' and request.GET.get('end_date')!=''):
        start_date = datetime.datetime.strptime(request.GET.get('start_date'), "%b. %d, %Y")
        end_date = datetime.datetime.strptime(request.GET.get('end_date'), "%b. %d, %Y")
        distribute = distribute.filter(date__range=[start_date, end_date])
    if(category!=['']):
        cL = Category.objects.filter(name__in=category)
        sList = [c.stock.pk for c in cL]
        distribute = distribute.filter(pk__in=sList).order_by('stock__name')
    if(stock_name!=''):
        distribute = distribute.filter(stock__name=stock_name)
    if(family!=''):
        distribute = distribute.filter(family=family_type)
    
    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet('my_sheet')

    header = ['Stock', 'Unit Measure' ,'Quantity','Family Type','Date']
    for hcol, hcol_data in enumerate(header):
        sheet.write(0, hcol, hcol_data)

    row = 0

    for item in distribute:
        row = row + 1
        stock = Stock.objects.get(id = item.stock_id)
        sheet.write(row, 0, stock.name)
        sheet.write(row, 1, stock.unit_measure)
        sheet.write(row, 2, item.quantity)
        sheet.write(row, 3, item.family_type)
        sheet.write(row, 4, item.date.strftime("%Y/%m/%d"))
        
    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=distribution_report.xls'
    book.save(response)
    return response

def transfer_out_report(request):
    destination = request.GET.get('destination', '')
    stock_name = request.GET.get('stock_name', '')
    category = re.split(', | ', request.GET.get('category', ''))
    transfer = Transfer.objects.all().order_by('stock__name','stock__unit_measure')

    if(request.GET.get('start_date')!='' and request.GET.get('end_date')!=''):
        start_date = datetime.datetime.strptime(request.GET.get('start_date'), "%b. %d, %Y")
        end_date = datetime.datetime.strptime(request.GET.get('end_date'), "%b. %d, %Y")
        transfer = transfer.filter(date__range=[start_date, end_date])
    if(category!=['']):
        cL = Category.objects.filter(name__in=category)
        sList = [c.stock.pk for c in cL]
        transfer = transfer.filter(pk__in=sList).order_by('stock__name')
    if(stock_name!=''):
        transfer = transfer.filter(stock__name=stock_name)
    if(destination!=''):
        transfer = transfer.filter(destination__name=destination)

    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet('my_sheet')

    header = ['Stock', 'Unit measure', 'Quantity', 'Destination','Date']
    for hcol, hcol_data in enumerate(header):
        sheet.write(0, hcol, hcol_data)

    row = 0

    for item in transfer:
        row = row + 1
        stock = Stock.objects.get(id = item.stock_id)
        sheet.write(row, 0, stock.name)
        sheet.write(row, 1, stock.unit_measure)
        sheet.write(row, 2, item.quantity)
        sheet.write(row, 3, Destination.objects.get(id = item.destination_id).name)
        sheet.write(row, 4, item.date.strftime("%Y/%m/%d"))
        
    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=transfer_out_report.xls'
    book.save(response)
    return response

def vendor_report(request):
    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet('my_sheet')

    header = ['Name', 'Address', 'Contact Number']
    for hcol, hcol_data in enumerate(header):
        sheet.write(0, hcol, hcol_data)

    row = 0
    vendor = Vendor.objects.order_by('name','address')
    for item in vendor:
        row = row + 1
        sheet.write(row, 0, item.name)
        sheet.write(row, 1, item.address)
        sheet.write(row, 2, item.contact_no)
        
    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=vendor_report.xls'
    book.save(response)
    return response

def donor_report(request):
    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet('my_sheet')

    header = ['Name', 'Address', 'Contact Number', 'mailing', 'Referral']
    for hcol, hcol_data in enumerate(header):
        sheet.write(0, hcol, hcol_data)

    row = 0
    donor = Donor.objects.order_by('name','address')
    for item in donor:
        row = row + 1
        sheet.write(row, 0, item.name)
        sheet.write(row, 1, item.address)
        sheet.write(row, 2, item.contact_no)
        mail = {0:'NO', 1:'YES'}
        sheet.write(row, 3, mail[item.mailing])
        referral_types = {'F':'FM 97.2', 'C':'SYCC Client', 'V':'SYCC Volunteer',
                    'R':'Regular Donor', 'O':'Others'}
        sheet.write(row, 4, referral_types[item.referral])
        
    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=donor_report.xls'
    book.save(response)
    return response
