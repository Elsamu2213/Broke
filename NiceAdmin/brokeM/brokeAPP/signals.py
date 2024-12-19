from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Tarea, Notificacion

@receiver(post_save, sender=Tarea)
def crear_notificacion(sender, instance, created, **kwargs):
    # Solo crear notificación si el estado cambió
    if not created and hasattr(instance, '_original_estado') and instance.estado != instance._original_estado:
        # Crear notificación solo si el estado cambió
        Notificacion.objects.create(
            descripcion=f"El estado de la tarea {instance.id} ha cambiado de {instance._original_estado} a {instance.estado}",
            tarea=instance,
            usuario=instance.usuario
        )
