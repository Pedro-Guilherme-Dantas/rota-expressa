from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rota_expressa.views import (
    motorista_view, usuario_view, cidade_view, viagem_view,
    modelo_view, telefone_view, avaliacao_view, veiculo_view,
    me_view
)
from drf_spectacular.views import (
    SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()

router.register(
    r'me',
    me_view.MeViewSet,
    basename='me'
)
router.register(
    r'motoristas',
    motorista_view.MotoristaViewSet,
    basename='motorista'
)

router.register(
    r'usuarios',
    usuario_view.UsuarioViewSet,
    basename='usuario'
)

router.register(
    r'cidades',
    cidade_view.CidadeViewSet,
    basename='cidade'
)

router.register(
    r'modelos',
    modelo_view.ModeloViewSet,
    basename='modelo'
)

router.register(
    r'telefones',
    telefone_view.TelefoneViewSet,
    basename='telefone'
)

router.register(
    r'avaliacoes',
    avaliacao_view.AvaliacaoViewSet,
    basename='avaliacao'
)

router.register(
    r'veiculos',
    veiculo_view.VeiculoViewSet,
    basename='veiculo'
)

router.register(
    r'viagens',
    viagem_view.ViagemViewSet,
    basename='viagem'
)

urlpatterns = [
    path('', include(router.urls)),
    path(
        'token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),

    path(
        'docs/swagger/',
        SpectacularSwaggerView.as_view(
            url_name='schema'),
        name='swagger-ui'),

    path(
        'docs/redoc/',
        SpectacularRedocView.as_view(
            url_name='schema'),
        name='redoc'),
]
