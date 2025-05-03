from django.db import models
from django.utils import timezone 
from decimal import Decimal

class Cliente(models.Model):
    nombre = models.CharField(max_length=200)
    direccion = models.TextField(blank=True, null=True) 
    telefono = models.CharField(max_length=20, blank=True, null=True) 
    email = models.EmailField(blank=True, null=True)
    rut_dni = models.CharField(max_length=20, blank=True, null=True, unique=True)

    def __str__(self):
        return self.nombre

class Articulo(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=200)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

class Pedido(models.Model):

    # numero_pedido = models.IntegerField(max_length=100, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(default=timezone.now)
    fecha_entrega = models.DateField(blank=True, null=True)
    ESTADO_CHOICES = [
        ('PEN', 'Pendiente'),
        ('PRO', 'En Proceso'),
        ('COM', 'Completado'),
        ('CAN', 'Cancelado'),
    ]
    estado = models.CharField(max_length=3, choices=ESTADO_CHOICES, default='PEN')
    notas = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.nombre}"

    @property
    def total_pedido(self):
        return sum(linea.importe_linea for linea in self.lineapedido_set.all())


class LineaPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE) # Si borras pedido, se borran sus líneas
    articulo = models.ForeignKey(Articulo, on_delete=models.PROTECT) # No borres un artículo si hay pedidos que lo contienen
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    porcentaje_descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0) # % descuento

    def __str__(self):
        return f"Línea {self.id} para Pedido #{self.pedido.numero_pedido}"

    @property
    def importe_linea(self):

        cantidad_dec = Decimal(self.cantidad if self.cantidad is not None else 0)
        precio_dec = self.precio_unitario if self.precio_unitario is not None else Decimal('0.00')
        porcentaje_descuento_dec = self.porcentaje_descuento if self.porcentaje_descuento is not None else Decimal('0.00')

        descuento_ratio = porcentaje_descuento_dec / Decimal(100) if Decimal(100) != 0 else Decimal('0.00')

        # Opcional: Asegurar que el ratio de descuento está entre 0 y 1
        if descuento_ratio < 0:
            descuento_ratio = Decimal('0.00')
        if descuento_ratio > 1: # Si es más del 100%
             descuento_ratio = Decimal('1.00')

        importe_bruto = cantidad_dec * precio_dec
        importe_neto = importe_bruto * (Decimal(1) - descuento_ratio)

        return importe_neto


    def __str__(self):
        return f"Línea {self.id} para Pedido #{self.pedido.numero_pedido}"



