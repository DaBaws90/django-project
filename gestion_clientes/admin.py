from django.contrib import admin
from .models import Customer, Review
from django import forms
from .forms import CustomerForm, ReviewForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from gestion_restaurante.admin import OrderInline
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Register your models here.

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1
    can_delete = False

# Creamos una opción para el menú desplegables del panel de administración, en el que está la opcón de eliminar los
#  registros seleccionados
def reset_email_info(self, request, queryset):
    cont = queryset.update(email = None)
    if cont == 1:
        mssg = "1 email was"
    else:
        mssg = "{} emails were".format(cont)
    self.message_user(request, "{} successfully reseted.".format(mssg))
    reset_email_info.short_description = "Reset linked email information"

class CustomerInline(admin.StackedInline):
    model = Customer
    can_delete = False
    verbose_name_plural = "Cliente"

class UserAdmin(BaseUserAdmin):
    inlines = [CustomerInline,]

class CustomerAdmin(admin.ModelAdmin):
    form = CustomerForm
    actions = [reset_email_info]
    readonly_fields = ['slug']
    actions_on_bottom = True
    actions_on_top = False
    list_per_page = 5
    ordering = ['name', 'middlename', 'lastname', 'birthday']
    search_fields = ['name', 'middlename', 'lastname', 'birthday']
    list_filter = ['name', 'registered', 'updated', 'address', 'slug']
    list_display_links = ['name', 'middlename', 'lastname']
    list_editable = ['birthday']
    inlines = [ReviewInline, OrderInline]
    list_display = ['name', 'middlename', 'lastname', 'birthday']
    fieldsets = [
        ('Datos personales', {'fields': ['name', 'middlename', 'lastname', 'birthday', 'gender']}),
        ('Otros datos', {
            'classes': ('collapse',),
            'fields': ['address', 'image', 'slug']}),
    ]
    date_hierarchy = 'registered'
    empty_value_display = "No data assoc"
    list_max_show_all = 50
    # prepopulated_fields = {"slug": ('name', 'middlename', 'lastname')}

class ReviewAdmin(admin.ModelAdmin):
    form = ReviewForm
    fields = [('title', 'valoration', 'author'), 'content']
    actions_on_bottom = True
    actions_on_top = False
    list_per_page = 10
    search_fields = ['title', 'valoration']
    list_filter = ['title', 'valoration']
    list_display = ['title', 'valoration', 'author']
    list_max_show_all = 50


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.empty_value_display = '(None)'
