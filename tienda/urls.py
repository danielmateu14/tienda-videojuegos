from django.contrib import admin
from django.urls import path, include
from juegos.urls import router
from usuarios.views import RegistroUsuarioAPIView


urlpatterns = [
    path('admin/', admin.site.urls),
    # Juegos URLs
    path('api/', include(router.urls)),

    # Usuarios URLs
    path('api/usuarios/', include('usuarios.urls')),
    path('api-auth/', include('rest_framework.urls')), 
]

