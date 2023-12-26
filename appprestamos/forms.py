#encoding:utf-8
from django import forms
from .models import Prestamo


class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = '__all__'

    ESTADOS_CHOICE =[
        ('vigente','Préstamo Vigente'),
        ('finalizado','Préstamo Finalizado'),
        ('atrasado','Devolución Atrasada'),
    ]

    widgets = {
        'estado_prestamo': forms.Select(attrs={'class': 'regDropDown'}),
        'fecha_devolucion_real': forms.DateInput(attrs={'type': 'date'}),
    }
            
    estado_prestamo = forms.ChoiceField(choices=ESTADOS_CHOICE, widget=forms.Select(attrs={'class': 'form-control'}))


   
