from django.contrib import admin
from .models import Restaurant, Order, Place, Product
from django import forms
from .forms import OrderForm, PlaceForm, ProductForm, RestaurantForm

# Register your models here.

class RestaurantAdmin(admin.ModelAdmin):
    pass
    # form = RestaurantAdminForm
    # inlines = [PlaceInline,]

class PlaceAdmin(admin.ModelAdmin):
    pass

class ProductAdmin(admin.ModelAdmin):
    pass

class OrderAdmin(admin.ModelAdmin):
    pass

admin.site.register(Order, OrderAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.empty_value_display = '(None)'
