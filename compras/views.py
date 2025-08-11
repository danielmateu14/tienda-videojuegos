from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import MethodNotAllowed
from .models import Compra
from .serializers import CompraSerializer
from .permissions import EsCliente, EsPropietarioOStaff

class CompraViewSet(ModelViewSet):
    queryset = Compra.objects.select_related('usuario', 'videojuego')
    serializer_class = CompraSerializer
    http_method_names = ['get', 'post', 'head', 'options', 'delete']  # sin updates

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), EsCliente()]
        if self.action in ('list',):
            return [IsAuthenticated()]
        if self.action in ('retrieve', 'destroy'):
            return [IsAuthenticated(), EsPropietarioOStaff()]
        return [AllowAny()]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if not user.is_authenticated:
            return qs.none()
        rol = getattr(user, 'rol', None)
        if rol == 'cliente':
            return qs.filter(usuario=user)
        # admin/empleado ven todo
        return qs

    # Bloqueamos updates para mantener integridad del histórico
    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed('PUT')

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed('PATCH')
