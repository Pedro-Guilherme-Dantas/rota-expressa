from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rota_expressa.services.telefone_service import TelefoneService
from rota_expressa.serializers.telefone_serializer import (
    TelefoneSerializer, TelefoneResponseSerializer
)


class TelefoneViewSet(viewsets.ViewSet):
    @extend_schema(
        summary="Lista os telefones",
        responses={200: TelefoneResponseSerializer(many=True)}
    )
    def list(self, request):
        telefones = TelefoneService.get_all_telefones()
        serializer = TelefoneResponseSerializer(
            telefones, many=True
            )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Cria um novo telefone",
        request=TelefoneSerializer,
        responses={201: TelefoneResponseSerializer}
    )
    def create(self, request):
        serializer = TelefoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        telefone = TelefoneService.criar_telefone(serializer.validated_data)
        response_serializer = TelefoneResponseSerializer(telefone)
        return Response(
            response_serializer.data, status=status.HTTP_201_CREATED
            )

    @extend_schema(
        summary="Recupera um telefone por ID",
        responses={200: TelefoneResponseSerializer, 404: "Not Found"}
    )
    def retrieve(self, request, pk=None):
        telefone = TelefoneService.get_telefone_by_id(pk)
        serializer = TelefoneResponseSerializer(telefone)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Atualiza um telefone por ID",
        request=TelefoneSerializer,
        responses={200: TelefoneResponseSerializer, 404: "Not Found"}
    )
    def update(self, request, pk=None):
        serializer = TelefoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        telefone = TelefoneService.atualizar_telefone(
            pk, serializer.validated_data
            )
        response_serializer = TelefoneResponseSerializer(telefone)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Atualiza parcialmente um telefone por ID",
        request=TelefoneSerializer,
        responses={200: TelefoneResponseSerializer, 404: "Not Found"}
    )
    def partial_update(self, request, pk=None):
        serializer = TelefoneSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        telefone = TelefoneService.atualizar_telefone(
            pk, serializer.validated_data
            )
        response_serializer = TelefoneResponseSerializer(telefone)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Deleta um telefone por ID",
        responses={204: "No Content", 404: "Not Found"}
    )
    def destroy(self, request, pk=None):
        telefone = TelefoneService.get_telefone_by_id(pk)
        if not telefone:
            return Response(
                {"detail": "Erro: Telefone não encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )
        TelefoneService.deletar_telefone(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
