from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Videojuego, Comentario
from .serializers import VideojuegoSerializer, ComentarioSerializer
from .permissions import EsAdminOEmpleado

import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from .models import Videojuego


class VideojuegoFilter(django_filters.FilterSet):
    # Rango de precio
    min_precio = django_filters.NumberFilter(field_name='precio', lookup_expr='gte')
    max_precio = django_filters.NumberFilter(field_name='precio', lookup_expr='lte')
    # Rango de fecha de lanzamiento
    min_fecha = django_filters.DateFilter(field_name='fecha_lanzamiento', lookup_expr='gte')
    max_fecha = django_filters.DateFilter(field_name='fecha_lanzamiento', lookup_expr='lte')

    class Meta:
        model = Videojuego
        fields = []


# permite ?page_size=XX con un máximo
class DefaultPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# === Videojuegos CRUD ===
class VideojuegoViewSet(ModelViewSet):
    queryset = Videojuego.objects.all()
    serializer_class = VideojuegoSerializer
    permission_classes = [EsAdminOEmpleado] 

    #filtros + búsqueda + ordenación + paginación
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = VideojuegoFilter
    search_fields = ['titulo'] 
    ordering_fields = ['precio', 'fecha_lanzamiento', 'stock', 'titulo']
    ordering = ['-fecha_lanzamiento']  # orden por defecto
    pagination_class = DefaultPagination  # para ?page_size=XX (opcional)



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



