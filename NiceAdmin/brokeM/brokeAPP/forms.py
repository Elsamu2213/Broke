# forms.py
from django import forms
from .models import Tarea


class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['descripcion', 'fecha_vencimiento', 'direccion', 'actividad']  # Asegúrate de incluir fecha_vencimiento