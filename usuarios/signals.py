from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Postulacion, Notificacion


@receiver(post_save, sender=Postulacion)
def handle_postulacion_accepted(sender, instance, created, **kwargs):
    """
    Signal que maneja el cierre automático de ofertas cuando se aceptan postulaciones.
    Se ejecuta cada vez que se guarda una Postulacion.
    """
    if instance.estado == 'aceptada':
        instance.oferta_laboral.verificar_y_cerrar_si_completa()


@receiver(post_save, sender=Postulacion)
def handle_postulacion_cancelada(sender, instance, created, **kwargs):
    """
    Signal que crea notificación cuando un músico cancela su postulación.
    """
    if not created and instance.estado == 'cancelada':
        Notificacion.objects.create(
            empleador=instance.oferta_laboral.empleador,
            tipo='postulacion_cancelada',
            titulo=f'Postulación cancelada - {instance.oferta_laboral.titulo}',
            mensaje=f'{instance.musico.get_full_name()} ha cancelado su postulación a "{instance.oferta_laboral.titulo}".',
            postulacion=instance,
            oferta_laboral=instance.oferta_laboral
        )


@receiver(post_save, sender=Postulacion)
def handle_postulacion_response_date(sender, instance, **kwargs):
    """
    Signal que actualiza la fecha de respuesta automáticamente.
    Ya está implementado en el método save() del modelo, pero mantenermos consistency.
    """
    pass
