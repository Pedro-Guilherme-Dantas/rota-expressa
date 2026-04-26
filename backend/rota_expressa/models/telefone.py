from django.db import models
from django.core.validators import MinLengthValidator
from rota_expressa.models.usuario import Usuario


class Telefone(models.Model):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='telefones'
    )

    numero = models.CharField(
        max_length=11,
        unique=True,
        validators=[MinLengthValidator(11)]
    )

    def __str__(self):
        return f"{self.numero} ({self.usuario.username})"
