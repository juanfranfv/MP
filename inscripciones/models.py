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
    nombre = models.CharField(max_length=100, verbose_name="Nombre *")
    lugar = models.CharField(max_length=100, verbose_name="Lugar *")
    descripcion = models.TextField(blank=True)
    costo = models.CharField(max_length=100, verbose_name= 'Costo *')
    requisitos = models.TextField(verbose_name="Requisitos *")
    fechaInicio = models.DateTimeField(verbose_name="Fecha de inicio *")
    fechaFin = models.DateTimeField(verbose_name="Fecha de finalizacion *")
    fechaActivacion = models.DateTimeField(verbose_name="Fecha de activacion *")
    fechaCreacion = models.DateTimeField(auto_now=True)
    cantidadTitulares = models.PositiveIntegerField(verbose_name="Cantidad de Titulares *")
    cantidadSuplentes = models.PositiveIntegerField(verbose_name="Cantidad de Suplentes")
    nombreContacto = models.CharField(max_length=100, verbose_name="Nombre de contacto")
    emailContacto = models.EmailField(verbose_name="Email de contacto")
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
    encuentro = models.CharField(max_length=2, choices=CONTROL_OPCIONES, default=NO, verbose_name='Retiro de encuentro')
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

class FormularioEncuentro(models.Model):
    MASCULINO = 'M'
    FEMENINO = 'F'
    SEXO_OPCIONES = (
        (MASCULINO, 'Masculino'),
        (FEMENINO, 'Femenino')
    )

    nombre = models.CharField(max_length=100, verbose_name="Nombre (*)")
    apellido = models.CharField(max_length=100, verbose_name="Apellido (*)")
    edad = models.PositiveIntegerField(verbose_name="Edad")
    fechaNacimiento = models.DateField(verbose_name="Fecha de Nacimiento (*)")
    cedula = models.CharField(max_length=30, verbose_name="Cedula (*)")
    telefono = models.CharField(max_length=30, verbose_name="Telefono (*)")
    email = models.EmailField(verbose_name="Email (*)")
    institucion = models.CharField(max_length=100, verbose_name="Colegio/Universidad (*)")
    curso = models.CharField(max_length=100, blank=True)
    sexo = models.CharField(max_length=1, choices=SEXO_OPCIONES, verbose_name="Sexo (*)")
    invitadoPeregrino = models.CharField(max_length=100, verbose_name="Peregrino que te invito", blank=True)
    enfermedad = models.TextField(verbose_name="Enfermedad/Alergias", blank=True)
    contacto = models.CharField(max_length=50, verbose_name='Nombre de Contacto (*)')
    telefonoContacto = models.CharField(max_length=50, verbose_name='Telefono Contacto (*)')
    relacionContacto = models.CharField(max_length=50, verbose_name='Relacion con Contacto (*)')
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


class FormularioActividad(models.Model):
    MASCULINO = 'M'
    FEMENINO = 'F'
    SEXO_OPCIONES = (
        (MASCULINO, 'Masculino'),
        (FEMENINO, 'Femenino')
    )

    nombre = models.CharField(max_length=100, verbose_name="Nombre (*)")
    apellido = models.CharField(max_length=100, verbose_name="Apellido (*)")
    cedula = models.CharField(max_length=30, verbose_name="Cedula (*)")
    telefono = models.CharField(max_length=30, verbose_name="Telefono (*)")
    email = models.EmailField(verbose_name="Email (*)")
    edad = models.PositiveIntegerField(verbose_name="Edad")
    fechaNacimiento = models.DateField(verbose_name="Fecha de Nacimiento (*)")
    fechaRetiroEncuetro = models.DateField("Fecha de Retiro de Encuentro (*)")
    coordinador = models.CharField(max_length=100, verbose_name="Coordinador de Retiro de Encuentro")
    institucion = models.CharField(max_length=100, verbose_name="Colegio/Universidad (*)",)
    curso = models.CharField(max_length=100, blank=True)
    sexo = models.CharField(max_length=1, choices=SEXO_OPCIONES, verbose_name="Sexo (*)")
    enfermedad = models.TextField(verbose_name="Enfermedad/Alergias", blank=True)
    contacto = models.CharField(max_length=50, verbose_name='Nombre de Contacto (*)')
    telefonoContacto = models.CharField(max_length=50, verbose_name='Telefono Contacto (*)')
    relacionContacto = models.CharField(max_length=50, verbose_name='Relacion con Contacto (*)')
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
