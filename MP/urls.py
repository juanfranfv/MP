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
)
