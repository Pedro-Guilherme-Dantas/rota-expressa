from rota_expressa.models.telefone import Telefone
from rest_framework import serializers


class TelefoneResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Telefone
        fields = ['id', 'usuario', 'numero']


class TelefoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Telefone
        fields = ['usuario', 'numero']

        read_only_fields = ['id']
