from django.db.models import QuerySet
from rest_framework.exceptions import NotFound
from rota_expressa.models import Telefone


class TelefoneService:
    @staticmethod
    def get_telefone_by_numero(numero: str) -> Telefone | None:
        return Telefone.objects.filter(numero=numero).first()

    @staticmethod
    def get_all_telefones() -> QuerySet[Telefone]:
        return Telefone.objects.all()

    @staticmethod
    def criar_telefone(dados_validados: dict) -> Telefone:
        return Telefone.objects.create(**dados_validados)

    @staticmethod
    def atualizar_telefone(telefone_id: int, dados_validados: dict) -> Telefone:
        telefone = Telefone.objects.filter(id=telefone_id).first()

        if not telefone:
            raise NotFound("Erro: Telefone não encontrado")

        for chave, valor in dados_validados.items():
            setattr(telefone, chave, valor)
        telefone.save()
        return telefone

    @staticmethod
    def delete_telefone(telefone_id: int) -> None:
        telefone = Telefone.objects.filter(id=telefone_id).first()
        if not telefone:
            raise NotFound("Erro: Telefone não encontrado")

        telefone.delete()
        return
