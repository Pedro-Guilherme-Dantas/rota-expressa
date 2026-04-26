from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rota_expressa.services.modelo_service import ModeloService
from rota_expressa.serializers.modelo_serializer import (
    ModeloSerializer, ModeloResponseSerializer
)
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class ModeloViewSet(viewsets.ViewSet):
    @extend_schema(
        summary="Lista os modelos",
        responses={200: ModeloResponseSerializer(many=True)}
    )
    @method_decorator(cache_page(60 * 60 * 24))
    def list(self, request):
        modelos = ModeloService.get_all_modelos()
        serializer = ModeloResponseSerializer(
            modelos, many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Cria um novo modelo",
        request=ModeloSerializer,
        responses={201: ModeloResponseSerializer}
    )
    def create(self, request):
        serializer = ModeloSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        modelo = ModeloService.criar_modelo(serializer.validated_data)
        response_serializer = ModeloResponseSerializer(modelo)
        return Response(
            response_serializer.data, status=status.HTTP_201_CREATED
        )

    @extend_schema(
        summary="Recupera um modelo por ID",
        responses={200: ModeloResponseSerializer, 404: "Not Found"}
    )
    def retrieve(self, request, pk=None):
        modelo = ModeloService.get_modelo_by_id(pk)
        serializer = ModeloResponseSerializer(modelo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Atualiza um modelo por ID",
        request=ModeloSerializer,
        responses={200: ModeloResponseSerializer, 404: "Not Found"}
    )
    def update(self, request, pk=None):
        serializer = ModeloSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        modelo = ModeloService.atualizar_modelo(
            pk, serializer.validated_data
        )
        response_serializer = ModeloResponseSerializer(modelo)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Atualiza parcialmente um modelo por ID",
        request=ModeloSerializer,
        responses={200: ModeloResponseSerializer, 404: "Not Found"}
    )
    def partial_update(self, request, pk=None):
        serializer = ModeloSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        modelo = ModeloService.atualizar_modelo(
            pk, serializer.validated_data
        )
        response_serializer = ModeloResponseSerializer(modelo)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Deleta um modelo por ID",
        responses={204: "No Content", 404: "Not Found"}
    )
    def destroy(self, request, pk=None):
        modelo = ModeloService.get_modelo_by_id(pk)
        if not modelo:
            return Response(
                {"detail": "Erro: Modelo não encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )
        ModeloService.deletar_modelo(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
