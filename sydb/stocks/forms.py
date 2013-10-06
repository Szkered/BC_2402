from django import forms
from stocks.models import *

class DonorForm(forms.Form):
    FM = 'F'
    CLIENT = 'C'
    VOLUNTEER = 'V'
    REGULAR = 'R'
    OTHERS = 'O'
    REFERRAL_TYPES = (
        (FM, 'FM 97.2'),
        (CLIENT, 'SYCC Client'),
        (VOLUNTEER, 'SYCC Volunteer'),
        (REGULAR, 'Regular Donor'),
        (OTHERS, 'Others'),
    )
    name = forms.CharField(max_length=30)
    address = forms.CharField(max_length=100)
    contact_no = forms.IntegerField()
    mailing = forms.BooleanField(required=False)
    referral = forms.ChoiceField(choices=REFERRAL_TYPES)

# class DonorForm(forms.ModelForm):
#     class Meta:
#         model = Donor
    
class DonateForm(forms.Form):
    date = forms.DateField()
    quantity = forms.IntegerField()
    stock_name = forms.CharField()
    unit_measure = forms.CharField(max_length=10)
    unit_price = forms.DecimalField(max_digits=10, decimal_places=2)
    

    
