from django import forms
from stocks.models import *

class DonorForm(forms.ModelForm):
    class Meta:
        model = Donor

class DateForm(forms.Form):
    date = forms.DateField()
        
class DonateForm(forms.Form):
    stock_name = forms.CharField()
    quantity = forms.IntegerField()
    unit_measure = forms.CharField(max_length=10)
    unit_price = forms.DecimalField(max_digits=10, decimal_places=2)
    # date = forms.DateField()


    

