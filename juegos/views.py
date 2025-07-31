from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Videojuego, Comentario
from .serializers import VideojuegoSerializer, ComentarioSerializer
from .permissions import EsAdminOEmpleado


# === Videojuegos CRUD ===
class VideojuegoViewSet(ModelViewSet):
    queryset = Videojuego.objects.all()
    serializer_class = VideojuegoSerializer
    permission_classes = [EsAdminOEmpleado]


# === Comentarios generales ===
class ComentarioListAPIView(generics.ListAPIView):
    serializer_class = ComentarioSerializer
    queryset = Comentario.objects.all()


class ComentarioCreateAPIView(generics.CreateAPIView):
    serializer_class = ComentarioSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(autor=self.request.user)


# === Comentario anidado en videojuego ===
class CrearComentarioEnVideojuego(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, videojuego_id):
        videojuego = get_object_or_404(Videojuego, id=videojuego_id)
        serializer = ComentarioSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(videojuego=videojuego, autor=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
