from django import forms
from .models import Libro

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = '__all__'

    CATEGORIAS_CHOICES = [
        ('novelas', 'Novelas'),
        ('suspenso', 'Suspenso'),
        ('historia', 'Historia'),
        ('test', 'Test'),
    ]
        
    categoria = forms.ChoiceField(choices=CATEGORIAS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    