from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect, HttpResponseRedirect
from .models import Order, Product, Place, Restaurant
from .forms import OrderForm, ProductForm, PlaceForm, RestaurantForm
from django.db import transaction
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.models import User
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class HomeRestaurantPage(TemplateView):
    template_name = "restaurante/home.html"

class OrdersListPage(LoginRequiredMixin, ListView):
    model = Order
    template_name = "pedidos/index.html"
    queryset = Order.objects.order_by("id")

class OrderDetailsPage(LoginRequiredMixin, DetailView):
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

class OrderUpdatePage(LoginRequiredMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = "pedidos/update.html"

    def get_success_url(self):
        return self.request.path + "?updated"


class OrderDeletaPage(LoginRequiredMixin, DeleteView):
    model = Order
    context_object_name = "order"
    template_name = "pedidos/order_confirm_delete.html"
    
    def get_success_url(self):
        return reverse_lazy('ordersIndex') + "?deleted"


class PlaceListPage(ListView):
    model = Place
    template_name = "lugares/index.html"
    queryset = Place.objects.order_by('id')

class PlaceDetailsPage(DetailView):
    model = Place
    template_name = "lugares/details.html"
    context_object_name = "place"

class PlaceCreatePage(LoginRequiredMixin, CreateView):
    model = Place
    template_name = "lugares/create.html"
    form_class = PlaceForm

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.has_perm('gestion_restaurante.add_place'):
            form = PlaceForm()
            return render(request, 'lugares/create.html', {'form': form})
        else:
            return redirect(reverse('home') + '?unable')

    def get_success_url(self):
        return reverse_lazy('placesIndex') + "?created"

class PlaceUpdatePage(LoginRequiredMixin, UpdateView):
    model = Place
    template_name = "lugares/update.html"
    form_class = PlaceForm

    def get(self, request, *args, **kwargs):
        place = Place.objects.get(id = kwargs['pk'])
        if request.user.is_superuser or request.user.has_perm('gestion_restaurante.change_place'):
            form = PlaceForm(instance=place)
            return render(request, 'lugares/update.html', {'form': form})
        else:
            return redirect(reverse('home') + '?unable')

    def get_success_url(self):
        return self.request.path + '?updated'

class PlaceDeletePage(LoginRequiredMixin, DeleteView):
    model = Place
    context_object_name = "place"
    template_name = "lugares/place_confirm_delete.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.has_perm('gestion_restaurante.delete_place'):
            place = Place.objects.get(id = kwargs['pk'])
            return render(request, 'lugares/place_confirm_delete.html', {'place': place})
        else:
            return HttpResponseRedirect(reverse_lazy('home') + "?unable")

    def get_success_url(self):
        return reverse_lazy('placesIndex') + "?deleted"

class ProductListPage(ListView):
    model = Product
    template_name = "productos/index.html"
    queryset = Product.objects.order_by('id')

class ProductDetailsPage(DetailView):
    model = Product
    template_name = "productos/details.html"
    context_object_name = "product"

class ProductCreatePage(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "productos/create.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.has_perm('gestion_restaurante.add_product'):
            form = ProductForm()
            return render(request, 'productos/create.html', {'form': form})
        else:
            return redirect(reverse('home') + '?unable')

    def get_success_url(self):
        return reverse('productsIndex') + '?created'

class ProductUpdatePage(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "productos/update.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.has_perm('gestion_restaurante.change_product'):
            product = Product.objects.get(id = kwargs['pk'])
            form = ProductForm(instance=product)
            return render(request, 'productos/update.html', {'form': form})
        else:
            return HttpResponseRedirect(reverse_lazy('home') + "?unable")

    def get_success_url(self):
        return self.request.path + '?updated'

class ProductDeletePage(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "productos/product_confirm_delete.html"
    context_object_name = "product"

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.has_perm('gestion_restaurante.delete_product'):
            product = Product.objects.get(id = kwargs['pk'])
            return render(request, 'productos/product_confirm_delete.html', {'product': product})
        else:
            return HttpResponseRedirect(reverse_lazy('home') + "?unable")

    def get_success_url(self):
        return reverse('productsIndex') + '?deleted'

class RestaurantListPage(ListView):
    model = Restaurant
    template_name = "restaurante/index.html"
    queryset = Restaurant.objects.order_by('place_id')

class RestaurantDetailsPage(DetailView):
    model = Restaurant
    template_name = "restaurante/details.html"
    context_object_name = "restaurant"

class RestaurantCreatePage(LoginRequiredMixin, CreateView):
    model = Product
    form_class = RestaurantForm
    template_name = "restaurante/create.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.has_perm('gestion_restaurante.add_restaurant'):
            form = RestaurantForm()
            return render(request, 'restaurante/create.html', {'form': form})
        else:
            return redirect(reverse('home') + '?unable')

    def get_success_url(self):
        return reverse('restaurantsIndex') + '?created'

class RestaurantUpdatePage(LoginRequiredMixin, UpdateView):
    model = Restaurant
    form_class = RestaurantForm
    template_name = "restaurante/update.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.has_perm('gestion_restaurante.change_restaurant'):
            restaurant = Restaurant.objects.get(pk = kwargs['pk'])
            form = RestaurantForm(instance=restaurant)
            return render(request, 'restaurante/update.html', {'form': form})
        else:
            return HttpResponseRedirect(reverse_lazy('home') + "?unable")

    def get_success_url(self):
        return reverse('restaurantsIndex') + '?updated'

class RestaurantDeletePage(LoginRequiredMixin, DeleteView):
    model = Restaurant
    template_name = "restaurante/restaurant_confirm_delete.html"
    context_object_name = "restaurant"

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.has_perm('gestion_restaurante.delete_restaurant'):
            restaurant = Restaurant.objects.get(pk = kwargs['pk'])
            return render(request, 'restaurante/restaurant_confirm_delete.html', {'restaurant': restaurant})
        else:
            return HttpResponseRedirect(reverse_lazy('home') + "?unable")

    def get_success_url(self):
        return reverse('restaurantsIndex') + '?deleted'

class About(TemplateView):
    template_name = "about/aboutUs.html"