from django.db import models
from django.contrib.auth.models import AbstractUser
from decimal import Decimal

class Usuario(AbstractUser):
    ROLES = (
        ('CLIENTE', 'Empresa Constructora'),
        ('EJECUTIVO', 'Ejecutivo de Arriendos'),
    )
    rol = models.CharField(max_length=20, choices=ROLES, default='CLIENTE')
    telefono = models.CharField(max_length=20, blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)

class Maquinaria(models.Model):
    TIPO_CHOICES = (
        ('MAQUINARIA', 'Maquinaria Pesada'),
        ('MATERIAL', 'Material de Construcción')
    )
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='MAQUINARIA')
    nombre = models.CharField(max_length=150)
    categoria = models.CharField(max_length=100)
    tarifa_diaria = models.DecimalField(max_digits=12, decimal_places=2) # actua como precio unitario en materiales
    garantia = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    stock_disponible = models.IntegerField(default=1)
    descripcion_detallada = models.TextField(blank=True, null=True)
    imagen_url = models.URLField(max_length=500, blank=True, null=True)
    imagen_upload = models.ImageField(upload_to='productos/', blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} (Stock: {self.stock_disponible})"

class Carro(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='carro')

class ItemCarro(models.Model):
    carro = models.ForeignKey(Carro, on_delete=models.CASCADE, related_name='items')
    maquinaria = models.ForeignKey(Maquinaria, on_delete=models.CASCADE)
    
    # Para Maquinarias
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    factor_uso = models.DecimalField(max_digits=4, decimal_places=2, default=1.0)
    costo_delivery = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Para Materiales
    cantidad = models.PositiveIntegerField(default=1)

    @property
    def dias(self):
        if self.fecha_inicio and self.fecha_fin:
            delta = (self.fecha_fin - self.fecha_inicio).days
            return delta if delta > 0 else 1
        return 1

    @property
    def subtotal(self):
        if self.maquinaria.tipo == 'MATERIAL':
            base = self.maquinaria.tarifa_diaria * Decimal(self.cantidad)
            if self.cantidad >= 30:
                return base * Decimal('0.90') # 10% descuento
            return base
        else:
            return (self.maquinaria.tarifa_diaria * self.factor_uso * Decimal(self.dias)) + self.costo_delivery + self.maquinaria.garantia

class Contrato(models.Model):
    ESTADOS = (
        ('PENDIENTE', 'Pendiente'),
        ('PAGADO', 'Pagado'),
        ('ENTREGADO', 'Entregado'),
        ('COMPLETADO', 'Completado'),
        ('CANCELADO', 'Cancelado'),
    )
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='contratos')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

class ItemContrato(models.Model):
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, related_name='items')
    maquinaria = models.ForeignKey(Maquinaria, on_delete=models.PROTECT)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    cantidad = models.PositiveIntegerField(default=1)
    precio_cobrado = models.DecimalField(max_digits=12, decimal_places=2, default=0) # Subtotal cobrado final


class ServicioExterno(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    nombre_encargado = models.CharField(max_length=150)
    titulo_universitario = models.CharField(max_length=150)
    telefono = models.CharField(max_length=20)
    horario = models.CharField(max_length=100)
    foto_url = models.URLField(max_length=500, blank=True, null=True)
    foto_upload = models.ImageField(upload_to='servicios/', blank=True, null=True)

    def __str__(self):
        return self.titulo


class Configuracion(models.Model):
    banner_url = models.URLField(max_length=500, blank=True, null=True)
    titulo_banner = models.CharField(max_length=200, default="Espacio para Banner E-Commerce")
    titulo_principal = models.CharField(max_length=200, default="Renta testa.")
    subtitulo_principal = models.TextField(default="Maquinarias de última generación, asesorías y materiales minoristas y mayoristas.")
    @classmethod
    def get_solo(cls):
        obj, created = cls.objects.get_or_create(id=1)
        return obj
