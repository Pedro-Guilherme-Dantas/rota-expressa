import pytest
from rest_framework.test import APIClient
from rota_expressa.models import Avaliacao
from rota_expressa.services.viagem_service import ViagemService
from rota_expressa.tests.factories import (
    UsuarioFactory, MotoristaFactory, CidadeFactory,
    VeiculoFactory, ViagemFactory, ModeloFactory,
)


@pytest.mark.django_db
class TestCriacaoViagem:
    """Testes do fluxo de criação de viagem e suas regras de negócio."""

    def test_criar_viagem_com_get_or_create_cidade(self):
        """processar_cidades_ibge deve criar cidades automaticamente."""
        dados = {
            'origem_nome': 'Cidade Nova A',
            'origem_estado': 'MG',
            'destino_nome': 'Cidade Nova B',
            'destino_estado': 'RJ',
            'horario_partida': '08:00',
            'horario_chegada': '10:00',
            'dia_semana': '0',
            'valor': '50.00',
            'veiculo': '1',
        }
        resultado = ViagemService.processar_cidades_ibge(dados)
        assert 'origem' in resultado
        assert 'destino' in resultado
        # Não deve mais conter as chaves de nome
        assert 'origem_nome' not in resultado
        assert 'destino_nome' not in resultado

    def test_criar_viagem_rejeita_origem_igual_destino(self):
        """Serializer deve rejeitar viagem com origem == destino."""
        motorista = MotoristaFactory()
        veiculo = VeiculoFactory(motorista=motorista)
        cidade = CidadeFactory()

        client = APIClient()
        client.force_authenticate(user=motorista.usuario)
        payload = {
            'origem_nome': cidade.nome,
            'origem_estado': cidade.estado,
            'destino_nome': cidade.nome,
            'destino_estado': cidade.estado,
            'horario_partida': '08:00',
            'horario_chegada': '10:00',
            'dia_semana': 0,
            'valor': '50.00',
            'veiculo': veiculo.id,
            'is_pet_friendly': False,
            'is_acessivel': False,
            'is_ativo': True,
        }
        response = client.post('/api/viagens/', payload, format='json')
        assert response.status_code == 400

    def test_criar_viagem_rejeita_passageiro(self):
        """Usuário sem perfil de motorista deve receber 403."""
        passageiro = UsuarioFactory()
        veiculo = VeiculoFactory()
        origem = CidadeFactory(nome='Origem Test')
        destino = CidadeFactory(nome='Destino Test')

        client = APIClient()
        client.force_authenticate(user=passageiro)
        payload = {
            'origem_nome': origem.nome,
            'origem_estado': origem.estado,
            'destino_nome': destino.nome,
            'destino_estado': destino.estado,
            'horario_partida': '08:00',
            'horario_chegada': '10:00',
            'dia_semana': 0,
            'valor': '50.00',
            'veiculo': veiculo.id,
            'is_pet_friendly': False,
            'is_acessivel': False,
            'is_ativo': True,
        }
        response = client.post('/api/viagens/', payload, format='json')
        assert response.status_code == 403

    def test_criar_viagem_rejeita_veiculo_de_outro(self):
        """BOLA: usar veículo de outro motorista deve retornar 403."""
        motorista_a = MotoristaFactory()
        motorista_b = MotoristaFactory()
        veiculo_b = VeiculoFactory(motorista=motorista_b)
        origem = CidadeFactory(nome='Origem BOLA')
        destino = CidadeFactory(nome='Destino BOLA')

        client = APIClient()
        client.force_authenticate(user=motorista_a.usuario)
        payload = {
            'origem_nome': origem.nome,
            'origem_estado': origem.estado,
            'destino_nome': destino.nome,
            'destino_estado': destino.estado,
            'horario_partida': '08:00',
            'horario_chegada': '10:00',
            'dia_semana': 0,
            'valor': '50.00',
            'veiculo': veiculo_b.id,
            'is_pet_friendly': False,
            'is_acessivel': False,
            'is_ativo': True,
        }
        response = client.post('/api/viagens/', payload, format='json')
        assert response.status_code == 403

    def test_criar_viagem_sucesso(self):
        """Fluxo completo de criação de viagem deve retornar 201."""
        motorista = MotoristaFactory()
        veiculo = VeiculoFactory(motorista=motorista)
        origem = CidadeFactory(nome='Campinas')
        destino = CidadeFactory(nome='São Paulo')

        client = APIClient()
        client.force_authenticate(user=motorista.usuario)
        payload = {
            'origem_nome': origem.nome,
            'origem_estado': origem.estado,
            'destino_nome': destino.nome,
            'destino_estado': destino.estado,
            'horario_partida': '08:00',
            'horario_chegada': '10:00',
            'dia_semana': 0,
            'valor': '50.00',
            'veiculo': veiculo.id,
            'is_pet_friendly': True,
            'is_acessivel': False,
            'is_ativo': True,
        }
        response = client.post('/api/viagens/', payload, format='json')
        assert response.status_code == 201
        assert response.data['origem'] == 'Campinas'
        assert response.data['destino'] == 'São Paulo'
        assert response.data['is_pet_friendly'] is True


@pytest.mark.django_db
class TestFiltroViagens:
    """Testes dos filtros de busca do mural de viagens."""

    def test_filtro_viagens_por_origem(self):
        """GET /api/viagens/?origem=X deve retornar apenas viagens daquela cidade."""
        cidade_a = CidadeFactory(nome='Filtro A')
        cidade_b = CidadeFactory(nome='Filtro B')
        motorista = MotoristaFactory()
        veiculo = VeiculoFactory(motorista=motorista)

        ViagemFactory(
            origem=cidade_a,
            destino=cidade_b,
            veiculo=veiculo,
            motorista=motorista
        )
        ViagemFactory(
            origem=cidade_b,
            destino=cidade_a,
            veiculo=veiculo,
            motorista=motorista
        )

        client = APIClient()
        client.force_authenticate(user=motorista.usuario)
        response = client.get(f'/api/viagens/?origem={cidade_a.id}')
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['origem'] == 'Filtro A'


@pytest.mark.django_db
class TestVeiculos:
    """Testes de criação de veículos e injeção de motorista."""

    def test_criar_veiculo_injeta_motorista_logado(self):
        """POST /api/veiculos/ deve associar ao motorista do token."""
        motorista = MotoristaFactory()
        modelo = ModeloFactory()
        client = APIClient()
        client.force_authenticate(user=motorista.usuario)
        response = client.post('/api/veiculos/', {
            'modelo': modelo.id,
            'placa': 'ABC1D23',
            'cor': 'PRETO',
        }, format='json')
        assert response.status_code == 201
        assert response.data['motorista'] == str(motorista)

    def test_criar_veiculo_rejeita_passageiro(self):
        """Usuário sem perfil de motorista deve receber 403."""
        passageiro = UsuarioFactory()
        modelo = ModeloFactory()
        client = APIClient()
        client.force_authenticate(user=passageiro)
        response = client.post('/api/veiculos/', {
            'modelo': modelo.id,
            'placa': 'XYZ9A87',
            'cor': 'BRANCO',
        }, format='json')
        assert response.status_code == 403


@pytest.mark.django_db
class TestSignalAvaliacao:
    """Testes do signal que recalcula a nota_media do motorista."""

    def test_signal_atualiza_nota_media(self):
        """Ao criar e deletar avaliações, a nota_media do motorista deve ser recalculada."""
        motorista = MotoristaFactory()
        avaliador_1 = UsuarioFactory()
        avaliador_2 = UsuarioFactory()

        av1 = Avaliacao.objects.create(
            motorista=motorista, usuario=avaliador_1, nota=4)
        Avaliacao.objects.create(
            motorista=motorista,
            usuario=avaliador_2,
            nota=2
        )
        motorista.refresh_from_db()
        assert motorista.nota_media == 3.0

        av1.delete()
        motorista.refresh_from_db()
        assert motorista.nota_media == 2.0
