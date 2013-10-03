from django import forms

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

class DonorForm(forms.Form):
    donor_name = forms.CharField(max_length=30)
    donor_address = forms.CharField(max_length=100)
    donor_contact_no = forms.IntegerField()
    donor_mailing = forms.BooleanField(required=False)
    donor_referral = forms.ChoiceField(choices=REFERRAL_TYPES)
    donate_date = forms.DateField()
    
class DonateForm(forms.Form):
    donate_quantity = forms.IntegerField()
    stock_description = forms.CharField()
    stock_unit_measure = forms.CharField(max_length=10)
    stock_unit_price = forms.DecimalField(max_digits=10, decimal_places=2)
    
    
