from django.db.models import QuerySet
from rest_framework.exceptions import NotFound
from rota_expressa.models import Usuario
from rota_expressa.models.motorista import Motorista


class UsuarioService:
    @staticmethod
    def get_usuario_by_username(username: str) -> Usuario | None:
        return Usuario.objects.filter(username=username).first()

    @staticmethod
    def get_all_usuarios() -> QuerySet[Usuario]:
        return Usuario.objects.all()

    @staticmethod
    def get_usuario_by_id(usuario_id: int) -> Usuario | None:
        return Usuario.objects.filter(id=usuario_id).first()

    @staticmethod
    def criar_usuario(dados_validados: dict) -> Usuario:
        is_motorista = dados_validados.pop('is_motorista', False)

        if is_motorista:
            dados_validados['is_active'] = False
            usuario = Usuario.objects.create_user(**dados_validados)
            Motorista.objects.create(usuario=usuario)
        else:
            usuario = Usuario.objects.create_user(**dados_validados)

        return usuario

    @staticmethod
    def atualizar_usuario(usuario_id: int, dados_validados: dict) -> Usuario:
        usuario = Usuario.objects.filter(id=usuario_id).first()

        if not usuario:
            raise NotFound("Erro: Usuário não encontrado")

        password = dados_validados.pop('password', None)

        if password:
            usuario.set_password(password)

        for chave, valor in dados_validados.items():
            setattr(usuario, chave, valor)
        usuario.save()
        return usuario

    @staticmethod
    def delete_usuario(usuario_id: int) -> None:
        usuario = Usuario.objects.filter(id=usuario_id).first()
        if not usuario:
            raise NotFound("Erro: Usuário não encontrado")

        usuario.delete()
        return
