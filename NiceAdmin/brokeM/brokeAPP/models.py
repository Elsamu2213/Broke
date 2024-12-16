from django.contrib.auth.models import AbstractUser
from django.db import models

# Si necesitas agregar más campos, puedes extender el modelo de usuario de Django
class UsuarioCustomizado(AbstractUser):
    telefono = models.CharField(max_length=15, blank=True, unique=True)
    rol = models.CharField(
        max_length=10,
        choices=[('Admin', 'Admin'), ('Empleado', 'Empleado')],
        default='Empleado'
    )
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'  # Cambia el campo para la autenticación
    REQUIRED_FIELDS = []  # Puedes dejarlo vacío si no tienes campos requeridos adicionales

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Otras tablas como Cliente, Cotizacion, Factura, Tarea, etc.

class Cliente(models.Model):
    nombre_empresa = models.CharField(max_length=100)
    contacto_nombre = models.CharField(max_length=100)
    contacto_email = models.EmailField()
    telefono = models.CharField(max_length=15, blank=True)
    direccion = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre_empresa
    
class Cotizacion(models.Model):
    usuario = models.ForeignKey('UsuarioCustomizado', on_delete=models.CASCADE)  # Relación con el nuevo modelo
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(
        max_length=50,
        default='Pendiente',
        choices=[
            ('Pendiente', 'Pendiente'),
            ('Aceptada', 'Aceptada'),
            ('Rechazada', 'Rechazada'),
        ]
    )

class Factura(models.Model):
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE)
    fecha = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    pagada = models.BooleanField(default=False)

class Tarea(models.Model):
    descripcion = models.CharField(max_length=255)
    fecha_anclaje = models.CharField(max_length=20, null=True, blank=True)  # Cambiado a CharField
    hora_anclaje = models.CharField(max_length=10, null=True, blank=True)
    fecha_vencimiento = models.CharField(max_length=20, null=True, blank=True)  # Cambiado a CharField
    hora_venconfig = models.CharField(max_length=10, null=True, blank=True)
    direccion = models.CharField(max_length=255, default="Dirección pendiente")
    actividad = models.CharField(max_length=50, choices=[
        ('Anclaje', 'Anclaje'),
        ('Configuración', 'Configuración'),
        ('Fibra', 'Fibra')
    ], default='Anclaje')
    usuario = models.ForeignKey('UsuarioCustomizado', on_delete=models.SET_NULL, null=True, blank=True)  # Usar el nuevo modelo
    num_cajero = models.CharField(max_length=50, unique=True, default="Sin número")  # Con un valor por defecto único
    observaciones = models.TextField(null=True, blank=True)  # Campo observaciones que permite nulos y vacíos
    completada = models.BooleanField(default=False)  # Campo para marcar si está completada
    Cod_postal = models.CharField(max_length=255, default="Dirección pendiente")# Campo para marcar si está completada
    cordenadas = models.CharField(max_length=255, default="cordenadas pendiente")# Campo para marcar si está completada

    estado = models.CharField(max_length=20, choices=[
         ('iniciado', 'Iniciado'),
        ('en_proceso', 'En Proceso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
        ('pendiente_revision', 'Pendiente de Revisión'),
        ('reasignado', 'Reasignado'),
    ], default='pendiente')  # Agregar campo estado
    
    def __str__(self):
        return f"Tarea {self.id}: {self.descripcion}"

    @property
    def asignada(self):
        return self.usuario is not None


class MensajeWhatsApp(models.Model):
    usuario = models.ForeignKey('UsuarioCustomizado', on_delete=models.CASCADE)
    mensaje = models.TextField()
    imagen_url = models.CharField(max_length=255, blank=True)
    fecha_envio = models.DateTimeField(auto_now_add=True)

class Notificacion(models.Model):
    tipo = models.CharField(
        max_length=20,
        choices=[('Factura', 'Factura'), ('Tarea', 'Tarea'), ('Mensaje', 'Mensaje')],
        null=False
    )
    usuario = models.ForeignKey('UsuarioCustomizado', on_delete=models.CASCADE)
    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    leida = models.BooleanField(default=False)

class Salario(models.Model):
    usuario = models.ForeignKey('UsuarioCustomizado', on_delete=models.CASCADE)
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE)
    lugar_trabajo = models.CharField(max_length=100)
    viaticos = models.DecimalField(max_digits=10, decimal_places=2)
    pago_actividad = models.DecimalField(max_digits=10, decimal_places=2)
    total_pago = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    fecha_pago = models.DateField()

    def save(self, *args, **kwargs):
        self.total_pago = self.viaticos + self.pago_actividad
        super(Salario, self).save(*args, **kwargs)


class TareaAvanzada(Tarea):
    prioridad = models.CharField(max_length=50, choices=[('Alta', 'Alta'), ('Media', 'Media'), ('Baja', 'Baja')], default='Media')
    responsable = models.CharField(max_length=100, null=True, blank=True)
    comentarios = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Tarea Avanzada {self.id}: {self.descripcion} (Prioridad: {self.prioridad})"