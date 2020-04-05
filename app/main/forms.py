from django import forms
from bookings.validators import *

class invoiceForm(forms.Form):
    from_date = forms.CharField( 
        widget=forms.TextInput(attrs={'placeholder': 'DD/MM/YYYY', 'required': 'required'}),
        validators=[date_validation],
        label='',
        required=True
    )

    to_date = forms.CharField( 
        widget=forms.TextInput(attrs={'placeholder': 'DD/MM/YYYY', 'required': 'required'}),
        validators=[date_validation],
        label='',
        required=True
    )