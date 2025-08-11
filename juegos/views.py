from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from .models import Videojuego, Comentario
from .serializers import VideojuegoSerializer, ComentarioSerializer
from .permissions import EsAdminOEmpleado

# === filtros/paginación ===
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination

# === compras ===
from compras.serializers import CompraSerializer
from compras.permissions import EsCliente


class VideojuegoFilter(django_filters.FilterSet):
    min_precio = django_filters.NumberFilter(field_name='precio', lookup_expr='gte')
    max_precio = django_filters.NumberFilter(field_name='precio', lookup_expr='lte')
    min_fecha = django_filters.DateFilter(field_name='fecha_lanzamiento', lookup_expr='gte')
    max_fecha = django_filters.DateFilter(field_name='fecha_lanzamiento', lookup_expr='lte')

    class Meta:
        model = Videojuego
        fields = []


class DefaultPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# === Videojuegos CRUD ===
class VideojuegoViewSet(ModelViewSet):
    queryset = Videojuego.objects.all()
    serializer_class = VideojuegoSerializer
    permission_classes = [EsAdminOEmpleado]

    # filtros + búsqueda + ordenación + paginación
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = VideojuegoFilter
    search_fields = ['titulo']
    ordering_fields = ['precio', 'fecha_lanzamiento', 'stock', 'titulo']
    ordering = ['-fecha_lanzamiento']
    pagination_class = DefaultPagination

    @action(detail=True, methods=['post'], url_path='comprar',
            permission_classes=[IsAuthenticated, EsCliente])
    def comprar(self, request, pk=None):
        """
        POST /api/videojuegos/{id}/comprar/
        Body: {"cantidad": N}
        """
        data = {
            'videojuego': pk,
            'cantidad': request.data.get('cantidad'),
        }
        serializer = CompraSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        compra = serializer.save()
        return Response(CompraSerializer(compra).data, status=status.HTTP_201_CREATED)


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
