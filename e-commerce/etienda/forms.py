from django import forms
from django.core.exceptions import ValidationError

def validate_capitalized(value):
    if value[0] != value[0].upper():
        raise ValidationError("El nombre debe comenzar con una letra mayúscula.")

class ProductoForm(forms.Form):

	nombre = forms.CharField(label='Nombre', max_length=100, validators=[validate_capitalized])
	precio = forms.DecimalField(label='Precio')
	descripcion = forms.CharField(label='Descripcion', max_length=1000)
	categoria = forms.CharField(label='Categoria', max_length=100)
	imagen = forms.FileField()