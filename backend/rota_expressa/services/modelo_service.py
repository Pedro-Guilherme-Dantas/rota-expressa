from django.db import models
from rest_framework.exceptions import NotFound
from rota_expressa.models import Modelo


class ModeloService:
    @staticmethod
    def get_modelo_by_nome(nome: str) -> Modelo | None:
        return Modelo.objects.filter(nome=nome).first()

    @staticmethod
    def get_all_modelos() -> models.QuerySet[Modelo]:
        return Modelo.objects.all()

    @staticmethod
    def criar_modelo(dados_validados: dict) -> Modelo:
        return Modelo.objects.create(**dados_validados)

    @staticmethod
    def atualizar_modelo(modelo_id: int, dados_validados: dict) -> Modelo:
        modelo = Modelo.objects.filter(id=modelo_id).first()

        if not modelo:
            raise NotFound("Erro: Modelo não encontrado")

        for chave, valor in dados_validados.items():
            setattr(modelo, chave, valor)
        modelo.save()
        return modelo

    @staticmethod
    def delete_modelo(modelo_id: int) -> None:
        modelo = Modelo.objects.filter(id=modelo_id).first()
        if not modelo:
            raise NotFound("Erro: Modelo não encontrado")

        modelo.delete()
        return
