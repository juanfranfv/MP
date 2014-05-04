__author__ = 'jf'
from django import forms
from inscripciones.models import *

class MyForm(forms.ModelForm):

    error_css_class = 'list-group-item-danger'
    def __init__(self, *args, **kwargs):
        super(MyForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad

class FormularioForm(MyForm):
    class Meta:
        model = Formulario
        #exclude = ['Direccion_ip', 'Fecha_inscripcion', 'Actividad']