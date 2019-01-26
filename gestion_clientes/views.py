from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from gestion_clientes.models import Customer, Review
from gestion_restaurante.forms import ContactUsForm
from .forms import CustomerForm, UserForm
from django.db import transaction
from django.urls import reverse, reverse_lazy
from django.core.mail import send_mail
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView
from django.contrib.auth.models import User

# Create your views here.

class HomePage(TemplateView):
    template_name = "base/index.html"

class CustomerListPage(ListView):
    model  = Customer
    template_name = "clientes/index.html"
    queryset = Customer.objects.all()

class CustomerDetailsPage(DetailView):
    model = Customer
    template_name = "clientes/details.html"
    context_object_name = "customer"

class CustomerDeletePage(DeleteView):
    model = User
    success_url = reverse_lazy('customersIndex')

# class CustomerCreatePage(CreateView):
#     model = Customer
#     # customer_form = CustomerForm()
#     # user_form = UserForm()
#     form_class = CustomerForm, UserForm
#     template_name = "clientes/create.html"
#     # fields = '__all__'


@transaction.atomic
def create_user(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        customer_form = CustomerForm(request.POST, request.FILES)
        if user_form.is_valid() and customer_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()
            customer_form = CustomerForm(request.POST, instance=user.customer)
            customer_form.full_clean()
            customer_form.save()
            return redirect(reverse('home') + '?created')
        # else:
        #     messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm()
        customer_form = CustomerForm()
    return render(request, 'clientes/create.html', {'user_form': user_form, 'customer_form': customer_form
})

@transaction.atomic
def update_user(request):
    if request.method == 'POST':
        customer_form = CustomerForm(request.POST, request.FILES, instance= request.user.customer)
        user_form = UserForm(request.POST, instance = request.user)
        if customer_form.is_valid() and user_form.is_valid():
            customer_form.save()
            user_form.save()
            return redirect(reverse('home') + '?updated')
        # else:
        #     messages.error(request, _('Please correct the error below.'))
    else:
        customer_form = CustomerForm(instance=request.user.customer)
        user_form = UserForm(instance=request.user)
    return render(request, 'clientes/update.html', {'customer_form': customer_form, 'user_form':user_form})

# def listCustomers(request):
#     customers = get_list_or_404(Customer.objects.order_by("name"))
#     context = {'customers': customers}
#     return render(request, "clientes/index.html", context)

# def customerDetails(request, customer_id):
#     customer = get_object_or_404(Customer, id = customer_id)
#     reviews = Review.objects.filter(author = customer) # Inyectamos la "relación" o lo recuperamos en el template 
#         # desde el objeto customer (for X in customer.review_set.all)
#     return render(request, "clientes/details.html", {'customer': customer, 'reviews': reviews}) # This is the context

def listReviews(request):
    reviews = get_list_or_404(Review.objects.order_by("valoration"))
    context = {'reviews': reviews}
    return render(request, "reviews/index.html", context)

def reviewDetails(request, review_id):
    # En una sola línea de código, aunque es menos legible (a veces menos es más, y viceversa)
    return render(request, "reviews/details.html", {'review': get_object_or_404(Review, id = review_id)})

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