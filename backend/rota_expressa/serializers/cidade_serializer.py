from rota_expressa.models.cidade import Cidade
from rest_framework import serializers


class CidadeResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cidade
        fields = ['id', 'nome', 'estado', 'cep']


class CidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cidade
        fields = ['nome', 'estado', 'cep']

        read_only_fields = ['id']
