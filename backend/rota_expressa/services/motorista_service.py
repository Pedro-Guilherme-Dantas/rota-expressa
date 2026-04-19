from rest_framework.exceptions import NotFound
from django.db import models
from rota_expressa.models import Motorista


class MotoristaService:
    @staticmethod
    def get_motorista_by_id(motorista_id: int) -> Motorista | None:
        return Motorista.objects.filter(id=motorista_id).first()

    @staticmethod
    def get_all_motoristas() -> models.QuerySet[Motorista]:
        return Motorista.objects.all()

    @staticmethod
    def criar_motorista(dados_validados: dict) -> Motorista:
        return Motorista.objects.create(**dados_validados)

    @staticmethod
    def atualizar_motorista(motorista_id: int, dados_validados: dict) -> Motorista:
        motorista = Motorista.objects.filter(id=motorista_id).first()

        if not motorista:
            raise NotFound("Erro: Motorista não encontrado")

        for chave, valor in dados_validados.items():
            setattr(motorista, chave, valor)
        motorista.save()
        return motorista

    @staticmethod
    def delete_motorista(motorista_id: int) -> None:
        motorista = Motorista.objects.filter(id=motorista_id).first()
        if not motorista:
            raise NotFound("Erro: Motorista não encontrado")

        motorista.delete()
        return
