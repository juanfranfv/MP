from django.db import models


# Create your models here.

class MiForm(models.Model):
    error_css_class = 'list-group-item-danger'
    def __init__(self, *args, **kwargs):
        super(MiForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class Actividad(models.Model):
    #Agregar * a campos obligatorios
    nombre = models.CharField(max_length=30)
    lugar = models.CharField(max_length=50)
    descripcion = models.TextField()
    requisitos = models.TextField()
    fechaInicio = models.DateTimeField()
    fechaFin = models.DateTimeField()
    fechaActivacion = models.DateTimeField()
    fechaCreacion = models.DateTimeField(auto_now=True)
    cantidadTitulares = models.PositiveIntegerField()
    cantidadSuplentes = models.PositiveIntegerField()
    nombreContacto = models.CharField(max_length=50)
    emailContacto = models.EmailField()
    ACTIVO = 'A'
    INACTIVO = 'I'
    FINALIZADO = 'F'
    ESTADO_OPCIONES = (
        (ACTIVO, 'Activo'),
        (INACTIVO, 'Inactivo'),
        (FINALIZADO, 'Finalizado'),
    )
    estado = models.CharField(max_length=1, choices=ESTADO_OPCIONES, default=INACTIVO)
    SI = 'SI'
    NO = 'NO'
    CONTROL_OPCIONES = (
        (SI, 'Si'),
        (NO, 'No'),
    )
    controlIP = models.CharField(max_length=2, choices=CONTROL_OPCIONES, default=NO, verbose_name='Control de IP')
    controlCI = models.CharField(max_length=2, choices=CONTROL_OPCIONES, default=NO, verbose_name='Control de CI')
    #usuario_creacion = models.ForeignKey('usuario')
    #tipo = models.ForeignKey('tipo', nombre="tipo_id")

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "actividades"


class Formulario(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    cedula = models.PositiveIntegerField()
    telefono = models.CharField(max_length=30)
    email = models.EmailField()

    def validIp(self):
        return True

    def __unicode__(self):
        return self.nombre

class FormularioActividad(models.Model):
    MASCULINO = 'M'
    FEMENINO = 'F'
    SEXO_OPCIONES = (
        (MASCULINO, 'Masculino'),
        (FEMENINO, 'Femenino')
    )

    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    edad = models.PositiveIntegerField()
    fechaNacimiento = models.DateField(verbose_name="Fecha de Nacimiento", help_text="Formato: dd/mm/aaaa")
    cedula = models.CharField(max_length=30)
    telefono = models.CharField(max_length=30)
    email = models.EmailField()
    institucion = models.CharField(max_length=30, verbose_name="Colegio/Universidad")
    curso = models.CharField(max_length=30, blank=True)
    sexo = models.CharField(max_length=1, choices=SEXO_OPCIONES)
    invitadoPeregrino = models.CharField(max_length=30, verbose_name="Peregrino que te invito", blank=True)
    enfermedad = models.TextField(verbose_name="Enfermedad/Alergias", blank=True)
    contacto = models.CharField(max_length=30, verbose_name='Nombre de Contacto')
    telefonoContacto = models.CharField(max_length=30, verbose_name='Telefono Contacto')
    relacionContacto = models.CharField(max_length=30, verbose_name='Relacion con Contacto')
    alimentacion = models.TextField(verbose_name="Dieta Especial", blank=True)
    comentarios = models.TextField(blank=True)
    direccionIP = models.IPAddressField()
    fechaInscripcion = models.DateTimeField(auto_now_add=True)
    actividad = models.ForeignKey(Actividad, blank=True, null=True)
    puesto = models.PositiveIntegerField()

    def validIp(self):
        return True

    def fechaNacimientoCorrectFormat(self):
        return str(self.fechaNacimiento.day) + '/' + str(self.fechaNacimiento.month) + '/' + str(self.fechaNacimiento.year)

    def __unicode__(self):
        return self.nombre
