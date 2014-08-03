from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'MP.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'inscripciones.views.inicio', name='inicio'),
    url(r'^actividad/$', 'inscripciones.views.form_actividad'),
    url(r'^formulario/$', 'inscripciones.views.formulario_view', name='vista_formulario'),
    url(r'^lista/$', 'inscripciones.views.lista_inscriptos_view'),
    url(r'^actividad/(?P<idActividad>\d+)/formulario/$', 'inscripciones.views.formulario_actividad_view'),
    url(r'^actividad/(?P<idActividad>\d+)/form/$', 'inscripciones.views.formulario_encuentro_view'),
    url(r'^login/$', 'inscripciones.views.iniciar_sesion'),
    url(r'^logout/$', 'inscripciones.views.cerrar_sesion'),
    url(r'^actividades/$', 'inscripciones.views.lista_actividades_view'),
    url(r'^actividades/nueva/$', 'inscripciones.views.agregar_actividad_view'),
    url(r'^actividades/(?P<id_actividad>\d+)/editar/$', 'inscripciones.views.editar_actividad_view'),
    url(r'^actividades/(?P<id_actividad>\d+)/inscriptos/$', 'inscripciones.views.inscriptos_view'),
    url(r'^actividades/(?P<id_actividad>\d+)/inscriptos/csv/$', 'inscripciones.views.csv_view'),
    url(r'^actividades/(?P<id_actividad>\d+)/eliminar/$', 'inscripciones.views.eliminar_actividad_view'),
    url(r'^actividades/(?P<id_actividad>\d+)/eliminada/$', 'inscripciones.views.actividad_eliminada_view'),

)
