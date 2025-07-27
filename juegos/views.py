from rest_framework.viewsets import ModelViewSet
from .models import Videojuego
from .serializers import VideojuegoSerializer

class VideojuegoViewSet(ModelViewSet):
    queryset = Videojuego.objects.all()
    serializer_class = VideojuegoSerializer
