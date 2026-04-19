import pytest
from rest_framework.test import APIClient
from rota_expressa.tests.factories import UsuarioFactory, MotoristaFactory


@pytest.mark.django_db
class TestRegistroELogin:
    """Testes do fluxo de cadastro e autenticação JWT."""

    def test_registro_usuario_sem_token(self):
        """POST /api/usuarios/ deve funcionar sem autenticação (AllowAny)."""
        client = APIClient()
        payload = {
            'username': 'novo_user',
            'email': 'novo@teste.com',
            'first_name': 'Novo',
            'last_name': 'User',
            'password': 'senha12345',
        }
        response = client.post('/api/usuarios/', payload, format='json')
        assert response.status_code == 201
        assert response.data['username'] == 'novo_user'
        # Senha nunca deve vazar na resposta
        assert 'password' not in response.data

    def test_registro_rejeita_senha_curta(self):
        """Serializer deve rejeitar senha com menos de 8 caracteres."""
        client = APIClient()
        payload = {
            'username': 'curto',
            'email': 'curto@teste.com',
            'first_name': 'Curto',
            'last_name': 'Pwd',
            'password': '123',
        }
        response = client.post('/api/usuarios/', payload, format='json')
        assert response.status_code == 400

    def test_login_retorna_tokens(self):
        """POST /api/token/ deve retornar access e refresh tokens."""
        UsuarioFactory(username='loginuser', email='login@teste.com')
        client = APIClient()
        response = client.post('/api/token/', {
            'username': 'loginuser',
            'password': 'senha12345',
        }, format='json')
        assert response.status_code == 200
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_endpoint_protegido_rejeita_anonimo(self):
        """GET /api/me/ deve retornar 401 sem token."""
        client = APIClient()
        response = client.get('/api/me/')
        assert response.status_code == 401

    def test_me_retorna_usuario_logado(self):
        """GET /api/me/ deve retornar os dados do dono do token."""
        user = UsuarioFactory(username='meuser')
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get('/api/me/')
        assert response.status_code == 200
        assert response.data['username'] == 'meuser'


@pytest.mark.django_db
class TestBOLAUsuarios:
    """Testes de Broken Object Level Authorization nas rotas de usuário."""

    def test_usuario_nao_pode_editar_outro(self):
        """PATCH /api/usuarios/{outro_id}/ deve retornar 403."""
        user_a = UsuarioFactory()
        user_b = UsuarioFactory()
        client = APIClient()
        client.force_authenticate(user=user_a)
        response = client.patch(
            f'/api/usuarios/{user_b.id}/',
            {'first_name': 'Hacker'},
            format='json',
        )
        assert response.status_code == 403

    def test_usuario_pode_editar_a_si_mesmo(self):
        """PATCH /api/usuarios/{proprio_id}/ deve retornar 200."""
        user = UsuarioFactory()
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.patch(
            f'/api/usuarios/{user.id}/',
            {'first_name': 'Atualizado'},
            format='json',
        )
        assert response.status_code == 200
        assert response.data['first_name'] == 'Atualizado'


@pytest.mark.django_db
class TestMotoristas:
    """Testes de criação e BOLA no perfil de motorista."""

    def test_criacao_motorista_injeta_usuario_logado(self):
        """POST /api/motoristas/ deve vincular o perfil ao request.user."""
        user = UsuarioFactory()
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post(
            '/api/motoristas/',
            {'resumo': 'Sou motorista experiente.'},
            format='json',
        )
        assert response.status_code == 201
        assert response.data['usuario']['id'] == user.id

    def test_motorista_nao_pode_editar_perfil_alheio(self):
        """PATCH /api/motoristas/{outro_id}/ deve retornar 403."""
        motorista_a = MotoristaFactory()
        motorista_b = MotoristaFactory()
        client = APIClient()
        client.force_authenticate(user=motorista_a.usuario)
        response = client.patch(
            f'/api/motoristas/{motorista_b.id}/',
            {'resumo': 'Invadido'},
            format='json',
        )
        assert response.status_code == 403
