from django import forms
from django.core.validators import EmailValidator

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
    pass