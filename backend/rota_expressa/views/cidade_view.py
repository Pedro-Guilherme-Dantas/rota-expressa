from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rota_expressa.services.cidade_service import CidadeService
from rota_expressa.serializers.cidade_serializer import (
    CidadeSerializer, CidadeResponseSerializer
)
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class CidadeViewSet(viewsets.ViewSet):
    @extend_schema(
        summary="Lista as cidades",
        responses={200: CidadeResponseSerializer(many=True)}
    )
    @method_decorator(cache_page(60 * 60 * 24))
    def list(self, request):
        cidades = CidadeService.get_all_cidades()
        serializer = CidadeResponseSerializer(
            cidades, many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Cria uma nova cidade",
        request=CidadeSerializer,
        responses={201: CidadeResponseSerializer}
    )
    def create(self, request):
        serializer = CidadeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cidade = CidadeService.criar_cidade(serializer.validated_data)
        response_serializer = CidadeResponseSerializer(cidade)
        return Response(
            response_serializer.data, status=status.HTTP_201_CREATED
        )

    @extend_schema(
        summary="Recupera uma cidade por ID",
        responses={200: CidadeResponseSerializer, 404: "Not Found"}
    )
    def retrieve(self, request, pk=None):
        cidade = CidadeService.get_cidade_by_id(pk)
        serializer = CidadeResponseSerializer(cidade)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Atualiza uma cidade por ID",
        request=CidadeSerializer,
        responses={200: CidadeResponseSerializer, 404: "Not Found"}
    )
    def update(self, request, pk=None):
        serializer = CidadeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cidade = CidadeService.atualizar_cidade(
            pk, serializer.validated_data
        )
        response_serializer = CidadeResponseSerializer(cidade)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Atualiza parcialmente uma cidade por ID",
        request=CidadeSerializer,
        responses={200: CidadeResponseSerializer, 404: "Not Found"}
    )
    def partial_update(self, request, pk=None):
        serializer = CidadeSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        cidade = CidadeService.atualizar_cidade(
            pk, serializer.validated_data
        )
        response_serializer = CidadeResponseSerializer(cidade)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Deleta uma cidade por ID",
        responses={204: "No Content", 404: "Not Found"}
    )
    def destroy(self, request, pk=None):
        cidade = CidadeService.get_cidade_by_id(pk)
        if not cidade:
            return Response(
                {"detail": "Erro: Cidade não encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )
        CidadeService.deletar_cidade(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
