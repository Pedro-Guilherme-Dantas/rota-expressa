from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rota_expressa.services.motorista_service import MotoristaService
from rota_expressa.serializers.motorista_serializer import (
    MotoristaSerializer, MotoristaResponseSerializer
)


class MotoristaViewSet(viewsets.ViewSet):
    @extend_schema(
        summary="Lista os motoristas",
        responses={200: MotoristaResponseSerializer(many=True)}
    )
    def list(self, request):
        motoristas = MotoristaService.get_all_motoristas()
        serializer = MotoristaResponseSerializer(
            motoristas, many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Cria um novo motorista",
        request=MotoristaSerializer,
        responses={201: MotoristaResponseSerializer}
    )
    def create(self, request):
        serializer = MotoristaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['usuario'] = request.user
        motorista = MotoristaService.criar_motorista(serializer.validated_data)
        response_serializer = MotoristaResponseSerializer(motorista)
        return Response(
            response_serializer.data, status=status.HTTP_201_CREATED
        )

    @extend_schema(
        summary="Recupera um motorista por ID",
        responses={200: MotoristaResponseSerializer, 404: "Not Found"}
    )
    def retrieve(self, request, pk=None):
        motorista = MotoristaService.get_motorista_by_id(pk)
        serializer = MotoristaResponseSerializer(motorista)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Atualiza um motorista por ID",
        request=MotoristaSerializer,
        responses={200: MotoristaResponseSerializer, 404: "Not Found"}
    )
    def update(self, request, pk=None):
        if not hasattr(request.user, 'perfil_motorista') or str(
                request.user.perfil_motorista.id) != str(pk):
            return Response(
                {"detail": "Não autorizado"},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = MotoristaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        motorista = MotoristaService.atualizar_motorista(
            pk, serializer.validated_data
        )
        response_serializer = MotoristaResponseSerializer(motorista)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Atualiza parcialmente um motorista por ID",
        request=MotoristaSerializer,
        responses={200: MotoristaResponseSerializer, 404: "Not Found"}
    )
    def partial_update(self, request, pk=None):
        if not hasattr(request.user, 'perfil_motorista') or str(
                request.user.perfil_motorista.id) != str(pk):
            return Response(
                {"detail": "Não autorizado"},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = MotoristaSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        motorista = MotoristaService.atualizar_motorista(
            pk, serializer.validated_data
        )
        response_serializer = MotoristaResponseSerializer(motorista)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Deleta um motorista por ID",
        responses={204: "No Content", 404: "Not Found"}
    )
    def destroy(self, request, pk=None):
        if not hasattr(request.user, 'perfil_motorista') or str(
                request.user.perfil_motorista.id) != str(pk):
            return Response(
                {"detail": "Não autorizado"},
                status=status.HTTP_403_FORBIDDEN
            )
        motorista = MotoristaService.get_motorista_by_id(pk)
        if not motorista:
            return Response(
                {"detail": "Erro: Motorista não encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )
        MotoristaService.delete_motorista(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
