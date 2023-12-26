from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponse
from django.db.models import Q
from .models import Libro
from .forms import LibroForm

# Acá creamos las funciones para acceder a las vistas HTML

def inicio(request):
    return render(request, 'paginas/inicio.html')
def nosotros(request):
    return render(request, 'paginas/nosotros.html')


def catalogo(request):  #Listar libros y barra busqueda en el catalogo (para el usuario que reserve)
    busqueda = request.GET.get("buscar")
    libros = Libro.objects.all()

    #querys con la busqueda, que se obtiene del input name del index.html
    if busqueda:
        libros = Libro.objects.filter(
            Q(titulo__icontains = busqueda) |
            Q(autor__icontains = busqueda) |
            Q(isbn = busqueda) |
            Q(categoria__icontains = busqueda)
        ).distinct()
    return render(request, 'paginas/catalogo.html', {'libros': libros})



@login_required
def libros(request):  #Listar libros y barra busqueda para bibliotecario
    busqueda = request.GET.get("buscar")
    libros = Libro.objects.all()

    # Ordena los libros por título
    libros = libros.order_by('titulo')

    #querys con la busqueda, que se obtiene del input name del index.html
    if busqueda:
        libros = Libro.objects.filter(
            Q(titulo__icontains = busqueda) |
            Q(autor__icontains = busqueda) |
            Q(isbn = busqueda) |
            Q(categoria__icontains = busqueda)
        ).distinct()

    # Configuración de la paginación
    paginator = Paginator(libros, 10)  # Muestra 10 libros por página
    page = request.GET.get('page')

    try:
        libros_paginados = paginator.page(page)
    except PageNotAnInteger:
        # Si la página no es un número entero, entrega la primera página.
        libros_paginados = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera de rango (por encima de la última), entrega la última página.
        libros_paginados = paginator.page(paginator.num_pages)

    return render(request, 'libros/index.html', {'libros': libros_paginados})

def crear(request):
    formulario = LibroForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('libros')
    return render(request, 'libros/crear.html', {'formulario': formulario})

def editar(request,isbn):
    libro = Libro.objects.get(isbn=isbn)
    formulario = LibroForm(request.POST or None, request.FILES or None, instance=libro)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('libros')
    return render(request, 'libros/editar.html', {'formulario':formulario})

def eliminar(request, isbn):
    libro = Libro.objects.get(isbn=isbn)
    libro.delete()
    return redirect('libros')

def subir_csv(request):
    template_name = "libros/upload_csv.html"

    if request.method == "POST":
        csv_file = request.FILES["csv_file"]

        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")

        # Omitir la primera línea (cabecera)
        header_skipped = False

        for line in lines:

            # Omitir la primera línea (cabecera)
            if not header_skipped:
                header_skipped = True
                continue

            fields = line.split(",")
            if len(fields)>1:
                data_dict = {}
                data_dict ["isbn"] = fields[0]
                data_dict ["titulo"] = fields[1]
                data_dict ["autor"] = fields[2]
                data_dict ["categoria"] = fields[3]
                data_dict ["ubicacion"] = fields[4]
                data_dict ["ejemplares_totales"] = fields[5]
                data_dict ["ejemplares_disponibles"] = fields[6]
                data_dict ["ejemplares_prestados"] = fields[7]
                data_dict ["ejemplares_reservados"] = fields[8]
                data_dict ["descripcion"] = fields[9]

                try:
                    form = LibroForm(data_dict)
                    if form.is_valid():
                        form.save()
                    else:
                        print (form.errors.as_json(),data_dict["titulo"])
                except Exception as ex:
                    print(repr(ex))
        return redirect('libros')

    return render(request,template_name,{})

def exit(request):
    logout(request)
    return redirect('inicio')
