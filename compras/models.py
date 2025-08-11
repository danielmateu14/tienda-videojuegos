from decimal import Decimal
from django.conf import settings
from django.db import models

class Compra(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='compras'
    )
    videojuego = models.ForeignKey(
        'juegos.Videojuego',
        on_delete=models.PROTECT, 
        related_name='compras'
    )
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f'Compra #{self.pk} - {self.usuario} - {self.videojuego} x{self.cantidad}'

    @property
    def total(self) -> Decimal:
        return (self.precio_unitario or Decimal('0')) * Decimal(self.cantidad or 0)
