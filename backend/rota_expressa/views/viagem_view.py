from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rota_expressa.services.viagem_service import ViagemService
from rota_expressa.serializers.viagem_serializer import (
    ViagemSerializer, ViagemResponseSerializer
)
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class ViagemViewSet(viewsets.ViewSet):
    @extend_schema(
        summary="Lista as viagens",
        responses={200: ViagemResponseSerializer(many=True)}
    )
    @method_decorator(cache_page(60 * 5))
    def list(self, request):
        origem = request.query_params.get('origem')
        destino = request.query_params.get('destino')
        horario = request.query_params.get('horario_partida')
        preco = request.query_params.get('valor__lte')

        viagens = ViagemService.get_viagens_filtradas(
            origem=origem,
            destino=destino,
            horario=horario,
            preco=preco
        )

        serializer = ViagemResponseSerializer(viagens, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Cria uma nova viagem",
        request=ViagemSerializer,
        responses={201: ViagemResponseSerializer}
    )
    def create(self, request):
        dados_preparados = ViagemService.processar_cidades_ibge(request.data)

        serializer = ViagemSerializer(data=dados_preparados)
        serializer.is_valid(raise_exception=True)

        viagem = ViagemService.criar_viagem(
            serializer.validated_data, request.user)

        response_serializer = ViagemResponseSerializer(viagem)
        return Response(response_serializer.data,
                        status=status.HTTP_201_CREATED
                        )

    @extend_schema(
        summary="Recupera uma viagem por ID",
        responses={200: ViagemResponseSerializer, 404: "Not Found"}
    )
    def retrieve(self, request, pk=None):
        viagem = ViagemService.get_viagem_by_id(pk)
        serializer = ViagemResponseSerializer(viagem)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Atualiza uma viagem por ID",
        request=ViagemSerializer,
        responses={200: ViagemResponseSerializer, 404: "Not Found"}
    )
    def update(self, request, pk=None):
        serializer = ViagemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        viagem = ViagemService.atualizar_viagem(
            pk, serializer.validated_data
        )
        response_serializer = ViagemResponseSerializer(viagem)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Atualiza parcialmente uma viagem por ID",
        request=ViagemSerializer,
        responses={200: ViagemResponseSerializer, 404: "Not Found"}
    )
    def partial_update(self, request, pk=None):
        serializer = ViagemSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        viagem = ViagemService.atualizar_viagem(
            pk, serializer.validated_data
        )
        response_serializer = ViagemResponseSerializer(viagem)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Deleta uma viagem por ID",
        responses={204: "No Content", 404: "Not Found"}
    )
    def destroy(self, request, pk=None):
        viagem = ViagemService.get_viagem_by_id(pk)
        if not viagem:
            return Response(
                {"detail": "Erro: Viagem não encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )
        ViagemService.delete_viagem(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
