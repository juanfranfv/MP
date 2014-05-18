from django.shortcuts import render, render_to_response, HttpResponseRedirect, RequestContext
from forms import *
from models import *
from django.core.exceptions import *
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
    try:
        f = FormularioActividad.objects.get(direccionIP=ip, actividad=actividad)
    except ObjectDoesNotExist:
        ipBoolean = False

    if request.method=='POST':
        formularioMod = FormularioActividad()
        formularioMod.actividad = actividad
        formularioMod.direccionIP = ip
        formularioForm = FormularioActividadForm(request.POST, instance=formularioMod)

        if formularioForm.is_valid():
            formularioForm.save()
            return HttpResponseRedirect('/')
    else:
        formularioForm = FormularioActividadForm()
    return render_to_response('form-actividad2.html',
        {'formulario': formularioForm, 'ipBoolean':ipBoolean, 'actividad':actividad},
        context_instance=RequestContext(request))