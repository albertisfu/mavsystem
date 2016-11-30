from django.conf.urls import patterns, include, url
from django.contrib import admin
from panel import views
from django.contrib.auth.views import login, logout

urlpatterns = [
    # Examples:
    # url(r'^$', 'dental.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

 #    url(r'^$', views.home, name='home'),
     url(r'^login/$',login, {'template_name': 'login.html'}),
     url(r'^logout/$',logout, {'next_page': '/login/'}),
	# url(r'^administrar/ver_usuarios/$', verusuarios.as_view(), name='ver_usuarios'),
 #    url(r'^administrar/agregar_usuario/$', views.registrar, name='registrar_usuario'),
 #    url(r'^administrar/editar_usuario/(?P<pk>[0-9]+)/$', views.editarusuario, name='editar_usuario'),
 #    url(r'^administrar/borrar_usuario/(?P<pk>\d+)/$', deleteusuario.as_view(), name='borrar_usuario'),

    url(r'^prohibido/$', views.prohibido, name='prohibido'),
]