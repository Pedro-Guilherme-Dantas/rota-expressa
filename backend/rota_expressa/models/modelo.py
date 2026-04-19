from django.db import models
from django.core.validators import MinLengthValidator
from django.core.validators import MinValueValidator


class Modelo(models.Model):
    nome = models.CharField(
        max_length=60,
        unique=True,
        validators=[MinLengthValidator(1)]
        )

    ano = models.IntegerField()
    qtd_lugares = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.nome} ({self.ano})"
