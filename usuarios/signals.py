from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Postulacion, Notificacion, Invitacion


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


# SEÑALES PARA INVITACIONES (Ticket 3.8)
@receiver(post_save, sender=Invitacion)
def handle_invitacion_aceptada(sender, instance, created, **kwargs):
    """
    Signal que crea notificación cuando un músico acepta una invitación.
    """
    if not created and instance.estado == 'aceptada':
        Notificacion.objects.create(
            empleador=instance.empleador,
            tipo='invitacion_aceptada',
            titulo=f'Invitación aceptada - {instance.oferta_laboral.titulo}',
            mensaje=f'{instance.musico.get_full_name()} ha aceptado tu invitación para "{instance.oferta_laboral.titulo}". Se ha creado automáticamente una postulación.',
            invitacion=instance,
            oferta_laboral=instance.oferta_laboral,
            postulacion=instance.postulacion_creada
        )


@receiver(post_save, sender=Invitacion)
def handle_invitacion_rechazada(sender, instance, created, **kwargs):
    """
    Signal que crea notificación cuando un músico rechaza una invitación.
    """
    if not created and instance.estado == 'rechazada':
        mensaje_base = f'{instance.musico.get_full_name()} ha rechazado tu invitación para "{instance.oferta_laboral.titulo}".'
        mensaje_completo = mensaje_base
        
        if instance.mensaje_respuesta:
            mensaje_completo += f'\n\nMotivo: {instance.mensaje_respuesta}'
        
        Notificacion.objects.create(
            empleador=instance.empleador,
            tipo='invitacion_rechazada',
            titulo=f'Invitación rechazada - {instance.oferta_laboral.titulo}',
            mensaje=mensaje_completo,
            invitacion=instance,
            oferta_laboral=instance.oferta_laboral
        )


@receiver(post_save, sender=Invitacion)
def handle_invitacion_expirada(sender, instance, created, **kwargs):
    """
    Signal que crea notificación cuando una invitación expira sin respuesta.
    """
    if not created and instance.estado == 'expirada':
        Notificacion.objects.create(
            empleador=instance.empleador,
            tipo='invitacion_expirada',
            titulo=f'Invitación expirada - {instance.oferta_laboral.titulo}',
            mensaje=f'Tu invitación a {instance.musico.get_full_name()} para "{instance.oferta_laboral.titulo}" ha expirado sin respuesta.',
            invitacion=instance,
            oferta_laboral=instance.oferta_laboral
        )
