from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q
from .models import Prestamo
from .forms import PrestamoForm
from django.contrib.auth.forms import AuthenticationForm
from appejemplares.models import Libro
from appejemplares import views
from appusuarios.models import Usuario
from django.dispatch import receiver
from django.db.models.signals import pre_save
from datetime import date, timedelta

# Create your views here.
@login_required
def prestamos(request):
    busqueda = request.GET.get("buscar_prestamo")
    prestamos = Prestamo.objects.all()

   #querys con la busqueda, que se obtiene del input name del index.html
    if busqueda:
        prestamos = Prestamo.objects.filter( 
            Q(isbn = busqueda) |
            Q(rut_usuario = busqueda) |
            Q(estado_prestamo__icontains = busqueda) 
        )
 # Configuración de la paginación
    paginator = Paginator(prestamos, 11)  # Muestra 10 libros por página
    page = request.GET.get('page')

    try:
        prestamos_paginados = paginator.page(page)
    except PageNotAnInteger:
        # Si la página no es un número entero, entrega la primera página.
        prestamos_paginados = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera de rango (por encima de la última), entrega la última página.
        prestamos_paginados = paginator.page(paginator.num_pages)

    return render(request, 'prestamos/index.html', {'prestamos': prestamos_paginados})

def nuevo_prestamo(request):
    formulario = PrestamoForm(request.POST or None, request.FILES or None)
    
    if formulario.is_valid():
        formulario.save()
        return redirect('prestamos')
    return render(request, 'prestamos/nuevo_prestamo.html', {'formulario': formulario,'mensaje':'OK'})

def editar_prestamo(request, id_prestamo):
    prestamo = Prestamo.objects.get(id_prestamo=id_prestamo)
    
    # Formatear las fechas
    fecha_devolucion_calculada = prestamo.fecha_devolucion_calculada.strftime("%Y-%m-%d")
    fecha_prestamo = prestamo.fecha_prestamo.strftime("%Y-%m-%d")

    # Establecer los valores originales del préstamo en el formulario
    formulario = PrestamoForm(
        request.POST or None,
        request.FILES or None,
        instance=prestamo,
        initial={
            'fecha_devolucion_calculada': fecha_devolucion_calculada,
            'fecha_prestamo': fecha_prestamo,
        }
    )

    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('prestamos')
    return render(request, 'prestamos/editar_prestamo.html', {'formulario':formulario})

def eliminar_prestamo(request, id_prestamo):
    prestamo = Prestamo.objects.get(id_prestamo=id_prestamo)
    prestamo.delete()
    return redirect('prestamos')

