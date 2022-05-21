from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.http import request

from fundraiser_app.models import Institution, Category


class AddDonationForm(forms.Form):
    quantity = forms.CharField(max_length=150)
    institution_id = forms.CharField(max_length=150)
    address_street_no = forms.CharField(max_length=150)
    city = forms.CharField(max_length=64)
    zip_code = forms.CharField(max_length=7)
    phone_number = forms.CharField(max_length=50)
    pick_up_date = forms.DateField()
    pick_up_time = forms.TimeField()
    categories = forms.CharField(max_length=64, required=False)
    pick_up_comment = forms.CharField(required=False)

    # def clean(self):
    #     data = super().clean()
    #     errors = []
    #     if data['password'] != data['password2']:
    #         errors.append('Podaj dwukrotnie takie samo hasło!')
    #         raise forms.ValidationError(errors)
    #     else:
    #         return data

# from django import forms
# from splitjson.widgets import SplitJSONWidget
#
# from fundraiser_app.models import Donation
#
#
# class AddDonationForm(forms.Form):
#
#     class Meta:
#         model= Donation
#         fields = '__all__'