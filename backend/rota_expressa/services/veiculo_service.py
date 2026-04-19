import re
from django.db import models
from rest_framework.exceptions import NotFound, PermissionDenied
from rota_expressa.models import Veiculo


class VeiculoService:
    @staticmethod
    def validar_e_limpar_placa(placa: str) -> str:
        placa_limpa = re.sub(r'[^A-Z0-9]', '', placa.upper())
        padrao = re.compile(r'^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$')

        if not padrao.match(placa_limpa):
            raise ValueError("Formato de placa inválido.")
        return placa_limpa

    @staticmethod
    def get_veiculo_by_id(veiculo_id: int) -> Veiculo | None:
        return Veiculo.objects.filter(id=veiculo_id).first()

    @staticmethod
    def get_veiculo_by_placa(placa: str) -> Veiculo | None:
        return Veiculo.objects.filter(placa=placa).first()

    @staticmethod
    def get_all_veiculos() -> models.QuerySet[Veiculo]:
        return Veiculo.objects.all()

    @staticmethod
    def criar_veiculo(dados_validados: dict, usuario) -> Veiculo:
        if not hasattr(usuario, 'perfil_motorista'):
            raise PermissionDenied("Apenas motoristas podem cadastrar veículos.")
            
        dados_validados['motorista'] = usuario.perfil_motorista
        return Veiculo.objects.create(**dados_validados)

    @staticmethod
    def atualizar_veiculo(veiculo_id: int, dados_validados: dict) -> Veiculo:
        veiculo = Veiculo.objects.filter(id=veiculo_id).first()

        if dados_validados.get('placa'):
            dados_validados['placa'] = VeiculoService.validar_e_limpar_placa(
                dados_validados['placa']
                )

        if not veiculo:
            raise NotFound("Erro: Veículo não encontrado")

        for chave, valor in dados_validados.items():
            setattr(veiculo, chave, valor)
        veiculo.save()
        return veiculo

    @staticmethod
    def delete_veiculo(veiculo_id: int) -> None:
        veiculo = Veiculo.objects.filter(id=veiculo_id).first()
        if not veiculo:
            raise NotFound("Erro: Veículo não encontrado")

        veiculo.delete()
        return
