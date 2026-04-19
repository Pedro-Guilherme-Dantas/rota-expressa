from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from django.db import models
from rota_expressa.models import Viagem
from rota_expressa.models import Cidade


class ViagemService:
    @staticmethod
    def get_viagem_by_id(viagem_id: int) -> Viagem | None:
        return Viagem.objects.filter(id=viagem_id).first()

    @staticmethod
    def get_all_viagens() -> models.QuerySet[Viagem]:
        return Viagem.objects.select_related('origem', 'destino', 'veiculo__modelo', 'motorista__usuario').all()

    @staticmethod
    def get_viagens_filtradas(origem=None, destino=None, horario=None, preco=None):
        queryset = Viagem.objects.select_related('origem', 'destino', 'veiculo__modelo', 'motorista__usuario').all()

        if origem:
            queryset = queryset.filter(origem_id=origem) 
            
        if destino:
            queryset = queryset.filter(destino_id=destino)
            
        if horario:
            # __gte = Maior ou igual (horários a partir do que o usuário digitou)
            queryset = queryset.filter(horario_partida__gte=horario)
            
        if preco:
            # __lte = Menor ou igual (preços até o limite que o usuário digitou)
            queryset = queryset.filter(valor__lte=preco)

        return queryset

    @staticmethod
    def processar_cidades_ibge(dados_brutos: dict) -> dict:
        """
        Intercepta os nomes das cidades vindos do front, verifica no banco 
        e devolve o dicionário com os IDs corretos para o Serializer validar.
        """
        dados = dados_brutos.copy()
        
        origem_nome = dados.pop('origem_nome', None)
        origem_estado = dados.pop('origem_estado', None)
        destino_nome = dados.pop('destino_nome', None)
        destino_estado = dados.pop('destino_estado', None)

        if not origem_nome or not destino_nome:
            raise ValidationError({"detail": "Origem e destino são obrigatórios."})

        # Cria ou busca as cidades no banco local
        cidade_origem, _ = Cidade.objects.get_or_create(nome=origem_nome, estado=origem_estado)
        cidade_destino, _ = Cidade.objects.get_or_create(nome=destino_nome, estado=destino_estado)

        # Injeta os IDs na cópia dos dados para que o Serializer fique feliz
        dados['origem'] = cidade_origem.id
        dados['destino'] = cidade_destino.id

        return dados

    @staticmethod
    def criar_viagem(dados_validados: dict, usuario) -> Viagem:
        """
        Cria a viagem aplicando a regra de negócio do motorista logado.
        """
        if not hasattr(usuario, 'perfil_motorista'):
            raise PermissionDenied("Apenas motoristas cadastrados podem criar viagens.")
            
        veiculo = dados_validados.get('veiculo')
        if veiculo and veiculo.motorista != usuario.perfil_motorista:
            raise PermissionDenied("Você não pode criar uma viagem com o veículo de outro motorista.")
        
        dados_validados['motorista'] = usuario.perfil_motorista

        return Viagem.objects.create(**dados_validados)

    @staticmethod
    def atualizar_viagem(viagem_id: int, dados_validados: dict) -> Viagem:
        viagem = Viagem.objects.filter(id=viagem_id).first()

        if not viagem:
            raise NotFound("Erro: Viagem não encontrada")

        for chave, valor in dados_validados.items():
            setattr(viagem, chave, valor)
        viagem.save()
        return viagem

    @staticmethod
    def delete_viagem(viagem_id: int) -> None:
        viagem = Viagem.objects.filter(id=viagem_id).first()
        if not viagem:
            raise NotFound("Erro: Viagem não encontrada")

        viagem.delete()
        return
