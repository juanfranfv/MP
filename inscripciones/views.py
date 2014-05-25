from django.shortcuts import render, render_to_response, HttpResponseRedirect, RequestContext
from forms import *
from models import *
from django.core.exceptions import *
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail


# Create your views here.

def inicio(request):
    lista_actividades = Actividad.objects.all()

    return render_to_response('home.html', {'lista_actividades': lista_actividades}, context_instance=RequestContext(request))


def form_actividad(request):
    if request.method=='POST':
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

    ip = get_client_ip(request)
    actividad = Actividad.objects.get(pk=idActividad)
    ipBoolean = True
    cantidadPermitida = actividad.cantidadSuplentes + actividad.cantidadTitulares
    cantidadInscriptos = FormularioActividad.objects.filter(actividad=actividad).count()
    if cantidadInscriptos >= cantidadPermitida:
        suceso = False
        mensaje = 'El cupo  para "' + actividad.nombre + '" se encuentra lleno'
        mensaje += '\n'
        mensaje += 'Si tiene alguna consulta, comuniquese con el encargado de inscripciones al correo: '
        mensaje += actividad.emailContacto
        return render_to_response(
            'home.html',
            {'mensaje': mensaje, 'suceso': suceso},
            context_instance=RequestContext(request)
        )

    if timezone.now() < actividad.fechaActivacion:
        suceso = False
        mensaje = 'La inscripcion a "' + actividad.nombre + '" aun no se encuentra habilitada'
        lista_actividades = Actividad.objects.all()
        return render_to_response(
            'home.html',
            {'mensaje': mensaje, 'suceso': suceso, 'lista_actividades': lista_actividades},
            context_instance=RequestContext(request)
        )
    try:
        f = FormularioActividad.objects.get(direccionIP=ip, actividad=actividad)
    except ObjectDoesNotExist:
        ipBoolean = False


    if request.method=='POST':
        formularioMod = FormularioActividad()
        formularioMod.actividad = actividad
        formularioMod.direccionIP = ip
        formularioMod.puesto = 1000
        formularioForm = FormularioActividadForm(request.POST, instance=formularioMod)

        if formularioForm.is_valid():

            inscripto = formularioForm.save()
            cantidad = FormularioActividad.objects.filter(actividad=actividad).filter(pk__lte=inscripto.id).count()
            inscripto.puesto = cantidad
            inscripto.save()
            titulo_mail = 'Inscripcion a "' + actividad.nombre + '"'
            if inscripto.puesto < actividad.cantidadTitulares:
                mensaje_mail = 'Su inscripcion ha sido procesada con exito'
            else:
                mensaje_mail = 'Usted esta en lista de espera'
            destinatario = [inscripto.email]
            send_mail(titulo_mail, mensaje_mail, settings.EMAIL_HOST_USER, destinatario, fail_silently=False)
            suceso = True
            mensaje = 'Su solicitud ha sido procesada con exito'
            return render_to_response(
                'home.html',
                {'mensaje': mensaje, 'suceso': suceso},
                context_instance=RequestContext(request)
            )
    else:
        formularioForm = FormularioActividadForm()
    return render_to_response(
        'form-actividad2.html',
        {'formulario': formularioForm, 'ipBoolean':ipBoolean, 'actividad':actividad},
        context_instance=RequestContext(request)
    )

def iniciar_sesion(request):

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


@login_required(login_url='/iniciar_sesion')
def lista_actividades_view(request):
    actividades = Actividad.objects.all()
    return render_to_response(
        'lista_actividades.html',
        {'lista_actividades': actividades},
        context_instance=RequestContext(request)
    )

@login_required(login_url='/iniciar_sesion')
def inscriptos_view(request, id_actividad):
    actividad = Actividad.objects.get(pk=id_actividad)
    lista_inscriptos = FormularioActividad.objects.filter(actividad=actividad)
    return render_to_response(
        'inscriptos.html',
        {'lista_inscriptos': lista_inscriptos, 'actividad': actividad},
        context_instance=RequestContext(request)
    )