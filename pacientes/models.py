from django.db import models
from .validators import validate_data_nascimento

class Pacientes(models.Model):
    STATUS_CHOICES = [
        ('aguardando', 'Aguardando'),
        ('em_preparacao', 'Em Preparação'),
        ('em_procedimento', 'Em Procedimento'),
        ('recuperacao_pos_anestesica', 'Recuperação Pos-Anestésica'),
        ('no_quarto', 'No Quarto'),
        ('em_alta', 'Em Alta'),
    ]

    STATUS_ORDER = [choice[0] for choice in STATUS_CHOICES
                    ]
    name = models.CharField(max_length=100, verbose_name="Nome Completo")
    data_nascimento = models.DateField(
        verbose_name="Data de Nascimento",
        validators=[validate_data_nascimento]
        )
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='Aguardando'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def current_step_index(self):
        """Retornar ao passo atual (0 a 5)"""
        try:
            return self.STATUS_ORDER.index(self.status)
        except ValueError:
            return 0

    @property
    def progress_percentage(self):
        """Calcula o pprogresso"""
        total_steps = len(self.STATUS_ORDER) - 1
        if total_steps <= 0:
            return 0
        return int((self.current_step_index / total_steps) * 100)
        