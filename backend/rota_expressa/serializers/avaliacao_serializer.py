from rota_expressa.models.avaliacao import Avaliacao
from rest_framework import serializers


class AvaliacaoResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avaliacao
        fields = ['id', 'motorista', 'usuario', 'nota', 'comentario', 'data_avaliacao']


class AvaliacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avaliacao
        fields = ['motorista', 'usuario', 'nota', 'comentario']
        read_only_fields = ['id', 'data_avaliacao', 'usuario']
