from django.urls import path
from .views import VideojuegoListCreateAPIView, VideojuegoDetailAPIView

urlpatterns = [
    path('videojuegos/', VideojuegoListCreateAPIView.as_view(), name='videojuego-list-create'),
    path('videojuegos/<int:pk>/', VideojuegoDetailAPIView.as_view(), name='videojuego-detail'),

]