from django.db import models
from .validators import validate_data_nascimento

class Pacientes(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome Completo")
    data_nascimento = models.DateField(verbose_name="Data de Nascimento", validators=[validate_data_nascimento]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name