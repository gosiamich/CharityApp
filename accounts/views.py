from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import View


from accounts.forms import CreateUserForm, LoginForm, UpdateUserForm, ChangePassword, Pass, SignUpForm
from accounts.models import User
from fundraiser_app.models import Donation


class RegisterView(View):
    def get(self, request):
        form = CreateUserForm()
        return render(request, 'fundraiser_app/register.html')

    def post(self, request):
        form = CreateUserForm(request.POST)
        # breakpoint()
        if form.is_valid():
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user = User.objects.create(email=email, first_name=first_name, last_name=last_name)
            user.set_password(password)
            user.save()
            return redirect('login')
        else:
            return render(request, 'fundraiser_app/register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'fundraiser_app/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('landing_page')
            else:
                if len(User.objects.filter(email=email)) > 0:
                    return render(request, 'fundraiser_app/login.html',
                                  {'form': form, 'message': 'Wprowadź poprawne hasło'})
                else:
                    return redirect('register')
        else:
            return render(request, 'fundraiser_app/login.html', {'form': form})


class LogOutView(View):
    def get(self, request):
        logout(request)
        return redirect('landing_page')


class UserProfileView(View):
    def get(self, request):
        donations = Donation.objects.filter(user_id=self.request.user.id).order_by('-is_taken')
        return render(request, "fundraiser_app/user_profile.html", {'donations': donations})

    def post(self, request):
        donation_id = request.POST.get('donation_id')
        object = Donation.objects.get(id=donation_id)
        object.is_taken = True
        object.save()
        donations = Donation.objects.filter(user_id=self.request.user.id).order_by('-is_taken')
        return render(request, "fundraiser_app/user_profile.html", {'donations': donations})


class UpdateUserView(View):
    def get(self, request):
        user = User.objects.get(pk=request.user.id)
        form = UpdateUserForm(initial={"first_name": request.user.first_name, "last_name": request.user.last_name})
        return render(request, 'fundraiser_app/update_user.html',
                      {'form': form, 'message': 'Formularz zmiany danych:'})

    def post(self, request):
        form = UpdateUserForm(request.POST)
        if form.is_valid():
            password = request.POST.get('password')
            user = authenticate(email=request.user.email, password=password)
            if user is None:
                form.add_error('password', 'Podano błędne aktualne hasło')
                return render(request, 'fundraiser_app/update_user.html',
                              {'form': form, 'message': 'Formularz zmiany danych:'})
            else:
                user.first_name = form.cleaned_data["first_name"]
                user.last_name = form.cleaned_data["last_name"]
                user.save()
                return redirect(reverse('user_profile'))
        return render(request, 'fundraiser_app/update_user.html', {'form': form, 'message': 'Formularz zmiany danych:'})


class ChangePasswordView(View):
    def get(self, request):
        form = ChangePassword()
        return render(request, 'fundraiser_app/change_password.html',
                      {'form': form, 'message': 'Formularz zmiany hasła'})

    def post(self, request):
        u = User.objects.get(pk=request.user.id)
        form = ChangePassword(request.POST)
        if form.is_valid():
            old_password = request.POST.get('old_password')
            user = authenticate(email=request.user.email, password=old_password)
            if user is None:
                form.add_error('old_password', 'Podano błędne aktualne hasło')
                return render(request, 'fundraiser_app/change_password.html',
                              {'form': form, 'message': 'Formularz zmiany hasła:'})
            else:
                new_password = request.POST.get('new_password')
                u.set_password(new_password)
                u.save()
                return redirect(reverse('user_profile'))
        return render(request, 'fundraiser_app/change_password.html',
                      {'form': form, 'message': 'Formularz zmiany hasła'})


class Password(PasswordChangeView):
    form_class = Pass
    success_url = reverse_lazy('landing_page')


class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'fundraiser_app/signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        # breakpoint()
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return redirect("login")
        return render(request, 'fundraiser_app/signup.html', {'form': form})





