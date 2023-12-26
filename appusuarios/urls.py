from django.urls import path
from .import views

from django.conf import settings

from django.contrib.staticfiles.urls import static
from django.conf.urls.static import static


#Acá el usuario va a poder entrar y acceder a la vista y se debe colocar la funcion definida en views.py en cada path
urlpatterns = [
    path('usuarios', views.usuarios, name='usuarios'),
    path('usuarios/crear', views.crear, name='crear_usuario'),
    path('usuarios/editar', views.editar, name='editar_usuario'),
    path('usuarios/eliminar/<int:rut_usuario>', views.eliminar, name='eliminar_usuario'),
    path('usuarios/editar/<int:rut_usuario>', views.editar, name='editar_usuario'),
    path('usuarios/upload', views.subir_usuarios, name='subir_usuarios'),




]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)