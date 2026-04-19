from django.db import models
from rest_framework.exceptions import NotFound
from rota_expressa.models import Cidade


class CidadeService:
    @staticmethod
    def get_cidade_by_id(cidade_id: int) -> Cidade | None:
        return Cidade.objects.filter(id=cidade_id).first()

    @staticmethod
    def get_all_cidades() -> models.QuerySet[Cidade]:
        return Cidade.objects.all()
    
    @staticmethod
    def criar_cidade(dados_validados: dict) -> Cidade:
        return Cidade.objects.create(**dados_validados)
    
    @staticmethod
    def atualizar_cidade(cidade_id: int, dados_validados: dict) -> Cidade:
        cidade = Cidade.objects.filter(id=cidade_id).first()

        if not cidade:
            raise NotFound("Erro: Cidade não encontrada")

        for chave, valor in dados_validados.items():
            setattr(cidade, chave, valor)
        cidade.save()
        return cidade