import django_filters
from .models import Pedido 

class PedidoFilter(django_filters.FilterSet):

    cliente_nombre = django_filters.CharFilter(field_name='cliente__nombre', lookup_expr='icontains')

    class Meta:
        model = Pedido
        fields = {
            'estado': ['exact'],
            'fecha_pedido': ['exact', 'gte', 'lte'], # filtros por fecha (exacta, mayor o igual, menor o igual)
            'fecha_entrega': ['exact', 'gte', 'lte'],
        }
