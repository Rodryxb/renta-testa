from django.db import models
from django.contrib.auth.models import AbstractUser
from decimal import Decimal

# ---------------------------------------------------------
# TABLA 1: Usuario Personalizado
# ---------------------------------------------------------
# Extendemos el usuario por defecto de Django para poder agregarle
# campos extra como 'rol' (para saber si es admin o cliente), 'telefono' y 'ciudad'.
class Usuario(AbstractUser):
    ROLES = (
        ('CLIENTE', 'Empresa Constructora'),
        ('EJECUTIVO', 'Ejecutivo de Arriendos'),
    )
    rol = models.CharField(max_length=20, choices=ROLES, default='CLIENTE')
    telefono = models.CharField(max_length=20, blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)

# ---------------------------------------------------------
# TABLA 2: Maquinaria y Materiales
# ---------------------------------------------------------
# Esta tabla es el corazón del inventario. Sirve tanto para máquinas pesadas
# como para materiales (arena, cemento). 
class Maquinaria(models.Model):
    TIPO_CHOICES = (
        ('MAQUINARIA', 'Maquinaria Pesada'),
        ('MATERIAL', 'Material de Construcción')
    )
    # Define si el producto se arrienda (Maquinaria) o se compra (Material)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='MAQUINARIA')
    nombre = models.CharField(max_length=150)
    categoria = models.CharField(max_length=100)
    
    # 'tarifa_diaria' sirve como cobro por día para máquinas, o como precio fijo para materiales.
    tarifa_diaria = models.DecimalField(max_digits=12, decimal_places=2) 
    
    # Monto en garantía que se retiene por seguridad (generalmente 0 para materiales)
    garantia = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Inventario físico disponible en la bodega
    stock_disponible = models.IntegerField(default=1)
    
    descripcion_detallada = models.TextField(blank=True, null=True)
    
    # Opciones de imagen: antigua (por URL de internet) o nueva (subida real desde PC)
    imagen_url = models.URLField(max_length=500, blank=True, null=True)
    imagen_upload = models.ImageField(upload_to='productos/', blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} (Stock: {self.stock_disponible})"

# ---------------------------------------------------------
# TABLA 3: Carro de Compras (Cabecera)
# ---------------------------------------------------------
# Cada usuario tiene exactamente 1 carro activo a la vez (OneToOneField)
class Carro(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='carro')

# ---------------------------------------------------------
# TABLA 4: Ítem dentro del Carro de Compras (Detalle)
# ---------------------------------------------------------
# Aquí se guarda qué echó el cliente al carrito temporalmente antes de pagar.
class ItemCarro(models.Model):
    carro = models.ForeignKey(Carro, on_delete=models.CASCADE, related_name='items')
    maquinaria = models.ForeignKey(Maquinaria, on_delete=models.CASCADE)
    
    # --- Datos si es Maquinaria (Arriendo) ---
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    factor_uso = models.DecimalField(max_digits=4, decimal_places=2, default=1.0)
    costo_delivery = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # --- Datos si es Material (Venta directa) ---
    cantidad = models.PositiveIntegerField(default=1)

    # Propiedad Calculada: Obtiene la cantidad de días entre la fecha de inicio y fin.
    @property
    def dias(self):
        if self.fecha_inicio and self.fecha_fin:
            delta = (self.fecha_fin - self.fecha_inicio).days
            return delta if delta > 0 else 1
        return 1

    # Propiedad Calculada: Esta es la matemática central del proyecto.
    @property
    def subtotal(self):
        # Si es material, es (Precio x Cantidad). Además aplica 10% descuento si compra 30 o más.
        if self.maquinaria.tipo == 'MATERIAL':
            base = self.maquinaria.tarifa_diaria * Decimal(self.cantidad)
            if self.cantidad >= 30:
                return base * Decimal('0.90') # 10% de descuento por mayor
            return base
        # Si es máquina, es (PrecioDiario x Factor x Dias) + Delivery + Garantia
        else:
            return (self.maquinaria.tarifa_diaria * self.factor_uso * Decimal(self.dias)) + self.costo_delivery + self.maquinaria.garantia

# ---------------------------------------------------------
# TABLA 5: Contrato (Orden de Compra / Boleta Real)
# ---------------------------------------------------------
# Cuando el cliente paga, el Carro se vacía y se genera un "Contrato" histórico.
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

# ---------------------------------------------------------
# TABLA 6: Detalle Histórico del Contrato
# ---------------------------------------------------------
# Guarda qué productos EXACTOS compró el usuario en esa orden específica y a qué precio,
# para que no cambie el historial si en el futuro el administrador le sube el precio a la máquina.
class ItemContrato(models.Model):
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, related_name='items')
    maquinaria = models.ForeignKey(Maquinaria, on_delete=models.PROTECT)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    cantidad = models.PositiveIntegerField(default=1)
    precio_cobrado = models.DecimalField(max_digits=12, decimal_places=2, default=0) 

# ---------------------------------------------------------
# TABLA 7: Servicios Externos (Profesionales)
# ---------------------------------------------------------
# Tabla para mostrar el portafolio de Topógrafos, Ingenieros, etc.
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

# ---------------------------------------------------------
# TABLA 8: Configuración de la Página
# ---------------------------------------------------------
# Permite que el Administrador cambie los textos gigantes y la foto de portada
# del inicio de la página web desde su panel sin tocar el código fuente HTML.
class Configuracion(models.Model):
    banner_url = models.URLField(max_length=500, blank=True, null=True)
    titulo_banner = models.CharField(max_length=200, default="Espacio para Banner E-Commerce")
    titulo_principal = models.CharField(max_length=200, default="Renta Testa")
    subtitulo_principal = models.TextField(default="Maquinarias de última generación, asesorías y materiales.")
    
    # Patrón Singleton: Asegura que siempre exista solo 1 registro de configuración
    @classmethod
    def get_solo(cls):
        obj, created = cls.objects.get_or_create(id=1)
        return obj
