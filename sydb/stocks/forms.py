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
        
class DateForm(forms.Form):
    date = forms.DateField()

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
        
class StockInForm(forms.Form):
    stock_name = forms.CharField()
    quantity = forms.IntegerField()
    unit_measure = forms.CharField(max_length=10)
    unit_price = forms.DecimalField(max_digits=10, decimal_places=2)

