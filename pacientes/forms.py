from django import forms
from .models import Pacientes

class PacientesForm(forms.ModelForm):
    class Meta:
        model = Pacientes
        fields = ['name', 'data_nascimento']
        widgets = {
            'name': forms.TextInput(attrs={
                'id': 'name',
                'placeholder': 'Digite o nome completo do paciente',
                'class': 'form-control',
            }),
            'data_nascimento': forms.DateInput(attrs={
                'id': 'dataNascimento',
                'type': 'date',
                'class': 'form-control',
            }),
        }
        labels ={
            'name': 'Nome Completo',
            'data_nascimento': 'Data de Nascimento'
        }