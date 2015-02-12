# -*- encoding: utf-8 -*-

from django.shortcuts import render, render_to_response, HttpResponseRedirect, RequestContext, Http404
from forms import *
from models import *
from django.core.exceptions import *
from django.template import Context, loader
from django.template.loader import get_template
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.db import IntegrityError
import csv
import StringIO
from django.http import HttpResponse
from datetime import datetime, timedelta


def envio_mail(inscripto, archivo):
    htmly = get_template('emails/' + archivo + '.html')
    origen = 'Movimiento Peregrino <retiros-noreply@movimientoperegrino.org>'

    if archivo == 'inscripcion-titular':
        asunto = '[MP] Solicitud recibida'

    if archivo == 'inscripcion-suplente':
        asunto = '[MP] Lista de Espera'

    d = Context({'inscripto': inscripto})
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(asunto, html_content, origen, [inscripto.email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def inicio(request):
    lista_actividades = Actividad.objects.all().order_by('fechaActivacion').reverse()
    fechaActivacion = timezone.now() + timedelta(days=16)
    fechaFin = timezone.now() + timedelta(days=1)
    lista_actividades = lista_actividades.exclude(fechaFin__lte=fechaFin).exclude(fechaActivacion__gte=fechaActivacion)

    return render_to_response('home.html', {'lista_actividades': lista_actividades},
                              context_instance=RequestContext(request))


def form_actividad(request):
    if request.method == 'POST':
        formulario = ActividadForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/inicio/')
    else:
        formulario = ActividadForm()
    return render_to_response(
        'form-retiro.html',
        {'formulario': formulario},
        context_instance=RequestContext(request)
    )


def formulario_view(request):
    if request.method=='POST':
        #formularioMod = Formulario(Direccion_ip= request.META.get('REMOTE_ADDR'))
        #actividad = Actividad.objects.get(pk=1)
        #formularioMod.Actividad =actividad
        formularioForm = FormularioForm(request.POST)

        if formularioForm.is_valid():
            formularioForm.save()
            return HttpResponseRedirect('/')
    else:
        formularioForm = FormularioForm()
    return render_to_response('form-retiro.html',
        {'formulario': formularioForm},
        context_instance=RequestContext(request))


def lista_inscriptos_view(request):
    lista_inscriptos = Formulario.objects.all()
    return render_to_response('lista.html', {'lista_inscriptos':lista_inscriptos}, context_instance=RequestContext(request))


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def formulario_actividad_view(request, idActividad):
    #formulario_actividad

    ip = get_client_ip(request)
    actividad = Actividad.objects.get(pk=idActividad)

    #si el estado de la actividad es finalizado, termina la inscripcion
    if actividad.estado == Actividad.FINALIZADO:
        suceso = False
        mensaje = 'La inscripcion a la actividad: "' + actividad.nombre + '" ha finalizado.'
        mensaje += ' Si tiene alguna consulta, comuniquese con el encargado de inscripciones al correo: '
        mensaje += actividad.emailContacto
        return render_to_response(
            'home.html',
            {'mensaje': mensaje, 'suceso': suceso},
            context_instance=RequestContext(request)
        )

    #se controla la cantidad de inscriptos
    cantidadPermitida = actividad.cantidadSuplentes + actividad.cantidadTitulares
    cantidadInscriptos = FormularioActividad.objects.filter(actividad=actividad).count()
    if cantidadInscriptos >= cantidadPermitida:
        suceso = False
        mensaje = 'El cupo  para "' + actividad.nombre + '" se encuentra lleno.'
        mensaje += ' Si tiene alguna consulta, comuniquese con el encargado de inscripciones al correo: '
        mensaje += actividad.emailContacto
        return render_to_response(
            'home.html',
            {'mensaje': mensaje, 'suceso': suceso},
            context_instance=RequestContext(request)
        )

    #se controla la fecha/hora de activacion
    if timezone.now() < actividad.fechaActivacion:
        suceso = False
        mensaje = 'La inscripcion a  la actividad "' + actividad.nombre + '" aun no se encuentra habilitada'
        lista_actividades = Actividad.objects.all()
        return render_to_response(
            'home.html',
            {'mensaje': mensaje, 'suceso': suceso, 'lista_actividades': lista_actividades},
            context_instance=RequestContext(request)
        )
    else:
        if actividad.estado == Actividad.INACTIVO:
            actividad.estado = Actividad.ACTIVO
            actividad.save()

    #se verifica la ip
    if actividad.controlIP == Actividad.SI:
        #Si ipBoolean es True significa que ya se inscribieron con esa IP
        ipBoolean = True
        try:
            f = FormularioActividad.objects.get(direccionIP=ip, actividad=actividad)

        except ObjectDoesNotExist:
            ipBoolean = False

        if ipBoolean == True:
            suceso = False
            mensaje = 'ERROR: Usted ya se ha inscripto a esta actividad'
            return render_to_response(
                'home.html',
                {'mensaje': mensaje, 'suceso': suceso},
                context_instance=RequestContext(request)
            )
    else:
        ipBoolean = False
        
    
    #se procesa el POST
    if request.method == 'POST':
        instanciaFormulario = FormularioActividad()
        instanciaFormulario.actividad = actividad
        instanciaFormulario.direccionIP = ip
        instanciaFormulario.puesto = 1000

        formulario = FormularioActividadForm(request.POST, instance=instanciaFormulario)
        if formulario.is_valid():
            if actividad.controlCI == Actividad.SI:
                cedula = formulario.cleaned_data['cedula']


                #Si ciBoolean es True significa que ya se inscribieron con esa CI
                ciBoolean = True
                try:
                    f = FormularioActividad.objects.get(actividad=actividad, cedula=cedula)

                except ObjectDoesNotExist:
                    ciBoolean = False

                if ciBoolean == True:
                    suceso = False
                    mensaje = 'ERROR: Usted ya se ha inscripto a esta actividad'
                    return render_to_response(
                        'home.html',
                        {'mensaje': mensaje, 'suceso': suceso},
                        context_instance=RequestContext(request)
                    )

            try:
                inscripto = formulario.save()
            except IntegrityError:
                suceso = False
                mensaje = 'ERROR: Usted ya se ha inscripto a esta actividad'
                return render_to_response(
                    'home.html',
                    {'mensaje': mensaje, 'suceso': suceso},
                    context_instance=RequestContext(request)
                )
            cantidad = FormularioActividad.objects.filter(actividad=actividad).filter(pk__lte=inscripto.id).count()
            inscripto.puesto = cantidad
            inscripto.save()
            titulo_mail = 'Inscripcion a "' + actividad.nombre + '"'
            if inscripto.puesto <= actividad.cantidadTitulares:
                envio_mail(inscripto, 'inscripcion-titular')

            else:
                envio_mail(inscripto, 'inscripcion-suplente')

            suceso = True
            mensaje = 'Su solicitud ha sido procesada con exito'

            if cantidad == cantidadPermitida:
                if actividad.estado == Actividad.ACTIVO:
                    actividad.estado = actividad.FINALIZADO
                    actividad.save()
                    lista_inscriptos = FormularioActividad.objects.filter(actividad=actividad).order_by('puesto')
                    csvfile = StringIO.StringIO()
                    csvwriter = csv.writer(csvfile, delimiter=';')
                    csvwriter.writerow(['Puesto', 'Nombre', 'Apellido', 'Edad', 'Fecha de Nacimiento',
                                        'Cedula', 'Telefono', 'Email', 'Colegio/Universidad', 'Curso', 'Sexo',
                                        'Fecha de Retiro Encuentro', 'Coordinador', 'Enfermedades o Alergias', 'Contacto',
                                        'Relacion', 'Telefono Contacto', 'Dieta Especial', 'Comentarios', 'IP',
                                        'Fecha de inscripcion'])
                    for inscripto in lista_inscriptos:
                        csvwriter.writerow([inscripto.puesto, inscripto.nombre.encode('utf-8'), inscripto.apellido.encode('utf-8'),
                                            inscripto.edad, inscripto.fechaNacimiento, inscripto.cedula.encode('utf8'),
                                            inscripto.telefono.encode('utf-8'), inscripto.email, inscripto.institucion.encode('utf-8'),
                                            inscripto.curso.encode('utf-8'), inscripto.get_sexo_display(), inscripto.fechaRetiroEncuetro,
                                            inscripto.coordinador.encode('utf-8'), inscripto.enfermedad.encode('utf-8'),
                                            inscripto.contacto.encode('utf-8'), inscripto.relacionContacto.encode('utf-8'),
                                            inscripto.telefonoContacto.encode('utf-8'), inscripto.alimentacion.encode('utf-8'),
                                            inscripto.comentarios.encode('utf-8'),
                                            inscripto.direccionIP, inscripto.fechaInscripcion])
                    email = EmailMessage('Inscriptos', 'Documento con los inscriptos',
                                         settings.EMAIL_HOST_USER, [actividad.emailContacto])
                    email.attach('inscriptos-' + actividad.nombre + '.csv', csvfile.getvalue(), 'text/csv')
                    email.send()
            return render_to_response(
                'home.html',
                {'mensaje': mensaje, 'suceso': suceso},
                context_instance=RequestContext(request)
            )
    else:
        formulario = FormularioActividadForm()
    return render_to_response(
        'form-actividad2.html',
        {'formulario': formulario, 'ipBoolean':ipBoolean, 'actividad':actividad},
        context_instance=RequestContext(request)
    )


def formulario_encuentro_view(request, idActividad):
    #formulario_actividad

    ip = get_client_ip(request)
    actividad = Actividad.objects.get(pk=idActividad)

    if actividad.estado == Actividad.FINALIZADO:
        suceso = False
        mensaje = 'La inscripcion a la actividad: "' + actividad.nombre + '" ha finalizado.'
        mensaje += ' Si tiene alguna consulta, comuniquese con el encargado de inscripciones al correo: '
        mensaje += actividad.emailContacto
        return render_to_response(
            'home.html',
            {'mensaje': mensaje, 'suceso': suceso},
            context_instance=RequestContext(request)
        )

    cantidadPermitida = actividad.cantidadSuplentes + actividad.cantidadTitulares
    cantidadInscriptos = FormularioEncuentro.objects.filter(actividad=actividad).count()
    if cantidadInscriptos >= cantidadPermitida:
        suceso = False
        mensaje = 'El cupo  para "' + actividad.nombre + '" se encuentra lleno.'
        mensaje += ' Si tiene alguna consulta, comuniquese con el encargado de inscripciones al correo: '
        mensaje += actividad.emailContacto
        return render_to_response(
            'home.html',
            {'mensaje': mensaje, 'suceso': suceso},
            context_instance=RequestContext(request)
        )

    if timezone.now() < actividad.fechaActivacion:
        suceso = False
        mensaje = 'La inscripcion a  la actividad "' + actividad.nombre + '" aun no se encuentra habilitada'
        lista_actividades = Actividad.objects.all()
        return render_to_response(
            'home.html',
            {'mensaje': mensaje, 'suceso': suceso, 'lista_actividades': lista_actividades},
            context_instance=RequestContext(request)
        )
    else:
        if actividad.estado == Actividad.INACTIVO:
            actividad.estado = Actividad.ACTIVO
            actividad.save()

    if actividad.controlIP == Actividad.SI:
        #Si ipBoolean es True significa que ya se inscribieron con esa IP
        ipBoolean = True
        try:
            f = FormularioEncuentro.objects.get(direccionIP=ip, actividad=actividad)

        except ObjectDoesNotExist:
            ipBoolean = False

        if ipBoolean == True:
            suceso = False
            mensaje = 'ERROR: Usted ya se ha inscripto a esta actividad'
            return render_to_response(
                'home.html',
                {'mensaje': mensaje, 'suceso': suceso},
                context_instance=RequestContext(request)
            )
    else:
        ipBoolean = False



    if request.method == 'POST':
        instanciaFormulario = FormularioEncuentro()
        instanciaFormulario.actividad = actividad
        instanciaFormulario.direccionIP = ip
        instanciaFormulario.puesto = 1000
        formulario = FormularioEncuentroForm(request.POST, instance=instanciaFormulario)

        if formulario.is_valid():
            if actividad.controlCI == Actividad.SI:
                cedula = formulario.cleaned_data['cedula']
                #Si ciBoolean es True significa que ya se inscribieron con esa CI
                ciBoolean = True
                try:
                    f = FormularioEncuentro.objects.get(actividad=actividad, cedula=cedula)

                except ObjectDoesNotExist:
                    ciBoolean = False

                if ciBoolean:
                    suceso = False
                    mensaje = 'ERROR: Usted ya se ha inscripto a esta actividad'
                    return render_to_response(
                        'home.html',
                        {'mensaje': mensaje, 'suceso': suceso},
                        context_instance=RequestContext(request)
                    )

            try:
                inscripto = formulario.save()
            except IntegrityError:
                suceso = False
                mensaje = 'ERROR: Usted ya se ha inscripto a esta actividad'
                return render_to_response(
                    'home.html',
                    {'mensaje': mensaje, 'suceso': suceso},
                    context_instance=RequestContext(request)
                )
            cantidad = FormularioEncuentro.objects.filter(actividad=actividad).filter(pk__lte=inscripto.id).count()
            inscripto.puesto = cantidad
            inscripto.save()
            titulo_mail = 'Inscripcion a "' + actividad.nombre + '"'
            if inscripto.puesto <= actividad.cantidadTitulares:
                envio_mail(inscripto, 'inscripcion-titular')

            else:
                envio_mail(inscripto, 'inscripcion-suplente')

            suceso = True
            mensaje = 'Su solicitud ha sido procesada con exito'

            if cantidad == cantidadPermitida:
                if actividad.estado == Actividad.ACTIVO:
                    actividad.estado = actividad.FINALIZADO
                    actividad.save()
                    lista_inscriptos = FormularioEncuentro.objects.filter(actividad=actividad).order_by('puesto')

                    csvfile = StringIO.StringIO()
                    csvwriter = csv.writer(csvfile, delimiter=';')
                    csvwriter.writerow(['Puesto', 'Nombre', 'Apellido', 'Edad', 'Fecha de Nacimiento',
                                        'Cedula', 'Telefono', 'Email', 'Colegio/Universidad', 'Curso', 'Sexo',
                                        'Peregrino que le invito', 'Enfermedades o Alergias', 'Contacto', 'Relacion',
                                        'Telefono Contacto', 'Dieta Especial', 'Comentarios', 'IP',
                                        'Fecha de inscripcion'])
                    for inscripto in lista_inscriptos:
                        csvwriter.writerow([inscripto.puesto, inscripto.nombre.encode('utf-8'), inscripto.apellido.encode('utf-8'),
                                            inscripto.edad, inscripto.fechaNacimiento, inscripto.cedula.encode('utf-8'),
                                            inscripto.telefono.encode('utf-8'), inscripto.email, inscripto.institucion.encode('utf-8'),
                                            inscripto.curso.encode('utf-8'), inscripto.get_sexo_display(), inscripto.invitadoPeregrino.encode('utf-8'),
                                            inscripto.enfermedad.encode('utf-8'), inscripto.contacto.encode('utf-8'), inscripto.relacionContacto.encode('utf-8'),
                                            inscripto.telefonoContacto.encode('utf-8'), inscripto.alimentacion.encode('utf-8'), inscripto.comentarios.encode('utf-8'),
                                            inscripto.direccionIP, inscripto.fechaInscripcion])

                    email = EmailMessage('Inscriptos', 'Documento con los inscriptos',
                                         settings.EMAIL_HOST_USER, [actividad.emailContacto])
                    email.attach('inscriptos-' + actividad.nombre + '.csv', csvfile.getvalue(), 'text/csv')
                    email.send()
            return render_to_response(
                'home.html',
                {'mensaje': mensaje, 'suceso': suceso},
                context_instance=RequestContext(request)
            )
    else:
        formulario = FormularioEncuentroForm()
    return render_to_response(
        'form-actividad2.html',
        {'formulario': formulario, 'ipBoolean': ipBoolean, 'actividad': actividad},
        context_instance=RequestContext(request)
    )


def iniciar_sesion(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect('/actividades')
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username=usuario, password=clave)
            if acceso is not None:
                if acceso.is_active:
                    login(request, acceso)
                    return lista_actividades_view(request)
    else:
        formulario = AuthenticationForm()
    return render_to_response('iniciar_sesion.html', {'formulario': formulario},
                              context_instance=RequestContext(request))


def cerrar_sesion(request):
    logout(request)
    return HttpResponseRedirect('/login')


@login_required(login_url='/login')
def lista_actividades_view(request):
    if request.user.is_superuser:
        actividades = Actividad.objects.all().order_by('fechaActivacion').reverse()
        return render_to_response(
            'lista_actividades.html',
            {'lista_actividades': actividades},
            context_instance=RequestContext(request)
        )
    else:
        actividades = Actividad.objects.all().order_by('fechaActivacion').reverse()
        return render_to_response(
            'lista_actividades2.html',
            {'lista_actividades': actividades},
            context_instance=RequestContext(request)
        )


@login_required(login_url='/login')
def inscriptos_view(request, id_actividad):
    actividad = Actividad.objects.get(pk=id_actividad)

    if actividad.encuentro == Actividad.SI:
        html = 'inscriptos-encuentro.html'
        lista_inscriptos = FormularioEncuentro.objects.filter(actividad=actividad).order_by('puesto')



    else:
        html = 'inscriptos.html'
        lista_inscriptos = FormularioActividad.objects.filter(actividad=actividad).order_by('puesto')

    return render_to_response(
        html,
        {'lista_inscriptos': lista_inscriptos, 'actividad': actividad},
        context_instance=RequestContext(request)
    )


@login_required(login_url='/login')
def csv_view(request, id_actividad):

    actividad = Actividad.objects.get(pk=id_actividad)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inscriptos.csv"'

    writer = csv.writer(response, delimiter=';')

    if actividad.encuentro == Actividad.SI:
        #csvwriter = csv.writer(csvfile, delimiter=';')
        lista_inscriptos = FormularioEncuentro.objects.filter(actividad=actividad).order_by('puesto')
        writer.writerow(['Puesto', 'Nombre', 'Apellido', 'Edad', 'Fecha de Nacimiento',
                            'Cedula', 'Telefono', 'Email', 'Colegio/Universidad', 'Curso', 'Sexo',
                            'Peregrino que le invito', 'Enfermedades o Alergias', 'Contacto', 'Relacion',
                            'Telefono Contacto', 'Dieta Especial', 'Comentarios', 'IP',
                            'Fecha de inscripcion'])
        for inscripto in lista_inscriptos:
            writer.writerow([inscripto.puesto, inscripto.nombre.encode('utf-8'), inscripto.apellido.encode('utf-8'),
                                inscripto.edad, inscripto.fechaNacimiento, inscripto.cedula.encode('utf-8'),
                                inscripto.telefono.encode('utf-8'), inscripto.email, inscripto.institucion.encode('utf-8'),
                                inscripto.curso.encode('utf-8'), inscripto.get_sexo_display(), inscripto.invitadoPeregrino.encode('utf-8'),
                                inscripto.enfermedad.encode('utf-8'), inscripto.contacto.encode('utf-8'), inscripto.relacionContacto.encode('utf-8'),
                                inscripto.telefonoContacto.encode('utf-8'), inscripto.alimentacion.encode('utf-8'), inscripto.comentarios.encode('utf-8'),
                                inscripto.direccionIP, inscripto.fechaInscripcion])


    else:
        lista_inscriptos = FormularioActividad.objects.filter(actividad=actividad).order_by('puesto')
        #csvfile = StringIO.StringIO()
        #csvwriter = csv.writer(csvfile, delimiter=';')
        writer.writerow(['Puesto', 'Nombre', 'Apellido', 'Edad', 'Fecha de Nacimiento',
                            'Cedula', 'Telefono', 'Email', 'Colegio/Universidad', 'Curso', 'Sexo',
                            'Fecha de Retiro Encuentro', 'Coordinador', 'Enfermedades o Alergias', 'Contacto',
                            'Relacion', 'Telefono Contacto', 'Dieta Especial', 'Comentarios', 'IP',
                            'Fecha de inscripcion'])
        for inscripto in lista_inscriptos:
            writer.writerow([inscripto.puesto, inscripto.nombre.encode('utf-8'), inscripto.apellido.encode('utf-8'),
                                inscripto.edad, inscripto.fechaNacimiento, inscripto.cedula.encode('utf8'),
                                inscripto.telefono.encode('utf-8'), inscripto.email, inscripto.institucion.encode('utf-8'),
                                inscripto.curso.encode('utf-8'), inscripto.get_sexo_display(), inscripto.fechaRetiroEncuetro,
                                inscripto.coordinador.encode('utf-8'), inscripto.enfermedad.encode('utf-8'),
                                inscripto.contacto.encode('utf-8'), inscripto.relacionContacto.encode('utf-8'),
                                inscripto.telefonoContacto.encode('utf-8'), inscripto.alimentacion.encode('utf-8'),
                                inscripto.comentarios.encode('utf-8'),
                                inscripto.direccionIP, inscripto.fechaInscripcion])



    return response


@login_required(login_url='/login')
def agregar_actividad_view(request):
    if request.method == 'POST':
        formulario = ActividadForm(request.POST)

        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/login')
    else:
        formulario = ActividadForm()

    titulo = 'Nueva actividad'
    return render_to_response(
        'form-actividad-nueva.html',
        {'formulario': formulario, 'titulo': titulo},
        context_instance=RequestContext(request)
    )


@login_required(login_url='/login')
def editar_actividad_view(request, id_actividad):
    try:
        actividad = Actividad.objects.get(pk=id_actividad)
    except Actividad.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        formulario = ActividadForm(request.POST, instance=actividad)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/actividades')

    else:
        formulario = ActividadForm(instance=actividad)

    titulo = 'Editar actividad: ' + actividad.nombre
    return render_to_response(
        'form-actividad-nueva.html',
        {'formulario': formulario, 'titulo': titulo},
        context_instance=RequestContext(request)
    )


@login_required(login_url='/login')
def eliminar_actividad_view(request, id_actividad):
    try:
        actividad = Actividad.objects.get(pk=id_actividad)
    except Actividad.DoesNotExist:
        raise Http404
    return render_to_response(
        'eliminar-actividad.html',
        {'actividad': actividad},
        context_instance=RequestContext(request)
    )


@login_required(login_url='/login')
def actividad_eliminada_view(request, id_actividad):
    try:
        actividad = Actividad.objects.get(pk=id_actividad)
    except Actividad.DoesNotExist:
        raise Http404
    mensaje = "La actividad " + actividad.nombre + " ha sido eliminada con exito."
    actividad.delete()
    actividades = Actividad.objects.all().order_by('fechaActivacion').reverse()
    return render_to_response(
        'lista_actividades.html',
        {'mensaje': mensaje, 'lista_actividades': actividades},
        context_instance=RequestContext(request)
    )