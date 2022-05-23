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

#
# class AddDonationForm(forms.Form):
#     quantity = forms.IntegerField()
#     institution = forms.ModelChoiceField(queryset=Institution.objects.all())
#     address_street_no = forms.CharField(max_length=150)
#     city = forms.CharField(max_length=64)
#     zip_code = forms.CharField(max_length=7)
#     phone_number = forms.CharField(max_length=50)
#     pick_up_date = forms.DateField()
#     pick_up_time = forms.TimeField()
#     categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all())
#     pick_up_comment = forms.CharField(required=False)
