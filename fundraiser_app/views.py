from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View

from fundraiser_app.forms import AddDonationForm
from fundraiser_app.models import Donation, Institution, Category


class LandingPage(View):
    def get(self, request):
        quantity_all = sum([x.quantity for x in Donation.objects.all()])
        amounts_of_institution = len(set([x.institution for x in Donation.objects.all()]))
        foundations = Institution.objects.filter(type='Fundacja')
        # paginator = Paginator(foundations_list, 5)
        # page = request.GET.get('page')
        # foundations = paginator.get_page(page)
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
        form = AddDonationForm(data)
        breakpoint()
        instit = data.get('institution_id', False)
        input_id = int(instit)
        institution = Institution.objects.get(id=input_id)

        donation = Donation.objects.create(user=request.user,
                                           quantity=data.get('quantity', False),
                                           institution=institution,
                                           address_street_no=data.get('address_street_no', False),
                                           city=data.get('city', False),
                                           zip_code=data.get('zip_code', False),
                                           phone_number=data.get('phone_number', False),
                                           pick_up_date=data.get('pick_up_date'),
                                           pick_up_time=data.get('pick_up_time'),
                                           pick_up_comment=data.get('pick_up_comment', False),
                                           )
        for object in [x for x in data.get('categories', False).replace(',','')]:
            donation.categories.add(Category.objects.get(id=int(object)))
        donation.save()
        return JsonResponse({'url': reverse('form_confirmation')})

        # data = request.POST.dict()
        # form = AddDonationForm(data)
        # breakpoint()
        # if form.is_valid():
        #     # validate and save
        #     donation = Donation.objects.create(user=request.user,
        #                                        quantity=form['quantity', False],
        #                                        institution= Institution.objects.get(id=form['institution_id', False]),
        #                                        address_street_no=form['address_street_no', False],
        #                                        city=form['city', False],
        #                                        zip_code=form['zip_code', False],
        #                                        phone_number=form['phone_number', False],
        #                                        pick_up_date=form['pick_up_date'],
        #                                        pick_up_time=form['pick_up_time'],
        #                                        pick_up_comment=form['pick_up_comment', False],
        #                                        )
        #     for category in form['categories', False]:
        #         donation.categories.add(Category.objects.get(id=int(category)))
        #         donation.save()
        #     return JsonResponse({'url': reverse('form_confirmation')})
        # else:
        #     categories = Category.objects.all()
        #     organizations = Institution.objects.all()
        #     return render(request, "fundraiser_app/form.html", {'categories': categories, 'organizations': organizations})


class FormConfirmation(View):
    def get(self, request):
        return render(request, "fundraiser_app/form-confirmation.html")
