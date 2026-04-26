from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rota_expressa.services.avalicacao_service import AvaliacaoService
from rota_expressa.serializers.avaliacao_serializer import (
    AvaliacaoSerializer, AvaliacaoResponseSerializer
)


class AvaliacaoViewSet(viewsets.ViewSet):
    @extend_schema(
        summary="Lista as avaliações",
        responses={200: AvaliacaoResponseSerializer(many=True)}
    )
    def list(self, request):
        avaliacoes = AvaliacaoService.get_all_avaliacoes()
        serializer = AvaliacaoResponseSerializer(
            avaliacoes, many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Cria uma nova avaliação",
        request=AvaliacaoSerializer,
        responses={201: AvaliacaoResponseSerializer}
    )
    def create(self, request):
        serializer = AvaliacaoSerializer(
            data=request.data, context={
                'request': request}
        )
        serializer.is_valid(raise_exception=True)

        dados_da_avaliacao = serializer.validated_data

        dados_da_avaliacao['usuario'] = request.user

        avaliacao = AvaliacaoService.criar_avaliacao(dados_da_avaliacao)

        response_serializer = AvaliacaoResponseSerializer(avaliacao)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )

    @extend_schema(
        summary="Recupera uma avaliação por ID",
        responses={200: AvaliacaoResponseSerializer, 404: "Not Found"}
    )
    def retrieve(self, request, pk=None):
        avaliacao = AvaliacaoService.get_avaliacao_by_id(pk)
        serializer = AvaliacaoResponseSerializer(avaliacao)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Atualiza uma avaliação por ID",
        request=AvaliacaoSerializer,
        responses={200: AvaliacaoResponseSerializer, 404: "Not Found"}
    )
    def update(self, request, pk=None):
        serializer = AvaliacaoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        avaliacao = AvaliacaoService.atualizar_avaliacao(
            pk, serializer.validated_data
        )
        response_serializer = AvaliacaoResponseSerializer(avaliacao)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Atualiza parcialmente uma avaliação por ID",
        request=AvaliacaoSerializer,
        responses={200: AvaliacaoResponseSerializer, 404: "Not Found"}
    )
    def partial_update(self, request, pk=None):
        serializer = AvaliacaoSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        avaliacao = AvaliacaoService.atualizar_avaliacao(
            pk, serializer.validated_data
        )
        response_serializer = AvaliacaoResponseSerializer(avaliacao)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Deleta uma avaliação por ID",
        responses={204: "No Content", 404: "Not Found"}
    )
    def destroy(self, request, pk=None):
        avaliacao = AvaliacaoService.get_avaliacao_by_id(pk)
        if not avaliacao:
            return Response(
                {"detail": "Erro: Avaliação não encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )
        AvaliacaoService.deletar_avaliacao(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
