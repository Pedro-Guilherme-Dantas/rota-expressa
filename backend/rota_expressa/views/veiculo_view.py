from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rota_expressa.services.veiculo_service import VeiculoService
from rota_expressa.serializers.veiculo_serializer import (
    VeiculoSerializer, VeiculoResponseSerializer
)


class VeiculoViewSet(viewsets.ViewSet):
    @extend_schema(
        summary="Lista os veículos",
        responses={200: VeiculoResponseSerializer(many=True)}
    )
    def list(self, request):
        veiculos = VeiculoService.get_all_veiculos()
        serializer = VeiculoResponseSerializer(
            veiculos, many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Cria um novo veículo",
        request=VeiculoSerializer,
        responses={201: VeiculoResponseSerializer}
    )
    def create(self, request):
        serializer = VeiculoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        veiculo = VeiculoService.criar_veiculo(
            serializer.validated_data, request.user
        )
        response_serializer = VeiculoResponseSerializer(veiculo)
        return Response(
            response_serializer.data, status=status.HTTP_201_CREATED
        )

    @extend_schema(
        summary="Recupera um veículo por ID",
        responses={200: VeiculoResponseSerializer, 404: "Not Found"}
    )
    def retrieve(self, request, pk=None):
        veiculo = VeiculoService.get_veiculo_by_id(pk)
        serializer = VeiculoResponseSerializer(veiculo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Atualiza um veículo por ID",
        request=VeiculoSerializer,
        responses={200: VeiculoResponseSerializer, 404: "Not Found"}
    )
    def update(self, request, pk=None):
        serializer = VeiculoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        veiculo = VeiculoService.atualizar_veiculo(
            pk, serializer.validated_data
        )
        response_serializer = VeiculoResponseSerializer(veiculo)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Atualiza parcialmente um veículo por ID",
        request=VeiculoSerializer,
        responses={200: VeiculoResponseSerializer, 404: "Not Found"}
    )
    def partial_update(self, request, pk=None):
        serializer = VeiculoSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        veiculo = VeiculoService.atualizar_veiculo(
            pk, serializer.validated_data
        )
        response_serializer = VeiculoResponseSerializer(veiculo)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Deleta um veículo por ID",
        responses={204: "No Content", 404: "Not Found"}
    )
    def destroy(self, request, pk=None):
        veiculo = VeiculoService.get_veiculo_by_id(pk)
        if not veiculo:
            return Response(
                {"detail": "Erro: Veículo não encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )
        VeiculoService.delete_veiculo(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
