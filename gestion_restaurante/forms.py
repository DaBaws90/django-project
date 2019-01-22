from django import forms
from django.core.validators import EmailValidator
from gestion_clientes.models import Customer
from .models import Product, Order, Place, Restaurant

class ContactUs(forms.Form):
    sender = forms.EmailField(label = "Email", validators=[EmailValidator], required = True, widget = forms.EmailInput(
        attrs = {'class':'form-group', 'placeholder':'Introduzca su email'}
    ))

    subject = forms.CharField(label = "Asunto", required = True, widget = forms.TextInput(
        attrs = {'class':'form-group', 'placeholder':'Introduzca el asunto'}
    ))

    message = forms.CharField(label = "Asunto", required = True, widget = forms.Textarea(
        attrs = {'class':'form-group', 'placeholder':'Escriba su mensaje'}
    ))

    def clean_subject(self):
        if len(self.cleaned_data['subject']) < 3 or len(self.cleaned_data['subject']) > 25:
            raise forms.ValidationError('El campo debe tener 3 carácteres como mínimo y 25 como máximo')
        else:
            return self.cleaned_data['subject'].capitalize()

    def clean_message(self):
        if not self.cleaned_data['message'] is None or len(self.cleaned_data['message']) > 1000:
            raise forms.ValidationError('El campo debe tener 3 carácteres como mínimo y 1000 como máximo')
        else:
            return self.cleaned_data['message'].capitalize()

class RestaurantForm(forms.ModelForm):
    pass

class ProductForm(forms.ModelForm):
    pass

class PlaceForm(forms.ModelForm):
    pass

class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = '__all__'

    comment = forms.CharField(label = "Comentario", required = False, widget = forms.Textarea(
        attrs= {'class':'form-group', 'placeholder':'Escriba un comentario acerca del pedido...'}
    ))

    product = forms.ModelChoiceField(label = "Producto", queryset = Product.objects.all(), empty_label= "Seleccione un producto")

    # Mirar cómo añadir cliente desde aquí
    customer = forms.ModelChoiceField(label = "Cliente", queryset = Customer.objects.all(), empty_label= "Seleccione un cliente")

    def clean_comment(self):
        if len(self.cleaned_data['comment'] > 150):
            raise forms.ValidationError("El campo no puede exceder los 150 carácteres de longitud")
        else:
            return self.cleaned_data['comment'].capitalize()


