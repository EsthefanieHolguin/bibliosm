from django.db import models
from typing import Any
from appejemplares.models import Libro
from appusuarios.models import Usuario

# Create your models here.
class Reserva(models.Model):

    id_reserva = models.AutoField(primary_key=True)
    fecha_reserva = models.DateField(auto_now_add=True)
    isbn = models.ForeignKey(Libro, on_delete=models.CASCADE,null=False,blank=False)
    rut = models.ForeignKey(Usuario, on_delete=models.CASCADE,null=False,blank=False)


    def __str__(self):
        fila = "ID Reserva: " + self.id_reserva
        return fila

    class Meta:
        verbose_name = "Datos_Reservas"