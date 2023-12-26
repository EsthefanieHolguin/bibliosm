from typing import Any
from django.db import models
from django.utils.translation import gettext_lazy as _
from appejemplares.models import Libro
from appusuarios.models import Usuario
from datetime import date, timedelta
from django.dispatch import receiver
from django.db.models.signals import pre_save

def fecha_hoy():
    # Obtener la fecha actual
    fecha =  date.today()
    # Formatear la fecha en el formato "yyyy-mm-dd"
    fecha_formateada = fecha.strftime("%Y-%m-%d")
    
    return fecha_formateada

def fecha_devolucion():
    # Obtener la fecha actual y sumar 7 días
    fecha_calculada = date.today() + timedelta(days=7)
    # Formatear la fecha en el formato "yyyy-mm-dd"
    fecha_cal_formateada = fecha_calculada.strftime("%Y-%m-%d")

    return fecha_cal_formateada
class Prestamo(models.Model):
    ESTADOS_CHOICE =[
    ('vigente','Préstamo Vigente'),
    ('finalizado','Préstamo Finalizado'),
    ('atrasado','Devolución Atrasada'),
]
    
    id_prestamo = models.AutoField(primary_key=True)
    isbn = models.ForeignKey(Libro, on_delete=models.CASCADE,null=False,blank=False)
    rut_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE,null=False,blank=False)
    fecha_prestamo = models.DateField(null=False,blank=False,default=fecha_hoy)
    fecha_devolucion_calculada = models.DateField(null=False,blank=False, default=fecha_devolucion)
    fecha_devolucion_real = models.DateField(null=True,blank=True, default=''
                                             )
    estado_prestamo = models.CharField(max_length=50,choices=ESTADOS_CHOICE,default='vigente') #0=Préstamo Vigente, 1=Préstamo Finalizado 2=Devolución Atrasada 

    def __str__(self):
        fila = "ID Préstamo: " + self.id_prestamo + "Isbn: " + self.isbn + "Rut Usuario: " + self.rut_usuario + "Fecha Préstamo: " + self.fecha_prestamo + "Fecha Devolución: " + self.fecha_prestamo + "Fecha Préstamo: " + self.fecha_prestamo 

        return fila

    class Meta:
        verbose_name = "Datos_Prestamos"

@receiver(pre_save, sender=Prestamo)
def actualizar_fecha_devolucion_real(sender, instance, **kwargs):
    # Verificar si el estado del préstamo es "finalizado"
    if instance.estado_prestamo == 'finalizado':
        # Actualizar la fecha_devolucion_real con la fecha actual
        instance.fecha_devolucion_real = date.today()
    else:
        # Si el estado no es "finalizado", la fecha_devolucion_real será nulo
        instance.fecha_devolucion_real = None