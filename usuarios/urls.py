from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegistroUsuarioAPIView

urlpatterns = [
    path('registro/', RegistroUsuarioAPIView.as_view(), name='registro-usuario'),

    # Login (token access + refresh)
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
