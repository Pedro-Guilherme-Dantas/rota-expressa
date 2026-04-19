from django.contrib import admin
from .models import Usuario, Motorista, Viagem, Veiculo, Modelo, Cidade, Avaliacao

admin.site.register(Usuario)
admin.site.register(Motorista)
admin.site.register(Viagem)
admin.site.register(Veiculo)
admin.site.register(Modelo)
admin.site.register(Cidade)
admin.site.register(Avaliacao)