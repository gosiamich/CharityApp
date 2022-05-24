from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View

from fundraiser_app.forms import AddDonationModelForm
from fundraiser_app.models import Donation, Institution, Category


class LandingPage(View):
    def get(self, request):
        quantity_all = sum([x.quantity for x in Donation.objects.all()])
        amounts_of_institution = len(set([x.institution for x in Donation.objects.all()]))
        foundations = Institution.objects.filter(type='Fundacja')
        orgs_non_governmentals = Institution.objects.filter(type='Organizacja pozarządowa')
        local_collections = Institution.objects.filter(type='Zbiórka lokalna')
        return render(request, "fundraiser_app/index.html", \
                      {'quantity_all': quantity_all, \
                       'amounts_of_institution': amounts_of_institution, \
                       'foundations': foundations, \
                       'local_collections': local_collections, \
                       'orgs_non_governmentals': orgs_non_governmentals}
                      )


class AddDonationView(LoginRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.all()
        organizations = Institution.objects.all()
        return render(request, "fundraiser_app/form.html", {'categories': categories, 'organizations': organizations})

    def post(self, request):
        data = request.POST
        form = AddDonationModelForm(data)
        # breakpoint()
        if form.is_valid():
            donation = form.save(commit=False)
            donation.user =request.user
            donation.save()
            return JsonResponse({'url': reverse('form_confirmation')})
        else:
            categories = Category.objects.all()
            organizations = Institution.objects.all()
            return render(request, "fundraiser_app/form.html",
                          {'categories': categories, 'organizations': organizations})


class FormConfirmation(View):
    def get(self, request):
        return render(request, "fundraiser_app/form-confirmation.html")
