from . import views
from django.urls import path


urlpatterns = [
    path('sincronizar/', views.SincronizarVulnerabilidadesAPIView.as_view(), name='sincronizar-api'),

    # API
    path('vulnerabilidad/', views.VulnerabilidadesListAPIView.as_view(), name='vulnerabilidad-api'),
    path('descripcion/', views.DescripcionListAPIView.as_view(), name='descripcion-api'),
    path('metrica/', views.MetricaListAPIView.as_view(), name='metrica-api'),
    path('dato-metrica/', views.DatoMetricaListAPIView.as_view(), name='dato-metrica-api'),
    path('solucion-vulnerabilidad/', views.SolucionVulnerabilidadListCreateAPIView.as_view(), name='solucion-vulnerabilidad-api'),

    path('vulnerabilidad-sin-soluciones/', views.VulnerabilidadesSinSolucionListAPIView.as_view(), name='vulnerabilidad-sin-soluciones-api'),
    path('vulnerabilidad-severidad/', views.VulnerabilidadeSeveridadListAPIView.as_view(), name='vulnerabilidad-severidad-api'),

]
