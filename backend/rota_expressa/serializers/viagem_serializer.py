from rota_expressa.models.viagem import Viagem
from rest_framework import serializers


class ViagemResponseSerializer(serializers.ModelSerializer):
    origem = serializers.StringRelatedField()
    destino = serializers.StringRelatedField()

    veiculo_detalhes = serializers.SerializerMethodField()
    motorista_detalhes = serializers.SerializerMethodField()

    class Meta:
        model = Viagem
        fields = [
            'id', 'origem', 'destino', 'horario_partida', 'horario_chegada',
            'dia_semana', 'valor', 'veiculo', 'motorista', 'is_pet_friendly',
            'is_acessivel', 'is_ativo', 'veiculo_detalhes', 'motorista_detalhes'
        ]

    def get_veiculo_detalhes(self, obj):
        return {
            "modelo": obj.veiculo.modelo.nome,
            "placa": obj.veiculo.placa
        }

    def get_motorista_detalhes(self, obj):
        usuario = obj.motorista.usuario
        telefone_obj = usuario.telefones.first()
        return {
            "nome": usuario.first_name or usuario.username,
            "telefone": telefone_obj.numero if telefone_obj else None,
        }


class ViagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Viagem
        fields = [
            'origem',
            'destino',
            'horario_partida',
            'horario_chegada',
            'dia_semana',
            'valor',
            'veiculo',
            'is_pet_friendly',
            'is_acessivel',
            'is_ativo',
        ]

        read_only_fields = ['id', 'motorista']

    def validate(self, data):
        origem = data.get('origem')
        destino = data.get('destino')
        if origem and destino and origem == destino:
            raise serializers.ValidationError({"detail": "A origem e o destino não podem ser a mesma cidade."})
        return data
