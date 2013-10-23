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
    FAMILY_TYPES = (
        (TYPE_A, 'Type A'),
        (TYPE_B, 'Type B'),
        (TYPE_C, 'Type C'),
        (TYPE_D, 'Type D'),
    )
    family_type = forms.ChoiceField(choices=FAMILY_TYPES)
    
class DistributionForm(forms.Form):
    quantity = forms.IntegerField()

class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
    
class TransferForm(forms.Form):
    stock_name = forms.CharField()
    unit_measure = forms.CharField()
    quantity = forms.IntegerField()
    # remark = forms.CharField()

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        
class CategoryForm(forms.Form):
    category = forms.CharField()
