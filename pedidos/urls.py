from django.urls import path, include
from rest_framework.routers import DefaultRouter 
from . import views 

router = DefaultRouter()
router.register(r'pedidos', views.PedidoViewSet) 

urlpatterns = [
    path('', include(router.urls)),
    path('clientes/', views.ClienteListAPIView.as_view(), name='cliente-list'),
    path('articulos/', views.ArticuloListAPIView.as_view(), name='articulo-list'),


]