from django.db import models

class Pacientes(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome Completo")
    data_nascimento = models.DateField(verbose_name="Data de Nascimento")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name