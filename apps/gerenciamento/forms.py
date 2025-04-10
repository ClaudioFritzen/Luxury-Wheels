from django import forms
from gerenciamento.models import Inspecao

class InspecaoForm(forms.ModelForm):
    class Meta:
        model = Inspecao
        fields = ['data_ultima_inspecao','data_proxima_revisao', 'data_proxima_inspecao_obrigatoria', 'observacoes', 'status']
