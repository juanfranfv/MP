__author__ = 'jf'
from django import forms
from django.forms import Select
from inscripciones.models import *
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.admin.widgets import AdminDateWidget
from datetimewidget.widgets import DateTimeWidget
forms.DateInput.input_type = "date"

class MyForm(forms.ModelForm):

    error_css_class = 'list-group-item-danger'

    def __init__(self, *args, **kwargs):
        super(MyForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ActividadForm(MyForm):
    class Meta:
        model = Actividad
        widgets = {
            'fechaInicio': DateTimeWidget(attrs={'id': "id_fechaInicio"}, usel10n=True, bootstrap_version=3),
            'fechaFin': DateTimeWidget(attrs={'id': "id_fechaInicio"}, usel10n=True, bootstrap_version=3),
            'fechaActivacion': DateTimeWidget(attrs={'id': "id_fechaInicio"}, usel10n=True, bootstrap_version=3),
        }


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

class FormularioEncuentroForm(MyForm):

    class Meta:
        model = FormularioEncuentro
        exclude = ['direccionIP', 'fechaInscripcion', 'actividad', 'puesto']
        widgets = {
            'sexo': Select(choices=FormularioActividad.SEXO_OPCIONES),
        }
