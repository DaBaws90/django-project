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

# Create your views here.

class HomePage(TemplateView):
    template_name = "base/index.html"

class CustomerListPage(ListView):
    model  = Customer
    template_name = "clientes/index.html"
    queryset = Customer.objects.order_by("id")

class CustomerDetailsPage(DetailView):
    model = Customer
    template_name = "clientes/details.html"
    context_object_name = "customer"

class CustomerDeletePage(DeleteView):
    model = User
    context_object_name = "user"
    
    def get_success_url(self):
        return reverse_lazy('customersIndex') + "?deleted"

@transaction.atomic
def create_user(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        customer_form = CustomerForm(request.POST, request.FILES)
        if user_form.is_valid() and customer_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()
            customer_form = CustomerForm(request.POST, request.FILES, instance=user.customer)
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
def update_user2(request, pk):
    user = User.objects.get(id = pk)
    if request.method == 'POST':
        # Evaluamos si no ha cambiado el username
        # if request.POST['username'] == user.username:
        #     # Hay que hacer esto porque el objeto request.POST es inmutable
        #     post = request.POST.copy()
        #     post['username'] = "DUMMY"
        #     request.POST = post
        #     # Asignamos el antiguo username a variable porque al validar el formulario, se guarda el objeto user 
        #     # con el valor "DUMMY" y por tanto, necesitamos recuperarlo de alguna otra manera (con esta variable)
        #     oldUsername = user.username

        # if request.POST['username'] == "DUMMY":
        #     # Si el request['username] es igual a DUMMY, e que hubo error de validaión en el formulario del Customer.
        #     # Reseteamos manualmente el campo o de lo contrario, el formulario reflejará DUMMY en el campo username
        #     post = request.POST.copy()
        #     post['username'] = user.username
        #     request.POST = post

        customer_form = CustomerForm(request.POST, request.FILES, instance=user.customer)
        user_form = UserUpdateForm(request.POST, instance=user)

        if customer_form.is_valid() and user_form.is_valid():
            # if user_form.cleaned_data['username'] == "DUMMY":
                # Si el valor del username del form es DUMMY, es que no lo habíamos cambiado en el form, por lo que 
                # asignamos de nuevo el valor antiguo
                # user.username = oldUsername
                # user_form.cleaned_data['username'] = oldUsername

            # El objeto user lleva con él toda la información del customer, y lo guarda mediante el método que declaramos
            # en el modelo customer (el que intercepta la señal 'signal' con el decorador @receiver(post_save)) 
            user = user_form.save() 
            user.refresh_from_db()
            # customer_form = CustomerForm(customer_form.cleaned_data, request.FILES, instance=user.customer)
            # customer_form.full_clean()
            customer_form.save()
            return redirect(reverse('home') + '?updated')
            # Todo esto es necesario porque el form de UserCreationForm valida los usernames como únicos, por lo que
            # el formulario nos dice que el username ya está en uso (Con esto, pasamos por encima de esa validación)
        # else:
        #     messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserUpdateForm(instance=user)
        customer_form = CustomerForm(instance=user.customer)
        
    return render(request, 'clientes/update.html', {'customer_form': customer_form, 'user_form':user_form})



class ReviewsListPage(ListView):
    model  = Review
    template_name = "reviews/index.html"
    queryset = Review.objects.all()
    context_object_name = "reviews"

class ReviewDetailsPage(DetailView):
    model = Review
    template_name = "reviews/details.html"
    context_object_name = "review"

class ReviewsCreatePage(CreateView):
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

class ReviewUpdatePage(UpdateView):
    model = Review
    template_name = "reviews/update.html"
    form_class = ReviewForm

    def get_success_url(self):
        return self.request.path + "?updated"

class ReviewDeletePage(DeleteView):
    model = Review
    context_object_name = "review"
    
    def get_success_url(self):
        return reverse_lazy('reviewsIndex') + "?deleted"

    # Cuando esté implementado el login, habilitar esto y añadir exclude al form de Review, y comentar el atributo author en modelo
    

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