from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect, HttpResponseRedirect
# from gestion_clientes.models import Customer, Review
from .models import Order, Product, Place, Restaurant
from .forms import OrderForm, ProductForm, PlaceForm, RestaurantForm
# from .forms import ContactUsForm
# from gestion_clientes.forms import CustomerForm, UserForm, ReviewForm, UserUpdateForm
from django.db import transaction
from django.urls import reverse, reverse_lazy
# from django.core.mail import send_mail
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserChangeForm

# Create your views here.

class HomeRestaurantPage(TemplateView):
    template_name = "restaurante/home.html"

class OrdersListPage(ListView):
    model = Order
    template_name = "pedidos/index.html"
    queryset = Order.objects.order_by("id")

class OrderDetailsPage(DetailView):
    model = Order
    template_name = "pedidos/details.html"
    context_object_name = "order"

class OrderCreatePage(CreateView):
    model = Order
    template_name = "pedidos/create.html"
    form_class = OrderForm

    def get_success_url(self):
        return reverse_lazy('ordersIndex') + "?created"

    def post(self, request):
        form = self.get_form()
        if form.is_valid():  
            form.save(request=self.request)
            return HttpResponseRedirect(self.get_success_url())
        
        return render(request, "pedidos/create.html", {'form': form})

class OrderUpdatePage(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = "pedidos/update.html"

    def get_success_url(self):
        return self.request.path + "?updated"


class OrderDeletaPage(DeleteView):
    model = Order
    context_object_name = "order"
    template_name = "pedidos/order_confirm_delete.html"
    
    def get_success_url(self):
        return reverse_lazy('ordersIndex') + "?deleted"


class PlaceListPage(ListView):
    model = Place
    template_name = "lugares/index.html"
    queryset = Place.objects.all()

class PlaceDetailsPage(DetailView):
    model = Place
    template_name = "lugares/details.html"
    context_object_name = "place"

class PlaceCreatePage(CreateView):
    model = Order
    template_name = "lugares/create.html"
    form_class = PlaceForm

    def get_success_url(self):
        return reverse_lazy('placesIndex') + "?created"