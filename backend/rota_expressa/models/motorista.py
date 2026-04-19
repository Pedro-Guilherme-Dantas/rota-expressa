from django.db import models
from rota_expressa.models.usuario import Usuario


class Motorista(models.Model):
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='perfil_motorista'
        )

    nota_media = models.FloatField(default=0.0)
    resumo = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f"Motorista: {self.usuario.first_name}"