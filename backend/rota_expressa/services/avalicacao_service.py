from rest_framework.exceptions import NotFound
from django.db import models
from rota_expressa.models import Avaliacao


class AvaliacaoService:
    @staticmethod
    def get_avaliacao_by_id(avaliacao_id: int) -> Avaliacao | None:
        return Avaliacao.objects.filter(id=avaliacao_id).first()

    @staticmethod
    def get_all_avaliacoes() -> models.QuerySet[Avaliacao]:
        return Avaliacao.objects.all()

    @staticmethod
    def criar_avaliacao(dados_validados: dict) -> Avaliacao:
        return Avaliacao.objects.create(**dados_validados)

    @staticmethod
    def atualizar_avaliacao(avaliacao_id: int, dados_validados: dict) -> Avaliacao:
        avaliacao = Avaliacao.objects.filter(id=avaliacao_id).first()

        if not avaliacao:
            raise NotFound("Erro: Avaliação não encontrada")

        for chave, valor in dados_validados.items():
            setattr(avaliacao, chave, valor)
        avaliacao.save()
        return avaliacao

    @staticmethod
    def delete_avaliacao(avaliacao_id: int) -> None:
        avaliacao = Avaliacao.objects.filter(id=avaliacao_id).first()
        if not avaliacao:
            raise NotFound("Erro: Avaliação não encontrada")

        avaliacao.delete()
        return
