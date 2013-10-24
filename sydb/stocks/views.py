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
    return render(request, 'thanks.html')

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
                unit_price=donate_form.cleaned_data['unit_price'],
                unit_measure=donate_form.cleaned_data['unit_measure']
            )
            donate = Donate.objects.create(
                date=date_form.cleaned_data['date'],
                quantity=donate_form.cleaned_data['quantity'],
                stock=s,
                donor=d
            )
            category_list = re.split(
                ', | ',
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
            category_list = re.split(
                ', | ',
                     purchase_form.cleaned_data['category']
            )
            for item in category_list:
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
        
        
    
def donor(request):
    donor_list = Donor.objects.all()
    return render(request, 'donor.html',
                  RequestContext(request, {'donor_list': donor_list}))

################################################################################
# Report
################################################################################

def donation_summary(request):
    start_end_date_form = StartEndDateForm(request.GET or None)
    if(start_end_date_form.is_valid()):
        start_date = start_end_date_form.cleaned_data['start_date']
        end_date = start_end_date_form.cleaned_data['end_date']
        donations = Donate.objects.filter(date__range=[start_date, end_date])
    else:
        donations = Donate.objects.all()
    return render(request, 'donation_summary.html',
                  RequestContext(request, {'donations': donations,
                                           'start_end_date_form': start_end_date_form}))

def purchase_summary(request):
    start_end_date_form = StartEndDateForm(request.GET or None)
    if(start_end_date_form.is_valid()):
        start_date = start_end_date_form.cleaned_data['start_date']
        end_date = start_end_date_form.cleaned_data['end_date']
        purchases = Purchase.objects.filter(date__range=[start_date, end_date])
    else:
        purchases = Purchase.objects.all()
    return render(request, 'Purchase_summary.html',
                  RequestContext(request, {'purchases': purchases,
                                           'start_end_date_form': start_end_date_form}))

def distribution_summary(request):
    start_end_date_form = StartEndDateForm(request.GET or None)
    if(start_end_date_form.is_valid()):
        start_date = start_end_date_form.cleaned_data['start_date']
        end_date = start_end_date_form.cleaned_data['end_date']
        distributions = Distribute.objects.filter(date__range=[start_date, end_date])
    else:
        distributions = Distribute.objects.all()
    return render(request, 'distribution_summary.html',
                  RequestContext(request, {'distributions': distributions,
                                           'start_end_date_form': start_end_date_form}))

def transfer_out_summary(request):
    start_end_date_form = StartEndDateForm(request.GET or None)
    if(start_end_date_form.is_valid()):
        start_date = start_end_date_form.cleaned_data['start_date']
        end_date = start_end_date_form.cleaned_data['end_date']
        transfers = Transfer.objects.filter(date__range=[start_date, end_date])
    else:
        transfers = Transfer.objects.all()
    return render(request, 'transfer_out_summary.html',
                  RequestContext(request, {'transfers': transfers,
                                           'start_end_date_form': start_end_date_form}))
################################################################################


def confirmation(request):
    PurchaseFormSet = modelformset_factory(Purchase, extra=0)
    unconfirmed_purchases = Purchase.objects.filter(confirm=False).order_by('date')
    purchase_formset = PurchaseFormSet(request.POST or None, queryset=unconfirmed_purchases)
    if(purchase_formset.is_valid()):
        purchase_formset.save()
        return HttpResponseRedirect('thanks')
    return render(request, 'confirmation.html',
                  RequestContext(request, {'purchase_formset': purchase_formset,
                                           'unconfirmed_purchases': unconfirmed_purchases,
                                           'zip': zip(purchase_formset,
                                                      unconfirmed_purchases)}))

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
        catSlug += category + ' '
    results = [{'value': '%s - %s/%s' % (stock.name, stock.unit_price, stock.unit_measure),
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
def current_stock(request):
    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet('my_sheet')   
    
               # Adding style for cell
               # Create Alignment
#    alignment = xlwt.Alignment()
              
               # horz May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT,     
               # HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL,
               # HORZ_DISTRIBUTED
#    alignment.horz = xlwt.Alignment.HORZ_LEFT
               # May be: VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED,
               # VERT_DISTRIBUTED
#    alignment.vert = xlwt.Alignment.VERT_TOP
#    style = xlwt.XFStyle() # Create Style
#    style.alignment = alignment # Add Alignment to Style

    # write the header
    header = ['id','name', 'unit measure', 'unit Price']
    for hcol, hcol_data in enumerate(header): # [(0,'Header 1'), (1, 'Header 2'), (2,'Header 3'), (3,'Header 4')]
        sheet.write(0, hcol, hcol_data)
  
    # write your data, you can also get it from your model
#    data = ['genius', 'super', 'gorgeous', 'awesomeness']
#    for row, row_data in enumerate(data, start=1): # start from row no.1
#        for col, col_data in enumerate(row_data):
#                 sheet.write(row, col, col_data)

    row = 0
    stock = Stock.objects.order_by('name')
    for item in stock:
        row = row + 1
        sheet.write(row, 0, item.id)
        sheet.write(row, 1, item.name)
        sheet.write(row, 2, item.unit_measure)
        sheet.write(row, 3, item.unit_price)
    
        
    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=my_data.xls'
    book.save(response)
    return response

def stock_summary_report(request):
    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet('my_sheet')

    header = ['Name', 'Unit Measure', 'Unit Price','Total']
    for hcol, hcol_data in enumerate(header):
        sheet.write(0, hcol, hcol_data)

    row = 0
    stock = Stock.objects.order_by('name','unit_measure')
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
    start_date = datetime.datetime.strptime(request.GET.get('start_date'), "%b. %d, %Y")
    end_date = datetime.datetime.strptime(request.GET.get('end_date'), "%b. %d, %Y")
    
    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet('my_sheet')

    header = ['Donor', 'Donated Stock', 'Unit Measure', 'Quantity', 'Date']
    for hcol, hcol_data in enumerate(header):
        sheet.write(0, hcol, hcol_data)

    row = 0
    donation = Donate.objects.filter(date__range=[start_date, end_date]).order_by('stock__name','stock__unit_measure')
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
    start_date = datetime.datetime.strptime(request.GET.get('start_date'), "%b. %d, %Y")
    end_date = datetime.datetime.strptime(request.GET.get('end_date'), "%b. %d, %Y")

    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet('my_sheet')

    header = ['Vendor', 'Purchased Stock', 'Unit Measure','Quantity','Date']
    for hcol, hcol_data in enumerate(header):
        sheet.write(0, hcol, hcol_data)

    row = 0
    purchase = Purchase.objects.filter(date__range=[start_date, end_date]).order_by('stock__name','stock__unit_measure')
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
    start_date = datetime.datetime.strptime(request.GET.get('start_date'), "%b. %d, %Y")
    end_date = datetime.datetime.strptime(request.GET.get('end_date'), "%b. %d, %Y")
    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet('my_sheet')

    header = ['Stock', 'Unit Measure' ,'Quantity','Family Type','Date']
    for hcol, hcol_data in enumerate(header):
        sheet.write(0, hcol, hcol_data)

    row = 0
    distribute = Distribute.objects.filter(date__range=[start_date, end_date]).order_by('stock__name','family_type')
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
    start_date = datetime.datetime.strptime(request.GET.get('start_date'), "%b. %d, %Y")
    end_date = datetime.datetime.strptime(request.GET.get('end_date'), "%b. %d, %Y")
    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet('my_sheet')

    header = ['Stock', 'Unit measure', 'Quantity', 'Destination','Date']
    for hcol, hcol_data in enumerate(header):
        sheet.write(0, hcol, hcol_data)

    row = 0
    transfer = Transfer.objects.filter(date__range=[start_date, end_date]).order_by('stock__name','destination')
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
