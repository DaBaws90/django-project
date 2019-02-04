from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect, HttpResponseRedirect
from .models import Order, Product, Place, Restaurant
from .forms import OrderForm, ProductForm, PlaceForm, RestaurantForm
from django.db import transaction
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

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

class OrderCreatePage(LoginRequiredMixin, CreateView):
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
    model = Place
    template_name = "lugares/create.html"
    form_class = PlaceForm

    def get_success_url(self):
        return reverse_lazy('placesIndex') + "?created"

class PlaceUpdatePage(UpdateView):
    model = Place
    template_name = "lugares/update.html"
    form_class = PlaceForm

    def get_success_url(self):
        return self.request.path + '?updated'

class PlaceDeletePage(DeleteView):
    model = Place
    context_object_name = "place"
    template_name = "lugares/place_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy('placesIndex') + "?deleted"

class ProductListPage(ListView):
    model = Product
    template_name = "productos/index.html"
    queryset = Product.objects.all()

class ProductDetailsPage(DetailView):
    model = Product
    template_name = "productos/details.html"
    context_object_name = "product"

class ProductCreatePage(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "productos/create.html"

    def get_success_url(self):
        return reverse('productsIndex') + '?created'

class ProductUpdatePage(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "productos/update.html"

    def get_success_url(self):
        return self.request.path + '?updated'

class ProductDeletePage(DeleteView):
    model = Product
    template_name = "productos/product_confirm_delete.html"
    context_object_name = "product"

    def get_success_url(self):
        return reverse('productsIndex') + '?deleted'

class RestaurantListPage(ListView):
    model = Restaurant
    template_name = "restaurante/index.html"
    queryset = Restaurant.objects.all()

class RestaurantDetailsPage(DetailView):
    model = Restaurant
    template_name = "restaurante/details.html"
    context_object_name = "restaurant"

class RestaurantCreatePage(CreateView):
    model = Product
    form_class = RestaurantForm
    template_name = "restaurante/create.html"

    def get_success_url(self):
        return reverse('restaurantsIndex') + '?created'

class RestaurantUpdatePage(UpdateView):
    model = Restaurant
    form_class = RestaurantForm
    template_name = "restaurante/update.html"

    def get_success_url(self):
        return reverse('restaurantsIndex') + '?updated'

class RestaurantDeletePage(DeleteView):
    model = Restaurant
    template_name = "restaurante/restaurant_confirm_delete.html"
    context_object_name = "restaurant"

    def get_success_url(self):
        return reverse('restaurantsIndex') + '?deleted'

class About(TemplateView):
    template_name = "about/aboutUs.html"