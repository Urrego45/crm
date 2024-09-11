from . import views
from django.urls import path


urlpatterns = [
    path('sincronizar/', views.SincronizarVulnerabilidadesAPIView.as_view(), name='listar-api'),

    # API
    path('vulnerabilidad/', views.VulnerabilidadesListAPIView.as_view(), name='listar-api'),
    path('descripcion/', views.DescripcionListAPIView.as_view(), name='listar-api'),
    path('metrica/', views.MetricaListAPIView.as_view(), name='listar-api'),
    path('dato-metrica/', views.DatoMetricaListAPIView.as_view(), name='listar-api'),
    path('solucion-vulnerabilidad/', views.SolucionVulnerabilidadListCreateAPIView.as_view(), name='listar-api'),

    path('vulnerabilidad-sin-soluciones/', views.VulnerabilidadesSinSolucionListAPIView.as_view(), name='listar-api'),
    path('vulnerabilidad-severidad/', views.VulnerabilidadeSeveridadListAPIView.as_view(), name='listar-api'),

]
