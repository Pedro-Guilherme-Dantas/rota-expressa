from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny, IsAuthenticated
from rota_expressa.services.usuario_service import UsuarioService
from rota_expressa.serializers.usuario_serializer import (
    UsuarioSerializer, UsuarioResponseSerializer
)


class UsuarioViewSet(viewsets.ViewSet):
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    @extend_schema(
        summary="Lista os usuários",
        responses={200: UsuarioResponseSerializer(many=True)}
    )
    def list(self, request):
        usuarios = UsuarioService.get_all_usuarios()
        serializer = UsuarioResponseSerializer(
            usuarios, many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Cria um novo usuário",
        request=UsuarioSerializer,
        responses={201: UsuarioResponseSerializer}
    )
    def create(self, request):
        serializer = UsuarioSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        usuario = UsuarioService.criar_usuario(serializer.validated_data)
        response_serializer = UsuarioResponseSerializer(usuario)
        return Response(
            response_serializer.data, status=status.HTTP_201_CREATED
        )

    @extend_schema(
        summary="Recupera um usuário por ID",
        responses={200: UsuarioResponseSerializer, 404: "Not Found"}
    )
    def retrieve(self, request, pk=None):
        usuario = UsuarioService.get_usuario_by_id(pk)
        serializer = UsuarioResponseSerializer(usuario)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Atualiza um usuário por ID",
        request=UsuarioSerializer,
        responses={200: UsuarioResponseSerializer, 404: "Not Found"}
    )
    def update(self, request, pk=None):
        if str(request.user.id) != str(pk):
            return Response(
                {"detail": "Não autorizado"},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = UsuarioSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        usuario = UsuarioService.atualizar_usuario(
            pk, serializer.validated_data
        )
        response_serializer = UsuarioResponseSerializer(usuario)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Atualiza parcialmente um usuário por ID",
        request=UsuarioSerializer,
        responses={200: UsuarioResponseSerializer, 404: "Not Found"}
    )
    def partial_update(self, request, pk=None):
        if str(request.user.id) != str(pk):
            return Response(
                {"detail": "Não autorizado"},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = UsuarioSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        usuario = UsuarioService.atualizar_usuario(
            pk, serializer.validated_data
        )
        response_serializer = UsuarioResponseSerializer(usuario)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Deleta um usuário por ID",
        responses={204: "No Content", 404: "Not Found"}
    )
    def destroy(self, request, pk=None):
        if str(request.user.id) != str(pk):
            return Response(
                {"detail": "Não autorizado"},
                status=status.HTTP_403_FORBIDDEN
            )
        usuario = UsuarioService.get_usuario_by_id(pk)
        if not usuario:
            return Response(
                {"detail": "Erro: Usuário não encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )
        UsuarioService.delete_usuario(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
