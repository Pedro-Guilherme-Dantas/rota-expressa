from rota_expressa.serializers.usuario_serializer import UsuarioResponseSerializer
from rota_expressa.models.motorista import Motorista
from rest_framework import serializers


class MotoristaResponseSerializer(serializers.ModelSerializer):
    usuario = UsuarioResponseSerializer(read_only=True)

    class Meta:
        model = Motorista
        fields = [
            'id',
            'usuario',
            'nota_media',
            'resumo',
            ]


class MotoristaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motorista
        fields = [
            'resumo',
            ]

        read_only_fields = ['id', 'nota_media', 'usuario']
