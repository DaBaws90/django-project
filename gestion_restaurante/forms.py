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
        if self.cleaned_data['message'] is None or len(self.cleaned_data['message']) > 1000:
            raise forms.ValidationError('El campo debe tener 3 carácteres como mínimo y 1000 como máximo')
        else:
            return self.cleaned_data['message'].capitalize()

class RestaurantForm(forms.ModelForm):
    
    class Meta:
        model = Restaurant
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(
                attrs= {'class': 'form-group', 'placeholder': 'Escriba a1uí el nombre'}
            ),
            'capacity': forms.Textarea(
                attrs={'cols': 60, 'rows': 6, 'class': 'from-group', 'placeholder': '¿Cuántas personas caben?'}
            ),
        }
        help_texts = {
            'name': ('Nombre del establecimiento'),
            'place': ('Ubicación del local'),
            'capacity': ('Aforo máximo de las instalaciones')
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
            return self.cleaned_data['name'].capitalize()


class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = '__all__'

        widgets = {
            'comment': forms.Textarea(
                attrs={'cols': 60, 'rows': 6, 'class': 'from-group', 'placeholder': 'Escriba aquí su comentario'}
            ),
        }
        help_texts = {
            'comment': ('¿Algo que desee comentarnos acerca del pedido?'),
        }
        error_messages = {
            'comment': {
                'max_length': ("Parece que se ha extendido demasiado y ha rebasado la longitud máxima")
            }
        }

class PlaceForm(forms.ModelForm):
    
    class Meta:
        model = Place
        fields = '__all__'

        widgets = {
            'comment': forms.Textarea(
                attrs={'cols': 60, 'rows': 6, 'class': 'from-group', 'placeholder': 'Escriba aquí su comentario'}
            ),
        }
        help_texts = {
            'comment': ('¿Algo que desee comentarnos acerca del pedido?'),
        }
        error_messages = {
            'comment': {
                'max_length': ("Parece que se ha extendido demasiado y ha rebasado la longitud máxima")
            }
        }

class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = '__all__'

        widgets = {
            'comment': forms.Textarea(
                attrs={'cols': 60, 'rows': 6, 'class': 'from-group', 'placeholder': 'Escriba aquí su comentario'}
            ),
        }
        help_texts = {
            'comment': ('¿Algo que desee comentarnos acerca del pedido?'),
        }
        error_messages = {
            'comment': {
                'max_length': ("Parece que se ha extendido demasiado y ha rebasado la longitud máxima")
            }
        }

    product = forms.ModelChoiceField(label = "Producto", queryset = Product.objects.all(), empty_label= "Seleccione un producto")

    # Mirar cómo añadir cliente desde aquí
    customer = forms.ModelChoiceField(label = "Cliente", queryset = Customer.objects.all(), empty_label= "Seleccione un cliente")

    def clean_comment(self):
        if len(self.cleaned_data['comment'] > 150):
            raise forms.ValidationError("El campo no puede exceder los 150 carácteres de longitud")
        else:
            return self.cleaned_data['comment'].capitalize()


