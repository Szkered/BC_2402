from django import forms
from stocks.models import *
from django.forms.models import modelformset_factory, inlineformset_factory, BaseInlineFormSet
from django.forms.formsets import formset_factory, BaseFormSet
import re

class DonorForm(forms.ModelForm):
    class Meta:
        model = Donor
        
class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        
class ConfirmForm(forms.Form):
    confirm = forms.BooleanField()

class StockInForm(forms.Form):
    stock_name = forms.CharField()
    unit_price = forms.FloatField()
    unit_measure = forms.CharField(max_length=10)
    category = forms.CharField(required=False)
    quantity = forms.IntegerField()

    def clean(self):
        cleaned_data = super(StockInForm, self).clean()
        quantity = cleaned_data.get('quantity')
        unit_price = cleaned_data.get('unit_price')
        unit_measure = cleaned_data.get('unit_measure')
        category_list = re.split(', | |,',cleaned_data.get('category'))
        
        if quantity:
            if not quantity > 0:
                raise forms.ValidationError("Quantity must be positive integer!")

        if not unit_price > 0:
            raise forms.ValidationError("Unit price must be positive integer!")

        if not re.compile("\d+\w+").search(unit_measure):
            raise forms.ValidationError(
                "Unit measure must be the combination of number and characters!")

        if category_list:
            if 'Standard' not in category_list and 'Non-Standard' not in category_list:
                raise forms.ValidationError("An item must be either Standard or Non-Standard!")
            
        return cleaned_data


class DateForm(forms.Form):
    date = forms.DateField()

class StartEndDateForm(forms.Form):
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)
    
class FamilyForm(forms.Form):
    TYPE_A = 'A'
    TYPE_B = 'B'
    TYPE_C = 'C'
    TYPE_D = 'D'
    ALL = 'L'
    FAMILY_TYPES = (
        (TYPE_A, 'Type A'),
        (TYPE_B, 'Type B'),
        (TYPE_C, 'Type C'),
        (TYPE_D, 'Type D'),
        (ALL, 'All')
    )
    family_type = forms.ChoiceField(choices=FAMILY_TYPES)
    
class DistributionForm(forms.Form):
    quantity = forms.IntegerField(initial=0)
    stock_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    def clean(self):
        cleaned_data = super(DistributionForm, self).clean()
        quantity = cleaned_data.get('quantity')
        stock = Stock.objects.get(pk=cleaned_data.get('stock_id'))
        
        if quantity > stock.current_amt():
            raise forms.ValidationError("You don't have that much %s!" % stock.name)

        if quantity < 0:
            raise forms.ValidationError("Quantity must be positive integer!")
            
        return cleaned_data


class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
    
class TransferForm(forms.Form):
    stock_name = forms.CharField()
    unit_measure = forms.CharField()
    quantity = forms.IntegerField()
    remark = forms.CharField(required=False)

    def clean(self):
        cleaned_data = super(TransferForm, self).clean()
        quantity = cleaned_data.get('quantity')
        stock = Stock.objects.get(
            name=cleaned_data.get('stock_name'),
            unit_measure=cleaned_data.get('unit_measure')
        )
        
        if quantity > stock.current_amt():
            raise forms.ValidationError("You don't have that much %s!" % stock.name)

        if quantity < 0:
            raise forms.ValidationError("Quantity must be positive integer!")
            
        return cleaned_data

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        
class CategoryForm(forms.Form):
    category = forms.CharField()

    
class AdjustForm(forms.Form):
    stock_name = forms.CharField()
    unit_measure = forms.CharField()
    current_amount = forms.IntegerField()


# This class is used to require forms in the formset not to be empty
class RequiredFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super(RequiredFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False # self.forms[0].empty_permitted = False

StockInFormSet = formset_factory(StockInForm, max_num=30, formset=RequiredFormSet)

OrderFormSet = modelformset_factory(Order, extra=0)

DonationFormSet = modelformset_factory(Donation, extra=0)

DonateFormSet = modelformset_factory(Donate, extra=0)

PurchaseFormSet = modelformset_factory(Purchase, exclude=['order'] ,extra=0)

DistributeFormSet = modelformset_factory(Distribute, extra=0)

VendorFormSet = modelformset_factory(Vendor, extra=0)

DonorFormSet = modelformset_factory(Donor, extra=0)

StockFormSet = modelformset_factory(Stock, exclude='is_donated',extra=0)
