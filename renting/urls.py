from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConfiguracionView, MaquinariaViewSet, RegistroClienteView, CarroArriendoView, CheckoutView, MisContratosView, ContratoEstadoView, ServicioExternoViewSet
from .serializers import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'maquinarias', MaquinariaViewSet, basename='maquinarias')
router.register(r'servicios', ServicioExternoViewSet, basename='servicios')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/registro/', RegistroClienteView.as_view(), name='registro'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('carro-arriendo/', CarroArriendoView.as_view(), name='carro-arriendo'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('mis-contratos/', MisContratosView.as_view(), name='mis-contratos'),
    path('configuracion/', ConfiguracionView.as_view(), name='configuracion'),
    path('contratos/<int:pk>/estado/', ContratoEstadoView.as_view(), name='contrato-estado'),
]
