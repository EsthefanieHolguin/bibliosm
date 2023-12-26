from typing import Any
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Libro(models.Model):
    CATEGORIAS_CHOICES = [
        ('novelas', 'Novelas'),
        ('suspenso', 'Suspenso'),
        ('historia', 'Historia'),
        ('test', 'Test'),
    ]

    isbn = models.CharField(primary_key=True, max_length=13)
    titulo = models.CharField(max_length=100, verbose_name='Título', null=False, blank=False)
    autor = models.CharField(max_length=100, verbose_name='Autor', null=False, blank=False)
    categoria = models.CharField(max_length=50, verbose_name='Categoría', choices=CATEGORIAS_CHOICES)
    ubicacion = models.CharField(max_length=20, verbose_name='Ubicación', null=False, blank=False)
    ejemplares_totales = models.IntegerField(default=0)
    ejemplares_disponibles = models.IntegerField(default=ejemplares_totales)
    ejemplares_prestados = models.IntegerField(default=0)
    ejemplares_reservados = models.IntegerField(default=0)
    descripcion = models.TextField(verbose_name='Descripción', null=True, blank=True)

    def __str__(self):
        return self.isbn

    def is_upperclass(self):
        return self.categoria in (choice[0] for choice in self.CATEGORIAS_CHOICES)

    def delete(self, using=None, keep_parents=False):

        #self.imagen.storage.delete(self.imagen.name)
        super().delete()

from appprestamos.models import Prestamo 
@receiver(pre_save, sender=Prestamo)
def actualizar_ejemplares_libro(sender, instance, **kwargs):
    libro = instance.isbn

    # Verificar si es un préstamo nuevo
    if instance._state.adding:
        # Restar 1 al número de ejemplares disponibles
        libro.ejemplares_disponibles -= 1
        # Sumar 1 al número de ejemplares prestados
        libro.ejemplares_prestados += 1
    else:
        # Verificar si se está finalizando un préstamo
        if instance.estado_prestamo == 'finalizado':
            # Sumar 1 al número de ejemplares disponibles
            libro.ejemplares_disponibles += 1
            # Restar 1 al número de ejemplares prestados
            libro.ejemplares_prestados -= 1

    # Guardar los cambios en el libro
    libro.save()
