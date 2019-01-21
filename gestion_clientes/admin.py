from django.contrib import admin
from .models import Customer, Review
from django import forms
from .forms import CustomerForm, ReviewForm

# Register your models here.

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1

class CustomerAdmin(admin.ModelAdmin):
    form = CustomerForm
    # readonly_fields = ['registered', 'updated']
    actions_on_bottom = True
    actions_on_top = False
    list_per_page = 5
    ordering = ['name', 'middlename', 'lastname', 'birthday']
    search_fields = ['name', 'middlename', 'lastname', 'birthday']
    list_filter = ['name', 'registered', 'updated', 'address', 'email']
    list_display_links = ['name', 'middlename', 'lastname']
    list_editable = ['birthday' ,'email']
    inlines = [ReviewInline,]
    list_display = ['name', 'middlename', 'lastname', 'birthday', 'email']
    fieldsets = [
        ('Datos personales', {'fields': ['name', 'middlename', 'lastname', 'birthday', 'gender']}),
        ('Otros datos', {
            'classes': ('collapse',),
            'fields': ['address', 'email', 'image']}),
    ]
    date_hierarchy = 'registered'
    empty_value_display = "No data assoc"
    list_max_show_all = 50
    list_per_page = 20
    # prepopulated_fields = {"slug": ('name', 'middlename', 'lastname')}

class ReviewAdmin(admin.ModelAdmin):
    form = ReviewForm
    fields = [('title', 'valoration', 'author'), 'content']
    actions_on_bottom = True
    actions_on_top = False
    list_per_page = 5
    search_fields = ['title', 'valoration']
    list_filter = ['title', 'valoration']
    list_display = ['title', 'valoration', 'author']
    list_max_show_all = 50
    list_per_page = 20
    # formfield_overrides = {
    #     models.TextField: {'widget': RichTextEditorWidget},
    # }



admin.site.register(Customer, CustomerAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.empty_value_display = '(None)'
