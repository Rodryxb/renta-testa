from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from core.views import carro_view, index_view, auth_view, dashboard_view, maquinas_view, materiales_view, otros_servicios_view, custom_404_view, producto_detalle_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('renting.urls')),
    
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    path('', index_view, name='index'),
    path('auth/', auth_view, name='auth'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('carro/', carro_view, name='carro'),
    path('maquinas/', maquinas_view, name='maquinas'),
    path('materiales/', materiales_view, name='materiales'),
    path('producto/<int:pk>/', producto_detalle_view, name='producto_detalle'),
    path('servicios/', otros_servicios_view, name='servicios'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    re_path(r'^.*$', custom_404_view),
]

handler404 = 'core.views.custom_404_view'
