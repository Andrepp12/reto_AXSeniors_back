from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import filters 
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend 
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from .models import Cliente, Articulo, Pedido
from .serializers import ClienteSerializer, ArticuloSerializer, PedidoSerializer
from .filters import PedidoFilter


# --- Vista API para Listar Clientes ---
class ClienteListAPIView(generics.ListAPIView):
    queryset = Cliente.objects.all() # Obtiene todos los clientes
    serializer_class = ClienteSerializer # Usa el serializador de Cliente
    # Puedes añadir filtros, paginación, etc. aquí si lo necesitas

# --- Vista API para Listar Artículos ---
class ArticuloListAPIView(generics.ListAPIView):
    queryset = Articulo.objects.all() # Obtiene todos los artículos
    serializer_class = ArticuloSerializer # Usa el serializador de Articulo


class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]

    filterset_class = PedidoFilter
 
    # filterset_fields = ['estado', 'cliente', 'fecha_pedido', 'fecha_entrega']

    ordering_fields = [
        # 'numero_pedido',
        'fecha_pedido',
        'fecha_entrega',
        'estado',
        'total_pedido', # Si 'total_pedido' es una @property o SerializerMethodField en el Serializer, DRF intentará ordenarla en Python (puede ser ineficiente para grandes datasets)
        'cliente__nombre', # Ordenar por el nombre del cliente (asume que 'cliente' es un ForeignKey a un modelo con campo 'nombre')
    ]

    ordering = ['-fecha_pedido'] 

    @action(detail=True, methods=['get']) # detail=True significa que opera sobre una instancia específica (usando pk)
    def generate_pdf(self, request, pk=None): # El pk es el ID del pedido
        try:
            pedido = self.get_object() # Obtiene la instancia del pedido usando el pk de la URL

            # --- Lógica de Generación de PDF (Ejemplo Básico con ReportLab) ---
            # Esto es solo un esqueleto, la lógica real depende de tus necesidades
            response = HttpResponse(content_type='application/pdf')
            # Configurar la cabecera para forzar la descarga del archivo
            response['Content-Disposition'] = f'attachment; filename="pedido_{pedido.id}_detalle.pdf"'

            p = canvas.Canvas(response, pagesize=letter)

            # Añade contenido al PDF
            p.drawString(100, 750, f"Detalle del Pedido #{pedido.id}")
            p.drawString(100, 730, f"Cliente: {pedido.cliente.nombre if pedido.cliente else 'N/A'}")
            p.drawString(100, 710, f"Fecha: {pedido.fecha_pedido.strftime('%Y-%m-%d')}")

            y_position = 650
            p.drawString(100, y_position, "Líneas del Pedido:")
            y_position -= 20

            # Listar líneas de pedido
            for linea in pedido.lineapedido_set.all():
                 importe_linea = linea.importe_linea if hasattr(linea, 'importe_linea') else 'N/A'
                 p.drawString(120, y_position, f"- {linea.articulo.nombre} (x{linea.cantidad}) - Importe: {importe_linea:.2f}")
                 y_position -= 15


            p.drawString(100, y_position - 20, f"Total Pedido: {pedido.total_pedido:.2f}")

            p.showPage() # Finaliza la página
            p.save() # Guarda el contenido en la respuesta HTTP

            return response # Devuelve la respuesta HTTP con el PDF

        except Pedido.DoesNotExist:
            # Si el pedido no existe
            from rest_framework import status
            return Response({'detail': 'Pedido no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Manejar otros posibles errores durante la generación del PDF
            from rest_framework import status
            return Response({'detail': f'Error al generar PDF: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



