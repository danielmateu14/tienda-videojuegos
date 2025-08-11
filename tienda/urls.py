from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Juegos: incluye router (videojuegos) + rutas manuales (comentarios, etc.)
    path('api/', include('juegos.urls')),

    # Usuarios (registro, login, refresh, hola, etc.)
    path('api/usuarios/', include('usuarios.urls')),

    # Compras
    path('api/', include('compras.urls')),

    # Browsable API login/logout
    path('api-auth/', include('rest_framework.urls')),
]
