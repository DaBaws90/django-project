from django.contrib import admin
from .models import Restaurant, Order, Place, Product
from django import forms
from .forms import OrderForm, PlaceForm, ProductForm, RestaurantForm

# Register your models here.

class RestaurantAdmin(admin.ModelAdmin):
    form = RestaurantForm
    actions_on_bottom = True
    actions_on_top = False
    list_per_page = 5
    list_max_show_all = 20
    fields = ['name', ('built', 'capacity')]
    search_fields = ['name', 'built', 'capacity', 'place']
    list_filter = ['name', 'built', 'capacity', 'place']
    list_display_links = ['name', 'built', 'capacity']
    list_display = ['name', 'built', 'capacity', 'place']
    date_hierarchy = 'built'

class PlaceAdmin(admin.ModelAdmin):
    form = PlaceForm
    actions_on_bottom = True
    actions_on_top = False
    list_per_page = 5
    list_max_show_all = 20
    fields = ['address', ('city', 'country', 'zipCode')]
    search_fields = ['address', 'city', 'country', 'zipCode']
    list_filter = ['address', 'city', 'country', 'zipCode']
    list_display_links = ['address', 'city', 'country', 'zipCode']
    list_display = ['address', 'city', 'country', 'zipCode']

class OrderInline(admin.TabularInline):
    model = Order
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    form = OrderForm
    actions_on_bottom = True
    actions_on_top = False
    list_per_page = 5
    list_max_show_all = 50
    fields = [('product', 'customer'), 'comment']
    search_fields = ['product', 'customer', 'date', 'comment']
    list_filter = ['product', 'customer', 'date']
    list_display_links = ['product', 'customer', 'date']
    list_display = ['product', 'customer', 'date']
    date_hierarchy = 'date'

class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    actions_on_bottom = True
    actions_on_top = False
    list_max_show_all = 50
    list_per_page = 10
    inlines = [OrderInline,]
    fields = ['name', ('stock', 'weigth')]
    search_fields = ['name', 'stock', 'weigth', 'created', 'updated']
    list_filter = ['name', 'stock', 'weigth', 'created', 'updated']
    list_display_links = ['name', 'stock', 'weigth']
    list_display = ['name', 'stock', 'weigth', 'created', 'updated']
    date_hierarchy = 'created'


admin.site.register(Order, OrderAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.empty_value_display = '(None)'