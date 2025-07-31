from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    VideojuegoViewSet,
    ComentarioCreateAPIView,
    ComentarioListAPIView,
    CrearComentarioEnVideojuego  
)

router = DefaultRouter()
router.register(r'videojuegos', VideojuegoViewSet, basename='videojuego')

urlpatterns = router.urls + [
    path('comentarios/', ComentarioListAPIView.as_view(), name='comentario-list'),
    path('comentarios/nuevo/', ComentarioCreateAPIView.as_view(), name='comentario-create'),
    path('videojuegos/<int:videojuego_id>/comentarios/', CrearComentarioEnVideojuego.as_view(), name='crear-comentario-en-videojuego'), 
]
