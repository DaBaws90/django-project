from django.shortcuts import render, redirect
from gestion_clientes.models import Customer, Review
from gestion_clientes.forms import CustomerForm, UserForm, UserUpdateForm
from django.db import transaction
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView

# Create your views here.
class SignIn(LoginView):
    form_class = AuthenticationForm
    template_name = "registration/login.html"

    def get_success_url(self):
        return reverse_lazy("profile") + "?signin"

@transaction.atomic
def signup(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        customer_form = CustomerForm(request.POST, request.FILES)
        if user_form.is_valid() and customer_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()
            customer_form = CustomerForm(request.POST, request.FILES, instance=user.customer)
            customer_form.full_clean()
            customer_form.save()
            return redirect(reverse('home') + '?signup')
    else:
        user_form = UserForm()
        customer_form = CustomerForm()
    return render(request, 'registration/signup.html', {'user_form': user_form, 'customer_form': customer_form
})

@transaction.atomic
def profile_update(request):
    if request.user.is_staff:
        return redirect('/admin/')

    if request.method == 'POST':
        customer_form = CustomerForm(request.POST, request.FILES, instance=request.user.customer)
        user_form = UserUpdateForm(request.POST, instance=request.user)

        if customer_form.is_valid() and user_form.is_valid():
            user_form.save()
            return redirect(reverse('profile') + '?updated')
    else:
        user_form = UserUpdateForm(instance=request.user)
        customer_form = CustomerForm(instance=request.user.customer)
        
    return render(request, 'registration/profile_update.html', {'customer_form': customer_form, 'user_form':user_form})