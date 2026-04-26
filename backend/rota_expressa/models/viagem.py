from django.db import models
from rota_expressa.models.cidade import Cidade
from rota_expressa.models.motorista import Motorista
from rota_expressa.models.veiculo import Veiculo


class Viagem(models.Model):
    DIAS_SEMANA = [
        (0, 'Segunda-feira'),
        (1, 'Terça-feira'),
        (2, 'Quarta-feira'),
        (3, 'Quinta-feira'),
        (4, 'Sexta-feira'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]

    origem = models.ForeignKey(
        Cidade,
        on_delete=models.CASCADE,
        related_name='viagem_origem'
    )

    destino = models.ForeignKey(
        Cidade,
        on_delete=models.CASCADE,
        related_name='viagem_destino'
    )

    horario_partida = models.TimeField()
    horario_chegada = models.TimeField()
    dia_semana = models.IntegerField(choices=DIAS_SEMANA)
    valor = models.DecimalField(max_digits=8, decimal_places=2)

    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    motorista = models.ForeignKey(Motorista, on_delete=models.CASCADE)

    is_pet_friendly = models.BooleanField(default=False)
    is_acessivel = models.BooleanField(default=False)
    is_ativo = models.BooleanField(default=True)

    def __str__(self):
        msg = (
            f'Viagem de {self.origem} para {self.destino} em '
            f'{self.horario_partida:%H:%M} até '
            f'{self.horario_chegada:%H:%M} no dia '
            f'{self.DIAS_SEMANA[self.dia_semana][1]} com valor de R$ {self.valor}'
        )

        return msg
