from django.contrib import admin
from .models import Customer, Review
from django import forms

# Register your models here.

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1

class CustomerAdminForm(forms.ModelForm):
    def clean_name(self):
        if len(self.cleaned_data['name']) < 3 or len(self.cleaned_data['name']) > 30:
            raise forms.ValidationError('El campo debe tener 3 carácteres como mínimo y 30 como máximo')
        else:
            return self.cleaned_data['name'].capitalize()

    def clean_middlename(self):
        if len(self.cleaned_data['middlename']) < 3 or len(self.cleaned_data['name']) > 40:
            raise forms.ValidationError('El campo debe tener 3 carácteres como mínimo y 30 como máximo')
        else:
            return self.cleaned_data['middlename'].capitalize()

    def clean_lastname(self):
        if len(self.cleaned_data['lastname']) < 3 or len(self.cleaned_data['lastname']) > 40:
            raise forms.ValidationError('El campo debe tener 3 carácteres como mínimo y 30 como máximo')
        else:
            return self.cleaned_data['lastname'].capitalize()
    
    def clean_address(self):
        if len(self.cleaned_data['address']) < 5 or len(self.cleaned_data['address']) > 80:
            raise forms.ValidationError('El campo debe tener 5 carácteres como mínimo y 80 como máximo')
        else:
            return self.cleaned_data['address'].capitalize()

class CustomerAdmin(admin.ModelAdmin):
    form = CustomerAdminForm
    # fields = ['all']
    readonly_fields = ['registered', 'updated']
    actions_on_bottom = True
    actions_on_top = False
    list_per_page = 5
    ordering = ['name', 'middlename', 'lastname', 'birthday']
    list_filter = ['name', 'registered', 'updated', 'address']
    inlines = [ReviewInline,]
    list_display = ['name', 'middlename', 'lastname', 'birthday']
    fieldsets = [
        ('Datos personales', {'fields': ['name', 'middlename', 'lastname', 'birthday', 'gender']}),
        ('Otros datos', {'fields': ['address', 'image']}),
    ]


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Review)
