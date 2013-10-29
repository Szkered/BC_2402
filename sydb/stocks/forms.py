from django import forms
from stocks.models import *

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
    unit_price = forms.DecimalField(max_digits=10, decimal_places=2)
    unit_measure = forms.CharField(max_length=10)
    category = forms.CharField()
    quantity = forms.IntegerField()

    def clean(self):
        cleaned_data = super(StockInForm, self).clean()
        quantity = cleaned_data.get('quantity')
        
        if quantity:
            if not quantity > 0:
                raise forms.ValidationError("Quantity must be positive integer!")

        return cleaned_data


class DateForm(forms.Form):
    date = forms.DateField()

class StartEndDateForm(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()
    
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
            
        return cleaned_data


class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
    
class TransferForm(forms.Form):
    stock_name = forms.CharField()
    unit_measure = forms.CharField()
    quantity = forms.IntegerField()
    # remark = forms.CharField()

    def clean(self):
        cleaned_data = super(TransferForm, self).clean()
        quantity = cleaned_data.get('quantity')
        stock = Stock.objects.get(
            name=cleaned_data.get('stock_name'),
            unit_measure=cleaned_data.get('unit_measure')
        )
        if quantity > stock.current_amt():
            raise forms.ValidationError("You don't have that much %s!" % stock.name)
            
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
