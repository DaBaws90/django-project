from django import forms
from django.core.validators import EmailValidator
from gestion_clientes.models import Customer
from .models import Product, Order, Place, Restaurant

class ContactUsForm(forms.Form):
    sender = forms.EmailField(label = "Email", validators=[EmailValidator], required = True, widget = forms.EmailInput(
        attrs = {'class':'form-group', 'placeholder':'Introduzca su email'}
    ))

    subject = forms.CharField(label = "Asunto", required = True, widget = forms.TextInput(
        attrs = {'class':'form-group', 'placeholder':'Introduzca el asunto'}
    ))

    message = forms.CharField(label = "Mensaje", required = True, widget = forms.Textarea(
        attrs = {'class':'form-group', 'placeholder':'Escriba su mensaje'}
    ))

    def clean_subject(self):
        if len(self.cleaned_data['subject']) < 3 or len(self.cleaned_data['subject']) > 25:
            raise forms.ValidationError('El campo debe tener 3 carácteres como mínimo y 25 como máximo')
        else:
            return self.cleaned_data['subject'].capitalize()

    def clean_message(self):
        if len(self.cleaned_data['message']) < 10 or len(self.cleaned_data['message']) > 1000:
            raise forms.ValidationError('El campo debe tener 10 carácteres como mínimo y 1000 como máximo')
        else:
            return self.cleaned_data['message'].capitalize()

class RestaurantForm(forms.ModelForm):
    
    class Meta:
        model = Restaurant
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(
                attrs= {'class': 'form-group', 'placeholder': 'Escriba aquí el nombre', 'required':True}
            ),
            'capacity': forms.Textarea(
                attrs={'cols': 60, 'rows': 6, 'class': 'from-group', 'placeholder': '¿Cuántas personas caben?', 'required':True}
            ),
            'built': forms.DateInput(
                attrs={'class': 'form-group', 'placeholder': 'Fecha de la que data el establecimiento', 'required':True}
            )
        }
        help_texts = {
            'name': ('Nombre del establecimiento'),
            'place': ('Ubicación del local'),
            'capacity': ('Aforo máximo de las instalaciones'),
            'built': ('Indique la fecha de construcción del local'),
        }
        error_messages = {
            'name': {
                'max_length': ("Ha excedido la longitud máxima para este campo"),
            },
        }

    place = forms.ModelChoiceField(label = "Ubicación", queryset = Place.objects.all(), empty_label= "Seleccione una ubicación")

    def clean_name(self):
        if len(self.cleaned_data['name']) > 35:
            raise forms.ValidationError("El campo no puede tener más de 35 carácteres")
        else:
            return self.cleaned_data['name']


class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = '__all__'

        widgets = {
            'description': forms.Textarea(
                attrs={'cols': 60, 'rows': 6, 'class': 'from-group', 'placeholder': 'Escriba aquí la descripción'}
            ),
        }
        help_texts = {
            'description': ('Breve descripción del producto. Máximo de 120 carácteres'),
            'name': ('Nombre del artículo. Obligatorio. Máximo de 30 carácteres')
        }

    def clean_description(self):
        if len(self.cleaned_data['description']) > 120:
            raise forms.ValidationError('El campo descripción no puede contener más de 120 carácteres')
        else:
            return self.cleaned_data['description']

    def clean_name(self):
        if len(self.cleaned_data['name']) > 30:
            raise forms.ValidationError('El campo nombre no puede contener más de 30 carácteres')
        else:
            return self.cleaned_data['name']


class PlaceForm(forms.ModelForm):
    
    class Meta:
        model = Place
        fields = '__all__'

        help_texts = {
            'address': ('Introduzca la dirección del lugar'),
            'city': ('¿En qué ciudad está?'),
            'country': ('País de la localización'),
            'zipCode': ('Introduzca el código postal')
        }

    def clean_address(self):
        if len(self.cleaned_data['address']) > 40:
            raise forms.ValidationError('El campo dirección no puede contener más de 40 carácteres')
        else:
            return self.cleaned_data['address']
    
    def clean_city(self):
        if len(self.cleaned_data['city']) > 30:
            raise forms.ValidationError('El campo ciudad no puede contener más de 30 carácteres')
        else:
            return self.cleaned_data['city']

    def clean_country(self):
        if len(self.cleaned_data['country']) > 30:
            raise forms.ValidationError('El campo país no puede contener más de 30 carácteres')
        else:
            return self.cleaned_data['country']


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        # fields = ['comment', 'stock', 'weigth', 'product']
        exclude = ['customer',]

        widgets = {
            'comment': forms.Textarea(
                attrs={'cols': 60, 'rows': 6, 'class': 'from-group', 'placeholder': 'Escriba aquí su comentario', 'required':True}
            ),
        }
        help_texts = {
            'comment': ('¿Algo que desee comentarnos acerca del pedido?'),
            'product': ('Indique el producto que contiene el pedido'),
            'weigth': ('Indique la cantidad deseada (Kgs). Debe indicar alguna de las dos cantidades'),
            'stock': ("Indique la cantidad deseada (Unidades). Debe indicar alguna de las dos cantidades"),

        }
        error_messages = {
            'comment': {
                'max_length': ("Parece que se ha extendido demasiado y ha rebasado la longitud máxima")
            }
        }

    product = forms.ModelChoiceField(label = "Producto", queryset = Product.objects.all(), empty_label= "Seleccione un producto")

    # customer = forms.ModelChoiceField(label = "Cliente", queryset = Customer.objects.all(), empty_label= "Seleccione un cliente")

    def clean_comment(self):
        if len(self.cleaned_data['comment']) > 150:
            raise forms.ValidationError("El campo no puede exceder los 150 carácteres de longitud")
        else:
            return self.cleaned_data['comment']

    def save(self, commit=True ,*args, **kwargs):
        request = None
        if 'request' in kwargs:
            request = kwargs.pop('request')
        obj = super().save(commit=False, *args, **kwargs)
        if obj.customer is None and request is not None:
            obj.customer = request.user.customer
        obj.save()

    # def save(self, commit=True ,*args, **kwargs):
    #     request = None
    #     if 'request' in kwargs:
    #         request = kwargs.pop('request')
    #     obj = super().save(commit=False, *args, **kwargs)
    #     if obj.customer is None and request is not None:
    #         print("CUSTOMER NONE: "+str(request.user.customer))
    #         temp = Customer.objects.filter(user = request.user)
    #         if temp.count() > 0:
    #             print("CUTOMER INSTANCE FOUND")
    #             obj.customer = temp
    #         else:
    #             obj.customer = None
    #     print("SAVING CUSTOMER")
    #     obj.save()


