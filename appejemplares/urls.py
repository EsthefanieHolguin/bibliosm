from django.urls import path
from .import views

from django.conf import settings

from django.contrib.staticfiles.urls import static
from django.conf.urls.static import static


#Acá el usuario va a poder entrar y acceder a la vista y se debe colocar la funcion definida en views.py en cada path
urlpatterns = [
    path('', views.inicio, name='inicio'), #Cuando el usuario acceda a la raiz (''), mostrará la vista 'inicio'
    path('nosotros', views.nosotros, name='nosotros'), #creamos el acceso a la vista de nosotros con el acceso views.nosotros
    path('libros', views.libros, name='libros'),
    path('libros/crear', views.crear, name='crear'),
    path('libros/editar', views.editar, name='editar'),
    path('eliminar/<int:isbn>', views.eliminar, name='eliminar'),
    path('libros/editar/<int:isbn>', views.editar, name='editar'),
    path('csv/upload', views.subir_csv, name='subir_csv'),
    path('catalogo', views.catalogo, name='catalogo'),
    path('logout/', views.exit, name='exit'),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)