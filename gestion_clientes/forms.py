from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator, EmailValidator
from .models import Customer, Review


class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = '__all__'

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
    
    # def clean_slug(self):
    #     if self.cleaned_data['slug'] == "":
    #         return self.cleaned_data['name'] + '-' + self.cleaned_data['middlename'] + '-' + self.cleaned_data['lastname']


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = '__all__'

    title = forms.CharField(max_length = 30, required = True, label = "Título", widget = forms.TextInput(
        attrs = {'class':'form-group'}
    ))
    content = forms.CharField(max_length = 400, required = True, label = "Contenido", widget = forms.Textarea(
        attrs= {'class':'form-group', 'placeholder':'Escriba aquí su opinión...'}
    ))
    valoration = forms.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], label = "Valoración")

    author = forms.ModelChoiceField(label = "Escrito por", queryset = Customer.objects.all(), empty_label= "Seleccione un cliente")

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