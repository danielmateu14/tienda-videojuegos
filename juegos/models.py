from django.db import models
from django.conf import settings

class Videojuego(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    fecha_lanzamiento = models.DateField()

    def __str__(self):
        return self.titulo
    

class Comentario(models.Model):
    videojuego = models.ForeignKey('Videojuego', on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        rol = self.autor.rol
        extra = " (staff)" if rol in ['admin', 'empleado'] else ""
        return f"{self.autor.username}{extra} - {self.texto[:30]}"
