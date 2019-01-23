from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from gestion_clientes.models import Customer, Review
from gestion_restaurante.forms import ContactUsForm
from .forms import CustomerForm, UserForm
from django.urls import reverse
from django.core.mail import send_mail
from django.views.generic import TemplateView, ListView, DetailView, CreateView
# from django.models import Page

# Create your views here.
# def index(request):
#     return render(request, "base/index.html")
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

    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get a context
    #     context = super().get_context_data(**kwargs)
    #     # Add in a QuerySet of all the books
    #     context['reviews_list'] = Review.objects.filter(author = self)
    #     return context

    # def get_queryset(self):
    #     self.reviews = get_list_or_404(Review, author=self.kwargs['publisher'])
    #     return Book.objects.filter(publisher=self.publisher)

class CustomerCreatePage(CreateView):
    model = Customer
    template_name = "clientes/create.html"
    fields = '__all__'

def create_user(request):
    if request.method == 'POST':
        customer_form = CustomerForm(request.POST, request.FILES)
        user_form = UserForm(request.POST)
        if customer_form.is_valid() and user_form.is_valid():
            customer_form.save()
            user_form.save()
            return redirect(reverse('home') + '?created')
        # else:
        #     messages.error(request, _('Please correct the error below.'))
    else:
        customer_form = CustomerForm()
        user_form = UserForm()
    return render(request, 'clientes/create.html', {'customer_form': customer_form, 'user_form':user_form})

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
            send_mail(subject, message, sender, ['carrascoperez90@gmail.com',], fail_silently=False)
            return redirect(reverse('contact') + '?success')
    else:
        form = ContactUsForm()

    return render(request, "contact/contact.html", {"form": form})