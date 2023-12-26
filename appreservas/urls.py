from django.urls import path
from .import views

from django.conf import settings

from django.contrib.staticfiles.urls import static
from django.conf.urls.static import static


#Acá el usuario va a poder entrar y acceder a la vista y se debe colocar la funcion definida en views.py en cada path
urlpatterns = [
    path('reservas', views.reservas, name='catalogo'),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)