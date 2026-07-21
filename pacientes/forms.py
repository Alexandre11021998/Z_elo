from django import forms
from .models import Pacientes

class PacientesForm(forms.ModelForm):
    data_nascimento = forms.DateField(
        label='Data de Nascimento',
        input_formats=['%d/%m/%Y', '%Y-%m-%d'],
        widget=forms.DateInput(
            format='%d/%m/%Y',
            attrs={
                'id': 'dataNascimento',
                'type': 'text',
                'inputmode': 'numeric',
                'placeholder': 'DD/MM/AAAA',
                'maxLength': '10',
                'class': 'form-control',
            }

        ),
        error_messages={
            'invalid': 'Data de nascimento inválida. Use o formato DD/MM/AAAA.',
        }
    )
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