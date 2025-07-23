from django.db import models

class Videojuego(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    fecha_lanzamiento = models.DateField()

    def __str__(self):
        return self.titulo