from dataclasses import fields
from pyexpat import model
from django import forms
from .models import Carrito, Producto, Cliente,Empresa_convenio
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from django.conf import settings

# Aquí las class formularios
class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', "first_name", "last_name", "email", "password1", "password2"]

class ClienteForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        model = Cliente
        fields = ['direccion', "rut", "numero_telefono", "fecha_nacimiento"]

class ProductoForm(forms.ModelForm):
    fecha_publicacion = forms.DateTimeField(input_formats=['%m/%d/%Y %H:%M'])
    '''disponible = forms.TypedChoiceField(
        label = "Está disponible?",
        choices = ((1, "Sí"), (0, "No")),
        coerce = lambda x: bool(int(x)),
        widget = forms.RadioSelect,
        initial = '1',
        required = True,
    )'''
    
    class Meta:
        model = Producto
        #fields = ['restaurant','tipo_producto','tipo_menu','nombre','precio','descripcion','imagen','fecha_publicacion','stock','disponible']
        fields = '__all__'
        
        '''
        widgets = {
            "fecha_publicacion": forms.SelectDateWidget()
            #"disponible": forms.CheckboxInput()
        }'''

class CarritoForm(forms.ModelForm):
    fecha_programada = forms.DateTimeField(input_formats=['%m/%d/%Y %H:%M'])
    
    class Meta:
        model = Carrito
        fields = ['fecha_programada']
        
class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa_convenio
        fields = '__all__'