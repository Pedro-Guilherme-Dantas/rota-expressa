from django.contrib.auth.models import AbstractUser
from django.db import models
from rota_expressa.models.cidade import Cidade


class Usuario(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)
    foto = models.ImageField(upload_to='perfis/', null=True, blank=True)
    cidade = models.ForeignKey(Cidade, on_delete=models.PROTECT, null=True)

    @property
    def is_motorista(self):
        return hasattr(self, 'perfil_motorista')

    def __str__(self):
        return self.username
