from rest_framework.permissions import BasePermission, SAFE_METHODS

class EsAdminOEmpleado(BasePermission):
    """
    Permite solo a usuarios con rol admin o empleado hacer cambios.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True
        return (
            request.user.is_authenticated and
            request.user.rol in ['admin', 'empleado']
        )
