from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True)
    rol = models.CharField(
        max_length=10,
        choices=[('Admin', 'Admin'), ('Empleado', 'Empleado')],
        default='Empleado'
    )
    contrasena = models.CharField(max_length=255)
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Equivalente a TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Cliente(models.Model):
    nombre_empresa = models.CharField(max_length=100)
    contacto_nombre = models.CharField(max_length=100)
    contacto_email = models.EmailField()
    telefono = models.CharField(max_length=15, blank=True)
    direccion = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre_empresa

class Cotizacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
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
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    fecha_vencimiento = models.DateTimeField(null=True, blank=True)
    direccion = models.CharField(max_length=255, default="Dirección pendiente")
    actividad = models.CharField(max_length=50, choices=[
        ('Anclaje', 'Anclaje'),
        ('Configuración', 'Configuración'),
        ('Fibra', 'Fibra')
    ], default='Anclaje')
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)  # Campo para almacenar el usuario asignado

    def __str__(self):
        return f"Tarea {self.id}: {self.descripcion}"

    # Agrega una propiedad para saber si la tarea está asignada
    @property
    def asignada(self):
        return self.usuario is not None


class MensajeWhatsApp(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    mensaje = models.TextField()
    imagen_url = models.CharField(max_length=255, blank=True)
    fecha_envio = models.DateTimeField(auto_now_add=True)  # Equivalente a TIMESTAMP DEFAULT CURRENT_TIMESTAMP

class Notificacion(models.Model):
    tipo = models.CharField(
        max_length=20,
        choices=[('Factura', 'Factura'), ('Tarea', 'Tarea'), ('Mensaje', 'Mensaje')],
        null=False
    )
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)  # Equivalente a TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    leida = models.BooleanField(default=False)

class Salario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE)
    lugar_trabajo = models.CharField(max_length=100)
    viaticos = models.DecimalField(max_digits=10, decimal_places=2)
    pago_actividad = models.DecimalField(max_digits=10, decimal_places=2)
    total_pago = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    fecha_pago = models.DateField()

    def save(self, *args, **kwargs):
        self.total_pago = self.viaticos + self.pago_actividad
        super(Salario, self).save(*args, **kwargs)