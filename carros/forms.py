from django import forms
from .models import Inspecao

class InspecaoForm(forms.ModelForm):
    class Meta:
        model = Inspecao
        fields = ['data_inspecao', 'observacoes', 'status']
