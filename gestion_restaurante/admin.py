from django.contrib import admin
from .models import Restaurant, Order, Place, Product
from django import forms

# Register your models here.

class PlaceInline(admin.TabularInline):
    model = Place
    extra = 1

# class RestaurantAdminForm(forms.ModelForm):
#     pass

class RestaurantAdmin(admin.ModelAdmin):
    # form = RestaurantAdminForm
    inlines = [PlaceInline,]

admin.site.register(Order)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Place)
admin.site.register(Product)
