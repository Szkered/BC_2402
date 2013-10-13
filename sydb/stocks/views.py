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
    else:
    
        if(request.method == 'POST'):    # When the form has been submitted
            donor_form = DonorForm(request.POST)
            donate_formset = DonateFormSet(request.POST)
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
            donate_formset = DonateFormSet()
        context = RequestContext(request, {'donor_form': donor_form,
                                           'date_form': date_form,
                                           'donate_formset': donate_formset})
        template = loader.get_template('donation.html')
        data = template.render(context)
        mimetype = "text/html; charset=utf-8"
    return HttpResponse(data, mimetype)
                  

def donor(request):
    categorys = Category.objects.all()
    cate_list = {categorys[0].name: categorys[0].stock.name}
    return render(request, 'donor.html',
                  RequestContext(request, {'cate_list': cate_list}))


