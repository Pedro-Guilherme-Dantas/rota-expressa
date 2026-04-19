from rota_expressa.models.modelo import Modelo
from rest_framework import serializers


class ModeloResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modelo
        fields = ['id', 'nome', 'ano', 'qtd_lugares']


class ModeloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modelo
        fields = ['nome', 'ano', 'qtd_lugares']

        read_only_fields = ['id']
