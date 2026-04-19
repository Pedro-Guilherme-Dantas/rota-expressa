import factory
from rota_expressa.models import Usuario, Motorista, Cidade, Modelo, Veiculo, Viagem


class CidadeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cidade

    nome = factory.Sequence(lambda n: f'Cidade {n}')
    estado = 'SP'
    cep = factory.Sequence(lambda n: f'{10000000 + n}')


class UsuarioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Usuario
        skip_postgeneration_save = True

    username = factory.Sequence(lambda n: f'usuario_{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@teste.com')
    first_name = 'Fulano'
    last_name = 'de Tal'
    password = factory.PostGenerationMethodCall('set_password', 'senha12345')
    cidade = factory.SubFactory(CidadeFactory)

    @classmethod
    def _after_postgeneration(cls, instance, create, results=None):
        if create:
            instance.save()


class MotoristaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Motorista

    usuario = factory.SubFactory(UsuarioFactory)
    resumo = 'Motorista experiente.'


class ModeloFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Modelo

    nome = factory.Sequence(lambda n: f'Modelo {n}')
    ano = 2024
    qtd_lugares = 4


class VeiculoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Veiculo

    modelo = factory.SubFactory(ModeloFactory)
    placa = factory.Sequence(lambda n: f'AAA{n:04d}')
    cor = 'BRANCO'
    motorista = factory.SubFactory(MotoristaFactory)


class ViagemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Viagem

    origem = factory.SubFactory(CidadeFactory)
    destino = factory.SubFactory(CidadeFactory)
    horario_partida = '08:00'
    horario_chegada = '10:00'
    dia_semana = 0
    valor = '50.00'
    veiculo = factory.SubFactory(VeiculoFactory)
    motorista = factory.LazyAttribute(lambda obj: obj.veiculo.motorista)
