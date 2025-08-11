from rest_framework import permissions

class EsCliente(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and
            getattr(request.user, 'rol', None) == 'cliente'
        )

class EsPropietarioOStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        if getattr(request.user, 'rol', None) in ('admin', 'empleado'):
            return True
        return obj.usuario_id == request.user.id
