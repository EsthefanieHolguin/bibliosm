from django.db import models
from typing import Any

# Create your models here.

class Usuario(models.Model):

    rut_usuario = models.CharField(primary_key=True,max_length=9,)
    nombre_usuario = models.CharField(max_length=100, verbose_name='Nombre', null=False, blank=False)
    email = models.EmailField(max_length=120, verbose_name='Email', null=False, blank=False)
    curso = models.CharField(max_length=20, verbose_name='Curso', null=False, blank=False)

    def __str__(self):
        fila = self.rut_usuario 
        return fila

    class Meta:
        verbose_name = "Datos_Usuarios"