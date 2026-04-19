from django.db import models
from rota_expressa.models.modelo import Modelo
from rota_expressa.models.motorista import Motorista
from django.core.validators import MinLengthValidator


class Veiculo(models.Model):
    CORES = [
        ('AMARELO', 'Amarelo'),
        ('AZUL', 'Azul'),
        ('BEGE', 'Bege'),
        ('BRANCO', 'Branco'),
        ('CINZA', 'Cinza'),
        ('DOURADO', 'Dourado'),
        ('GRENA', 'Grená'),
        ('LARANJA', 'Laranja'),
        ('MARROM', 'Marrom'),
        ('PRATA', 'Prata'),
        ('PRETO', 'Preto'),
        ('ROSA', 'Rosa'),
        ('ROXO', 'Roxo'),
        ('VERDE', 'Verde'),
        ('VERMELHO', 'Vermelho'),
    ]

    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE)
    placa = models.CharField(
        max_length=7,
        unique=True,
        validators=[MinLengthValidator(
            7, message="A placa deve ter exatamente 7 caracteres."
            )]
        )

    cor = models.CharField(max_length=30, choices=CORES)
    motorista = models.ForeignKey(Motorista, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.modelo.nome} {self.modelo.nome} - {self.placa}"
