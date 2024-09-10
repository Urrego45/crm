from . import views
from django.urls import path


urlpatterns = [
    path('listar/', views.ListarAPIView.as_view(), name='listar-api')
]
