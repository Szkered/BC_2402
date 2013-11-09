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
        this_donation = Donation.objects.create(
            date=date_form.cleaned_data['date'],
            donor=d,
        )
        for donate_form in donate_formset:
            s, created = Stock.objects.get_or_create(
                name=donate_form.cleaned_data['stock_name'],
                unit_measure=donate_form.cleaned_data['unit_measure'],
                defaults={'unit_price':donate_form.cleaned_data['unit_price']}
            )
            s.unit_price = donate_form.cleaned_data['unit_price']
            s.save()

            donate = Donate.objects.create(
                quantity=donate_form.cleaned_data['quantity'],
                stock=s,
                donation=this_donation,
            )
            category_list = re.split(
                ', | |,',
                donate_form.cleaned_data['category']
            )
            for item in category_list:
                if item != '':
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
                unit_measure=purchase_form.cleaned_data['unit_measure'],
                defaults={'unit_price':purchase_form.cleaned_data['unit_price']},
            )
            purchase = Purchase.objects.create(
                order=o,
                quantity=purchase_form.cleaned_data['quantity'],
                stock=s,
                price=purchase_form.cleaned_data['unit_price'],
            )
            category_list = re.split(
                ', | |,',
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
    now = datetime.datetime.now()
    # create formset
    standard_item = [item.stock for item in Category.objects.filter(name="standard")]
    cList = [item.current_amt(now) for item in standard_item]
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
                                       'zip': zip(standard_item, distribution_formset, cList)})
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

            if form.cleaned_data['remark']:
                r = form.cleaned_data['remark']
            else:
                r = ''
                
            transfer = Transfer.objects.create(
                date=date_form.cleaned_data['date'],
                quantity=form.cleaned_data['quantity'],
                destination=d,
                remark=r,
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
        
def adjust(request):
    adjust_form = AdjustForm(request.POST or None)
    
    if(adjust_form.is_valid()):
        corret_amt = adjust_form.cleaned_data['current_amount']
        target_stock = Stock.objects.get(name=adjust_form.cleaned_data['stock_name'],
                                         unit_measure=adjust_form.cleaned_data['unit_measure'])
        if(corret_amt > target_stock.current_amt(datetime.datetime.now())):
            adjustment = corret_amt - target_stock.current_amt(datetime.datetime.now())
            super_d, created = Donor.objects.get_or_create(
                name="adjust",
                address="adjust",
                contact_no="1",
                mailing=False,
                referral='O',
            )
            d = Donation.objects.create(
                date=datetime.datetime.now(),
                donor=super_d,                
            )
            Donate.objects.create(
                quantity=adjustment,
                stock=target_stock,
                donation=d,
            )
        else:
            adjustment = target_stock.current_amt(datetime.datetime.now()) - corret_amt
            super_d, created = Destination.objects.get_or_create(
                name="adjust",
                person_in_charge="adjust",
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

def initialization(request):
    init_formset = StockInFormSet(request.POST or None)

    if(init_formset.is_valid()):
        super_d, created = Donor.objects.get_or_create(
            name="init",
            address="init",
            contact_no="1",
            mailing=False,
            referral='O',
        )
        for init_form in init_formset:
            init_stock = Stock.objects.create(
                name=init_form.cleaned_data['stock_name'],
                unit_measure=init_form.cleaned_data['unit_measure'],
                unit_price=init_form.cleaned_data['unit_price'],
            )
            d = Donation.objects.create(
                date=datetime.datetime.now(),
                donor=super_d,
            )
            Donate.objects.create(
                quantity=init_form.cleaned_data['quantity'],
                stock=init_stock,
                donation=d,
            )
            category_list = re.split(
                ', | |,',
                init_form.cleaned_data['category']
            )
            for item in category_list:
                if item != '':
                    category, created = Category.objects.get_or_create(
                        stock=init_stock,
                        name=item,
                    )

        return HttpResponseRedirect('thanks')
        
    return render(request, 'init.html',
                  RequestContext(request, {'init_formset': init_formset}))

    
def historical_amt(request):
    date_form = DateForm(request.GET or None)
    stock_name = request.GET.get('stock_name', '')
    category = re.split(', | |,', request.GET.get('category', ''))

    q = Stock.objects.all().order_by('name')

    if(category!=['']):
        sList = [c.stock.pk for c in Category.objects.filter(name__in=category)]
        q = q.filter(pk__in=sList)
        
    if(stock_name!=''):
        q = q.filter(name=stock_name)

    if(date_form.is_valid()):
        date = date_form.cleaned_data['date']
        results = [{'stock': stock,
                    'category': stock.category_slug(),
                    'quantity': stock.current_amt(date),
                    'cash_value': stock.total_price(date)} for stock in q]
    else:
        results = []
        
    return render(request, 'historical_amt.html',
                  RequestContext(request, {'date_form': date_form,
                                           'stocks': results}))
    

def merge_stock(request):
    merge_form = MergeForm(request.GET or None)
    target_form = TargetForm(request.GET or None)
    merge_check_form = MergeCheckForm(request.POST or None)
    now = datetime.datetime.now()
    
    if(merge_form.is_valid() and target_form.is_valid()):
        request.session['merge_stock_unit_measure']=merge_form.cleaned_data['merge_stock_unit_measure']
        request.session['target_stock_unit_measure']=target_form.cleaned_data['target_stock_unit_measure']
        request.session['target_stock_name']=target_form.cleaned_data['target_stock_name']
        request.session['merge_stock_name']=merge_form.cleaned_data['merge_stock_name']

    target_stock_name = request.session.get('target_stock_name', None)
    target_stock_unit_measure = request.session.get('target_stock_unit_measure', None)
    merge_stock_name = request.session.get('merge_stock_name', None)
    merge_stock_unit_measure = request.session.get('merge_stock_unit_measure', None)
    
    if(target_stock_name and merge_stock_name and
       target_stock_unit_measure and merge_stock_unit_measure):
        target_stock = Stock.objects.get(
            name=target_stock_name,
            unit_measure=target_stock_unit_measure
        )
        merge_stock = Stock.objects.get(
            name=merge_stock_name,
            unit_measure=merge_stock_unit_measure
        )
        target_stock_quantity = target_stock.current_amt(now)
        target_stock_cash_value = float(target_stock.total_price(now))
        merge_stock_quantity = merge_stock.current_amt(now)
        merge_stock_cash_value = float(merge_stock.total_price(now))
        merged_cash_value = "%.2f" % (target_stock_cash_value + merge_stock_cash_value)
    else:
        target_stock = None
        merge_stock = None
        target_stock_quantity = ''
        target_stock_cash_value = ''
        merge_stock_quantity = ''
        merge_stock_cash_value = ''
        merged_cash_value = ''

    if(merge_check_form.is_valid()):
        confirm = merge_check_form.cleaned_data['confirm']
        if(confirm == True and merge_stock and target_stock):
            donates = Donate.objects.filter(stock=merge_stock)
            for item in donates:
                item.stock = target_stock
                item.save()
                
            purchases = Purchase.objects.filter(stock=merge_stock)
            for item in purchases:
                item.stock = target_stock
                item.save()
                
            distributes = Distribute.objects.filter(stock=merge_stock)
            for item in distributes:
                item.stock = target_stock
                item.save()
                
            transfers = Transfer.objects.filter(stock=merge_stock)
            for item in transfers:
                item.stock = target_stock
                item.save()

            merge_stock.delete()
            del request.session['merge_stock_unit_measure']
            del request.session['target_stock_unit_measure']
            del request.session['target_stock_name']
            del request.session['merge_stock_name']
                
            return HttpResponseRedirect('thanks')
                            
    
    return render(request, 'merge_stock.html',
                  RequestContext(request, {'merge_form': merge_form,
                                           'target_form': target_form,
                                           'target_stock_quantity': target_stock_quantity,
                                           'target_stock_cash_value': target_stock_cash_value,
                                           'merge_stock_quantity': merge_stock_quantity,
                                           'merge_stock_cash_value': merge_stock_cash_value,
                                           'merge_check_form': merge_check_form,
                                           'target_stock': target_stock,
                                           'merge_stock': merge_stock,
                                           'merged_cash_value': merged_cash_value}))
    



################################################################################
# Edit
################################################################################

def donation_edit(request):
    start_end_date_form = StartEndDateForm(request.GET or None)

    q = Donation.objects.exclude(donor__name='init')
    
    if(start_end_date_form.is_valid()):
        start_date = start_end_date_form.cleaned_data['start_date']
        end_date = start_end_date_form.cleaned_data['end_date']
        if(start_date!=None):
            q = q.filter(date__gte=start_date)
        if(end_date!=None):
            q = q.filter(date__lte=end_date)


    donate_list = [Donate.objects.filter(donation=item) for item in q]
    
    donation_formset = DonationFormSet(request.POST or None, queryset=q)
    
    if(donation_formset.is_valid()):
        donation_formset.save()
        return HttpResponseRedirect('thanks')
        
    return render(request, 'donation_edit.html',
                  RequestContext(request, {
                      'zip': zip(donation_formset, donate_list),
                      'donation_formset': donation_formset,
                      'start_end_date_form': start_end_date_form}))
    
def donate_edit(request, d_id):
    d = Donation.objects.get(pk=d_id)
    q = Donate.objects.filter(donation=d)
    
    donate_formset = DonateFormSet(request.POST or None, queryset=q)
    
    if(donate_formset.is_valid()):
        donate_formset.save()
        return HttpResponseRedirect('thanks')
        
    return render(request, 'donate_edit.html',
                  RequestContext(request, {'donate_formset': donate_formset,
                                           'donation': d}))

def purchase_edit(request, o_id):
    o = Order.objects.get(pk=o_id)
    q = Purchase.objects.filter(order=o)
    
    purchase_formset = PurchaseFormSet(request.POST or None, queryset=q)
    
    if(purchase_formset.is_valid()):
        purchase_formset.save()
        return HttpResponseRedirect('thanks')
        
    return render(request, 'purchase_edit.html',
                  RequestContext(request, {'order': o,
                                           'purchase_formset': purchase_formset}))

    
def order_edit(request):
    start_end_date_form = StartEndDateForm(request.GET or None)

    q = Order.objects.all()

    if(start_end_date_form.is_valid()):
        start_date = start_end_date_form.cleaned_data['start_date']
        end_date = start_end_date_form.cleaned_data['end_date']
        if(start_date!=None):
            q = q.filter(date__gte=start_date)
        if(end_date!=None):
            q = q.filter(date__lte=end_date)


    purchase_list = [Purchase.objects.filter(order=item) for item in q]
    
    order_formset = OrderFormSet(request.POST or None, queryset=q)
    if(order_formset.is_valid()):
        order_formset.save()
        return HttpResponseRedirect('thanks')
        
    return render(request, 'order_edit.html',
                  RequestContext(request, {
                      'zip': zip(order_formset, purchase_list),
                      'order_formset': order_formset,
                      'start_end_date_form': start_end_date_form}))
    

    
def transfer_edit(request):
    TransferFormSet = modelformset_factory(Transfer, extra=0)
    start_end_date_form = StartEndDateForm(request.GET or None)
    destination_name = request.GET.get('destination_name', '')
    stock_name = request.GET.get('stock_name', '')
    category = re.split(', | |,', request.GET.get('category', ''))
    
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
        if(start_date!=None):
            q = q.filter(date__gte=start_date)
        if(end_date!=None):
            q = q.filter(date__lte=end_date)

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
    start_end_date_form = StartEndDateForm(request.GET or None)
    family_form = FamilyForm(request.GET or None)
    stock_name = request.GET.get('stock_name', '')
    category = re.split(', | |,', request.GET.get('category', ''))
    
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
        if(start_date!=None):
            q = q.filter(date__gte=start_date)
        if(end_date!=None):
            q = q.filter(date__lte=end_date)        

            
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
    vendor_name = request.GET.get('id_name', '')
    q = Vendor.objects.exclude(name='adjust')
    
    if(vendor_name==''):
        vendor_formset = VendorFormSet(request.POST or None)
    else:
        q = q.filter(name=vendor_name)
        
    vendor_formset = VendorFormSet(request.POST or None, queryset=q)
    
    if(vendor_formset.is_valid()):
        vendor_formset.save()
        return HttpResponseRedirect('thanks')
    return render(request, 'vendor_edit.html',
                  RequestContext(request, {'vendor_formset': vendor_formset}))

def donor_edit(request):
    donor_name = request.GET.get('id_name', '')
    q = Donor.objects.exclude(name='init').order_by('name')
    q = q.exclude(name='adjust')
    
    if(donor_name==''):
        donor_formset = DonorFormSet(request.POST or None)
    else:
        q = q.filter(name=donor_name)
        
    donor_formset = DonorFormSet(request.POST or None, queryset=q)
    
    if(donor_formset.is_valid()):
        donor_formset.save()
        return HttpResponseRedirect('thanks')
        
    return render(request, 'donor_edit.html',
                  RequestContext(request, {'donor_formset': donor_formset}))

def stock_edit(request):
    stock_name = request.GET.get('stock_name', '')
    category = re.split(', | |,', request.GET.get('category', ''))
    
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
            c = "%s_%s" % (s.name, s.unit_measure)
            new_cList = re.split(', | |,', request.POST.get(c, ''))
            old_cList = re.split(', | |,', s.category_slug())
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
    category = re.split(', | |,', request.GET.get('category', ''))

    q = Stock.objects.all().order_by('name')

    if(category!=['']):
        sList = [c.stock.pk for c in Category.objects.filter(name__in=category)]
        q = q.filter(pk__in=sList)
        
    if(stock_name!=''):
        q = q.filter(name=stock_name)

        
    results = [{'stock': stock,
                'category': stock.category_slug(),
                'quantity': stock.current_amt(datetime.datetime.now()),
                'cash_value': stock.total_price(datetime.datetime.now())} for stock in q]
    
    return render(request, 'stock_summary.html',
                  RequestContext(request, {'stocks': results,
                                           'category': request.GET.get('category', ''),
                                           'stock_name': stock_name}))

def donation_summary(request):
    donor_name = request.GET.get('donor_name', '')
    stock_name = request.GET.get('stock_name', '')
    category = re.split(', | |,', request.GET.get('category', ''))
    start_end_date_form = StartEndDateForm(request.GET or None)

    if(category==['']):
        q = Donate.objects.exclude(donation__donor__name='init').order_by('stock__name')
        q = q.exclude(donation__donor__name='adjust')
    else:
        sList = [c.stock for c in Category.objects.filter(name__in=category)]
        q = Donate.objects.filter(stock__in=sList).order_by('stock__name')
        
    if(stock_name!=''):
        q = q.filter(stock__name=stock_name)
        
    if(donor_name!=''):
        q = q.filter(donation__donor__name=donor_name)


    if(start_end_date_form.is_valid()):
        start_date = start_end_date_form.cleaned_data['start_date']
        end_date = start_end_date_form.cleaned_data['end_date']
        if(start_date!=None):
            q = q.filter(donation__date__gte=start_date)
        if(end_date!=None):
            q = q.filter(donation__date__lte=end_date)

    stock_list = [d.stock.pk for d in q]
    stocks = Stock.objects.filter(pk__in=stock_list).order_by('name')
    
    results = [{'stock': stock,
                'category': stock.category_slug(),
                'quantity': stock.query_amt(q),
                'cash_value': stock.query_price(q)} for stock in stocks]

    return render(request, 'donation_summary.html',
                  RequestContext(request, {'results': results,
                                           'category': request.GET.get('category', ''),
                                           'stock_name': stock_name,
                                           'donor_name': donor_name,
                                           'start_end_date_form': start_end_date_form}))

def purchase_summary(request):
    vendor_name = request.GET.get('vendor_name', '')
    stock_name = request.GET.get('stock_name', '')
    category = re.split(', | |,', request.GET.get('category', ''))
    start_end_date_form = StartEndDateForm(request.GET or None)

    if(category==['']):
        q = Purchase.objects.all().order_by('order__date')
    else:
        sList = [c.stock.pk for c in Category.objects.filter(name__in=category)]
        q = Purchase.objects.filter(pk__in=sList).order_by('stock__name')
        
    if(stock_name!=''):
        q = q.filter(stock__name=stock_name)
    if(vendor_name!=''):
        q = q.filter(vendor__name=vendor_name)
            

    if(start_end_date_form.is_valid()):
        start_date = start_end_date_form.cleaned_data['start_date']
        end_date = start_end_date_form.cleaned_data['end_date']
        if(start_date!=None):
            q = q.filter(order__date__gte=start_date)
        if(end_date!=None):
            q = q.filter(order__date__lte=end_date)
                
    return render(request, 'Purchase_summary.html',
                  RequestContext(request, {'purchases': q,
                                           'category': request.GET.get('category', ''),
                                           'stock_name': stock_name,
                                           'vendor_name': vendor_name,
                                           'start_end_date_form': start_end_date_form}))

def distribution_summary(request):
    family = request.GET.get('family_type', '')
    stock_name = request.GET.get('stock_name', '')
    category = re.split(', | |,', request.GET.get('category', ''))

    q = Distribute.objects.all().order_by('stock__name')
    
    if(category!=['']):
        cL = Category.objects.filter(name__in=category)
        sList = [c.stock.pk for c in cL]
        q = q.filter(pk__in=sList).order_by('stock__name')
        
    if(stock_name!=''):
        q = q.filter(stock__name=stock_name)
        
    if(family!=''):
        q = q.filter(family_type=family)
        
    start_end_date_form = StartEndDateForm(request.GET or None)
    
    if(start_end_date_form.is_valid()):
        start_date = start_end_date_form.cleaned_data['start_date']
        end_date = start_end_date_form.cleaned_data['end_date']
        if(start_date!=None):
            q = q.filter(date__gte=start_date)
        if(end_date!=None):
            q = q.filter(date__lte=end_date)

    stock_list = [d.stock.pk for d in q]
    stocks = Stock.objects.filter(pk__in=stock_list).order_by('name')
    
    results = [{'stock': stock,
                'quantity': stock.query_amt(q),
                'cash_value': stock.query_price(q)} for stock in stocks]
    
    return render(request, 'distribution_summary.html',
                  RequestContext(request, {'results': results,
                                           'category': request.GET.get('category', ''),
                                           'stock_name': stock_name,
                                           'family_type': family,
                                           'start_end_date_form': start_end_date_form}))

def transfer_out_summary(request):
    destination = request.GET.get('destination', '')
    stock_name = request.GET.get('stock_name', '')
    category = re.split(', | |,', request.GET.get('category', ''))
    start_end_date_form = StartEndDateForm(request.GET or None)

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
            

    if(start_end_date_form.is_valid()):
        start_date = start_end_date_form.cleaned_data['start_date']
        end_date = start_end_date_form.cleaned_data['end_date']
        if(start_date!=None):
            q = q.filter(date__gte=start_date)
        if(end_date!=None):
            q = q.filter(date__lte=end_date)

    
    return render(request, 'transfer_out_summary.html',
                  RequestContext(request, {'transfers': q,
                                           'category': request.GET.get('category', ''),
                                           'stock_name': stock_name,
                                           'destination': destination,
                                           'start_end_date_form': start_end_date_form}))

def vendor_summary(request):
    vendors = Vendor.objects.exclude(name='adjust').order_by('name')
    
    return render(request, 'vendor_summary.html',
                  RequestContext(request, {'vendors': vendors}))

def donor_summary(request):
    donors = Donor.objects.exclude(name='adjust').order_by('name')
    donors = donors.exclude(name='init')
    
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
                'email': donor.email,
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
                'email': vendor.email,
                'fax': vendor.fax,
                'contact_person_name': vendor.contact_person_name,
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
    category = re.split(', | |,' , request.GET.get('category', ''))
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
        sheet.write(row, 2, "%.3f" % item.unit_price)
        sheet.write(row, 3, item.current_amt(datetime.datetime.now()))
        
    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=stock_summary_report.xls'
    book.save(response)
    return response

def donation_report(request):
    donor_name = request.GET.get('donor_name', '')
    stock_name = request.GET.get('stock_name', '')
    category = re.split(', | |,', request.GET.get('category', ''))
    donation = Donate.objects.all().order_by('stock__name','stock__unit_measure')
    
    if(request.GET.get('start_date', '')!='' and request.GET.get('end_date', '')!=''):
        start_date = datetime.datetime.strptime(request.GET.get('start_date'), "%b. %d, %Y")
        end_date = datetime.datetime.strptime(request.GET.get('end_date'), "%b. %d, %Y")
        if(start_date!=None):
            donation = donation.filter(date__gte=start_date)
        if(end_date!=None):
            donation = donation.filter(date__lte=end_date)

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

    header = ['Donor', 'Donated Stock', 'Unit Measure', 'Price', 'Quantity', 'Date']
    for hcol, hcol_data in enumerate(header):
        sheet.write(0, hcol, hcol_data)

    row = 0

    donation.exclude(donation__donor__name='init').exclude(donation__donor__name='adjust')
    
    for item in donation:
        row = row + 1
        sheet.write(row, 0, Donor.objects.get(id = item.donation.donor_id).name)
        sheet.write(row, 1, item.stock.name)
        sheet.write(row, 2, item.stock.unit_measure)
        sheet.write(row, 3, "%.3f" % item.stock.unit_price)
        sheet.write(row, 4, item.quantity)
        sheet.write(row, 5, item.donation.date.strftime("%Y/%m/%d"))
        
    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=donation_report.xls'
    book.save(response)
    return response

def purchase_report(request):
    vendor_name = request.GET.get('vendor_name', '')
    stock_name = request.GET.get('stock_name', '')
    category = re.split(', | |,', request.GET.get('category', ''))
    purchase = Purchase.objects.all().order_by('stock__name','stock__unit_measure')

    if(request.GET.get('start_date', '')!='' and request.GET.get('end_date', '')!=''):
        start_date = datetime.datetime.strptime(request.GET.get('start_date'), "%b. %d, %Y")
        end_date = datetime.datetime.strptime(request.GET.get('end_date'), "%b. %d, %Y")
        if(start_date!=None):
            purchase = purchase.filter(order__date__gte=start_date)
        if(end_date!=None):
            purchase = purchase.filter(order__date__lte=end_date)

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

    header = ['Vendor', 'Address', 'Email', 'Contact No', 'Contact Person', 'Fax', 'Purchased Stock','Unit Measure', 'Price','Quantity','Date']
    for hcol, hcol_data in enumerate(header):
        sheet.write(0, hcol, hcol_data)

    row = 0
    
    for item in purchase:
        row = row + 1
        vendor = Vendor.objects.get(id = item.order.vendor.id)
        sheet.write(row, 0, vendor.name)
        sheet.write(row, 1, vendor.address)
        sheet.write(row, 2, vendor.email)
        sheet.write(row, 3, vendor.contact_no)
        sheet.write(row, 4, vendor.contact_person_name)
        sheet.write(row, 5, vendor.fax)
        
        sheet.write(row, 6, item.stock.name)
        sheet.write(row, 7, item.stock.unit_measure)
        sheet.write(row, 8, "%.3f" % item.price)
        sheet.write(row, 9, item.quantity)
        sheet.write(row, 10, item.order.date.strftime("%Y/%m/%d"))
        
    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Purchase_report.xls'
    book.save(response)
    return response

def distribution_report(request):
    family = request.GET.get('family_type', '')
    stock_name = request.GET.get('stock_name', '')
    category = re.split(', | |,', request.GET.get('category', ''))
    distribute = Distribute.objects.all().order_by('stock__name','stock__unit_measure')

    if(request.GET.get('start_date')!='' and request.GET.get('end_date')!=''):
        start_date = datetime.datetime.strptime(request.GET.get('start_date'), "%b. %d, %Y")
        end_date = datetime.datetime.strptime(request.GET.get('end_date'), "%b. %d, %Y")
        if(start_date!=None):
            distribute = distribute.filter(date__gte=start_date)
        if(end_date!=None):
            distribute = distribute.filter(date__lte=end_date)
                
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
    category = re.split(', | |,', request.GET.get('category', ''))
    transfer = Transfer.objects.all().order_by('stock__name','stock__unit_measure')

    if(request.GET.get('start_date')!='' and request.GET.get('end_date')!=''):
        start_date = datetime.datetime.strptime(request.GET.get('start_date'), "%b. %d, %Y")
        end_date = datetime.datetime.strptime(request.GET.get('end_date'), "%b. %d, %Y")
        if(start_date!=None):
            transfer = transfer.filter(date__gte=start_date)
        if(end_date!=None):
            transfer = transfer.filter(date__lte=end_date)

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

    transfer.exclude(destination__name='adjust')

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
        sheet.write(row, 3, item.email)
        
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
        sheet.write(row, 3, item.email)
        mail = {0:'NO', 1:'YES'}
        sheet.write(row, 3, mail[item.mailing])
        referral_types = {'F':'FM 97.2', 'C':'SYCC Client', 'V':'SYCC Volunteer',
                          'R':'Regular Donor', 'O':'Others'}
        sheet.write(row, 4, referral_types[item.referral])
        
    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=donor_report.xls'
    book.save(response)
    return response

##############################################################################
def purchase_order(request):
    start_end_date_form = StartEndDateForm(request.GET or None)

    q = Order.objects.all()

    if(start_end_date_form.is_valid()):
        start_date = start_end_date_form.cleaned_data['start_date']
        end_date = start_end_date_form.cleaned_data['end_date']
        if(start_date!=None):
            q = q.filter(date__gte=start_date)
        if(end_date!=None):
            q = q.filter(date__lte=end_date)


    purchase_list = [Purchase.objects.filter(order=item) for item in q]
    
    return render(request, 'purchase_order.html',
                  RequestContext(request, {
                      'zip': zip(q, purchase_list),
                      'start_end_date_form': start_end_date_form}))

def purchase_order_generate(request, o_id):
    o = Order.objects.get(pk=o_id)
    p = Purchase.objects.filter(order=o)
    total = sum([purchase.purchase_price() for purchase in p])
    sub_total = float("%.3f" % (total/1.07))
    gst = float("%.3f" % (total - sub_total))
    return render(request, 'purchase_order_generate.html',
                  RequestContext(request, {'order': o,
                                           'purchases':p,
                                           'total': total,
                                           'sub_total': sub_total,
                                           'gst': gst}))

def thank_you_letter(request):
    start_end_date_form = StartEndDateForm(request.GET or None)
    donor_name = request.GET.get('donor_name', '')

    q = Donation.objects.exclude(donor__name='init')

    if(donor_name!=''):
        q = q.filter(donor__name=donor_name)
        
    if(start_end_date_form.is_valid()):
        start_date = start_end_date_form.cleaned_data['start_date']
        end_date = start_end_date_form.cleaned_data['end_date']
        if(start_date!=None):
            q = q.filter(date__gte=start_date)
        if(end_date!=None):
            q = q.filter(date__lte=end_date)


    donate_list = [Donate.objects.filter(donation=item) for item in q]
    
    return render(request, 'thank_you_letter.html',
                  RequestContext(request, {
                      'zip': zip(q, donate_list),
                      'start_end_date_form': start_end_date_form}))

def letter_generate(request, d_id):
    now = datetime.datetime.now()
    d = Donation.objects.get(pk=d_id)
    q = Donate.objects.filter(donation=d)
    letter_id = "%s%s%s" % (now.year, now.month, d.pk)
    
    return render(request, 'thank_you_letter_generate.html',
                  RequestContext(request, {'donation':d ,
                                           'now': now,
                                           'letter_id': letter_id,
                                           'donates':q}))
