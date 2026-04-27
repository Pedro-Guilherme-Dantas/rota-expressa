from rota_expressa.models.usuario import Usuario
from rest_framework import serializers


class UsuarioResponseSerializer(serializers.ModelSerializer):
    cidade_nome = serializers.ReadOnlyField(source='cidade.nome')
    class Meta:
        model = Usuario
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'cidade',
            'cidade_nome',
            'is_motorista',
            'last_login',
            'date_joined'
            ]


class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    username = serializers.CharField(min_length=3, max_length=50)
    first_name = serializers.CharField(min_length=2, max_length=100)
    last_name = serializers.CharField(min_length=2, max_length=100)
    is_motorista = serializers.BooleanField(write_only=True, required=False, default=False)

    class Meta:
        model = Usuario
        fields = [
            'username',
            'first_name',
            'last_name',
            'cidade',
            'email',
            'password',
            'is_motorista'
            ]

        read_only_fields = [
            'id',
            'usuario',
            'groups',
            'user_permissions',
            'is_staff',
            'is_active',
            'is_superuser',
            'last_login',
            'date_joined'
            ]
