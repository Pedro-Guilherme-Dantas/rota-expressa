from django.db.models import Avg
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from rota_expressa.models.motorista import Motorista
from rota_expressa.models.avaliacao import Avaliacao


@receiver(post_save, sender=Avaliacao)
@receiver(post_delete, sender=Avaliacao)
def update_motorista_media(sender, instance, **kwargs):
    motorista = instance.motorista

    stats = motorista.avaliacoes.aggregate(media=Avg('nota'))

    nova_media = stats['media'] or 0.0

    Motorista.objects.filter(pk=motorista.pk).update(nota_media=nova_media)
