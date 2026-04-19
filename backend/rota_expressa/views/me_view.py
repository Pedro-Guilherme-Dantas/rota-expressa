from rest_framework import viewsets
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rota_expressa.serializers.usuario_serializer import UsuarioResponseSerializer

class MeViewSet(viewsets.ViewSet):
    @extend_schema(
        summary="Recupera os dados do usuário autenticado",
        responses={200: UsuarioResponseSerializer}
    )
    def list(self, request):
        serializer = UsuarioResponseSerializer(request.user)
        return Response(serializer.data)
