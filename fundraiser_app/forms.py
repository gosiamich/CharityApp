from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.http import request

from fundraiser_app.models import Institution, Category, Donation


class AddDonationModelForm(forms.ModelForm):

    class Meta:
        model = Donation
        fields = ['quantity','categories', 'institution',\
        'address_street_no','city','phone_number','zip_code','pick_up_date','pick_up_time','pick_up_comment','user']
