from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect, HttpResponseRedirect
from gestion_clientes.models import Customer, Review
from gestion_restaurante.forms import ContactUsForm
from .forms import CustomerForm, UserForm, ReviewForm, UserUpdateForm
from django.db import transaction
from django.urls import reverse, reverse_lazy
from django.core.mail import send_mail
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

# Create your views here.

class HomePage(TemplateView):
    template_name = "base/index.html"

class CustomerListPage(LoginRequiredMixin, ListView):
    model  = Customer
    template_name = "clientes/index.html"
    queryset = Customer.objects.order_by("id")

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.has_perm('gestion_clientes.view_customer'):
            customers = Customer.objects.order_by('id')
            return render(request, 'clientes/index.html', {'object_list': customers})
        else:
            return HttpResponseRedirect(reverse_lazy('home') + "?unable")
    
class CustomerDetailsPage(LoginRequiredMixin, DetailView):
    model = Customer
    template_name = "clientes/details.html"
    context_object_name = "customer"

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.has_perm('gestion_clientes.view_customer'):
            customer = Customer.objects.get(id = kwargs['pk'])
            return render(request, 'clientes/details.html', {'customer': customer})
        else:
            return HttpResponseRedirect(reverse_lazy('home') + "?unable")

class CustomerDeletePage(LoginRequiredMixin, DeleteView):
    model = User
    context_object_name = "user"

    # @user_passes_test(lambda u: u.is_superuser)
    # self es la clase, request es la "ruta", args está vacío y kwargs contiene la PK del user vinculado al customer
    def get(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.has_perm('gestion_clientes.delete_customer'):
            user = User.objects.get(id = kwargs['pk'])
            # return HttpResponseRedirect(self.get_success_url())
            return render(request, 'auth/user_confirm_delete.html', {'object': user})
        else:
            return HttpResponseRedirect(reverse_lazy('home') + "?unable")
    
    def get_success_url(self):
        return reverse_lazy('customersIndex') + "?deleted"

@transaction.atomic
@login_required
# @user_passes_test(lambda u: u.is_superuser)
def create_user(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            user_form = UserForm(request.POST)
            customer_form = CustomerForm(request.POST, request.FILES)
            if user_form.is_valid() and customer_form.is_valid():
                user = user_form.save()
                user.refresh_from_db()
                customer_form = CustomerForm(request.POST, request.FILES, instance=user.customer)
                customer_form.full_clean()
                customer_form.save()
                return redirect(reverse('customersIndex') + '?created')
        else:
            user_form = UserForm()
            customer_form = CustomerForm()
        return render(request, 'clientes/create.html', {'user_form': user_form, 'customer_form': customer_form})
    else:
        return redirect(reverse_lazy('home') + '?unable')

@transaction.atomic
@login_required
# @user_passes_test(lambda u: u.is_superuser)
def update_user2(request, pk):
    if request.user.is_superuser:
        user = User.objects.get(id = pk)
        if request.method == 'POST':

            customer_form = CustomerForm(request.POST, request.FILES, instance=user.customer)
            user_form = UserUpdateForm(request.POST, instance=user)

            if customer_form.is_valid() and user_form.is_valid():
                user = user_form.save() 
                user.refresh_from_db()
                # customer_form = CustomerForm(customer_form.cleaned_data, request.FILES, instance=user.customer)
                # customer_form.full_clean()
                customer_form.save()
                return redirect(reverse('customersIndex') + '?updated')
        else:
            user_form = UserUpdateForm(instance=user)
            customer_form = CustomerForm(instance=user.customer)
            
        return render(request, 'clientes/update.html', {'customer_form': customer_form, 'user_form':user_form})
    else:
        return redirect(reverse_lazy('home') + '?unable')


class ReviewsListPage(ListView):
    model  = Review
    template_name = "reviews/index.html"
    queryset = Review.objects.all()
    context_object_name = "reviews"

class ReviewDetailsPage(DetailView):
    model = Review
    template_name = "reviews/details.html"
    context_object_name = "review"

class ReviewsCreatePage(LoginRequiredMixin, CreateView):
    model = Review
    template_name = "reviews/create.html"
    form_class = ReviewForm

    def get_success_url(self):
        return reverse('reviewsIndex') + "?created"

    def post(self, request):
        form = self.get_form()
        if form.is_valid():  
            form.save(request=self.request)
            return HttpResponseRedirect(self.get_success_url())

        return render(request, "reviews/update.html", {'form':form})

class ReviewUpdatePage(LoginRequiredMixin, UpdateView):
    model = Review
    template_name = "reviews/update.html"
    form_class = ReviewForm

    def get_success_url(self):
        return self.request.path + "?updated"


class ReviewDeletePage(LoginRequiredMixin, DeleteView):
    model = Review
    context_object_name = "review"
    template_name = "reviews/review_confirm_delete.html"
    
    def get_success_url(self):
        return reverse_lazy('reviewsIndex') + "?deleted"

def contactUs(request):
    if request.method == "POST":
        form = ContactUsForm(data = request.POST)
        if form.is_valid():
            sender = form.cleaned_data['sender']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            send_mail(subject, message, sender, ['felixreyesf@gmail.com',], fail_silently=False)
            return redirect(reverse('contact') + '?success')
    else:
        form = ContactUsForm()

    return render(request, "contact/contact.html", {"form": form})