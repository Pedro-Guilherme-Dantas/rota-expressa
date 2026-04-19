from rota_expressa.models.usuario import Usuario
from rest_framework import serializers


class UsuarioResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'cidade',
            'last_login',
            'date_joined'
            ]


class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    username = serializers.CharField(min_length=3, max_length=50)
    first_name = serializers.CharField(min_length=2, max_length=100)
    last_name = serializers.CharField(min_length=2, max_length=100)

    class Meta:
        model = Usuario
        fields = [
            'username',
            'first_name',
            'last_name',
            'cidade',
            'email',
            'password'
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
