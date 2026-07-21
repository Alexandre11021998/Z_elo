from django.core.exceptions import ValidationError
from datetime import date

def validate_data_nascimento(value):
    """Confere regras de validação"""
    if value:
        if value.year < 1900:
            raise ValidationError('Ano de nascimento inválido.')
        if value > date.today():
            raise ValidationError('Data de nascimento inválida')