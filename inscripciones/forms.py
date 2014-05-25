__author__ = 'jf'
from django import forms
from django.forms import Select
from inscripciones.models import *
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.admin.widgets import AdminDateWidget

forms.DateInput.input_type = "date"

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

class FormularioActividadForm(MyForm):

    class Meta:
        model = FormularioActividad
        exclude = ['direccionIP', 'fechaInscripcion', 'actividad', 'puesto']
        widgets = {
            'sexo': Select(choices=FormularioActividad.SEXO_OPCIONES),
        }
