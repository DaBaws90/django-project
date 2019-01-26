from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator, EmailValidator
from .models import Customer, Review
from gestion_restaurante.models import Product
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import admin


class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        # fields = '__all__'
        exclude = ['slug', 'products', 'user']

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
            return self.cleaned_data['address'][:1].upper() + self.cleaned_data['address'][1:]
    

class UserForm(UserCreationForm): # Podríamos usar UserCreationForm
    
    class Meta:
        model = User
        fields = ('username', 'email')
        error_messages = {
            'username': {
                'unique': ('El nombre de usuario debe ser único'),
                'max_length': ('Demasiado largo. Máximo de carácteres: 150'),
            },
        }
        help_text = {
            'username': ('Obligatorio. 150 carácteres o menos. Letras, números y @/./+/-/_ permitidos.'),
        }


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(
                attrs= {'class': 'form-group'}
            ),
            'content': forms.Textarea(
                attrs={'cols': 60, 'rows': 6, 'class': 'from-group', 'placeholder': '¿Qué le ha parecido la experiencia?'}
            ),
        }
        help_texts = { 
            'title': ('Título de su opinión'),
            'content': ('Escriba aquí su opinión'),
            'valoration': ('Ayúdenos a seguir mejorando. Introduzca su valoración')
        }
        error_messages = { # No sobreescribe las validaciones ya que estas tienen prioridad (me refiero a los ValidationError)
            'title': {
                'max_length': ("Ha excedido la longitud máxima para este campo"),
            },
            'content': {
                'max_length': ("Parece que se ha extendido demasiado y ha rebasado la longitud máxima")
            }
        }
        localized_fields = '__all__'

    # title = forms.CharField(max_length = 30, required = True, label = "Título", widget = forms.TextInput(
    #     attrs = {'class':'form-group'}
    # ))
    # content = forms.CharField(max_length = 400, required = True, label = "Contenido", widget = forms.Textarea(
    #     attrs= {'class':'form-group', 'placeholder':'Escriba aquí su opinión...'}
    # ))
    valoration = forms.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], label = "Valoración", help_text = "Pónganos nota")

    author = forms.ModelChoiceField(label = "Escrito por", queryset = Customer.objects.all(), empty_label= "Seleccione un cliente")
    # OBtener el author a través de la instance actual

    def clean_title(self):
        if len(self.cleaned_data['title']) < 3 or len(self.cleaned_data['title']) > 30:
            raise forms.ValidationError('El campo debe tener 3 carácteres como mínimo y 30 como máximo')
        else:
            return self.cleaned_data['title'].capitalize()

    def clean_content(self):
        if len(self.cleaned_data['content']) < 20 or len(self.cleaned_data['content']) > 400:
            raise forms.ValidationError('El campo debe tener 20 carácteres como mínimo y 400 como máximo')
        else:
            return self.cleaned_data['content'].capitalize()