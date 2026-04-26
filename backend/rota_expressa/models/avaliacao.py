from django.db import models
from rota_expressa.models.motorista import Motorista
from rota_expressa.models.usuario import Usuario


class Avaliacao(models.Model):
    motorista = models.ForeignKey(
        Motorista,
        on_delete=models.CASCADE,
        related_name='avaliacoes'
    )

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='avaliacoes_feitas'
    )

    NOTAS_CHOICES = [(i, str(i)) for i in range(1, 6)]
    nota = models.IntegerField(choices=NOTAS_CHOICES)
    comentario = models.TextField(max_length=500, blank=True)
    data_avaliacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        msg = (
            f'Avaliação de {self.usuario.username} para '
            f'{self.motorista.usuario.first_name} - Nota: {self.nota}'
        )

        return msg
