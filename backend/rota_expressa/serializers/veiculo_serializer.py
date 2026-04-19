from rota_expressa.models.veiculo import Veiculo
from rest_framework import serializers


class VeiculoResponseSerializer(serializers.ModelSerializer):
    modelo = serializers.StringRelatedField()
    motorista = serializers.StringRelatedField()

    class Meta:
        model = Veiculo
        fields = ['id', 'modelo', 'placa', 'cor', 'motorista']


class VeiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veiculo
        fields = ['modelo', 'placa', 'cor', 'motorista']

        read_only_fields = ['id', 'motorista']
