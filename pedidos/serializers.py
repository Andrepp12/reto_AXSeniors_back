from rest_framework import serializers
from .models import Cliente, Articulo, Pedido, LineaPedido

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'rut_dni'] 

class ArticuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articulo
        fields = ['id', 'codigo', 'nombre', 'precio_unitario']

class LineaPedidoSerializer(serializers.ModelSerializer):
    articulo_details = ArticuloSerializer(source='articulo', read_only=True) 

    class Meta:
        model = LineaPedido
        fields = ['id', 'articulo', 'cantidad', 'precio_unitario', 'porcentaje_descuento', 'importe_linea', 'articulo_details']
        read_only_fields = ['importe_linea', 'articulo_details'] 

class PedidoSerializer(serializers.ModelSerializer):

    lineapedido_set = LineaPedidoSerializer(many=True) # 'many=True' porque es una lista de líneas

    numero_pedido = serializers.IntegerField(source='id', read_only=True) # Muestra el ID como numero_pedido, solo lectura

    cliente_details = ClienteSerializer(source='cliente', read_only=True)

    class Meta:
        model = Pedido
        fields = ['id', 'numero_pedido', 'cliente', 'fecha_pedido', 'fecha_entrega', 'estado', 'notas','total_pedido', 'lineapedido_set', 'cliente_details'] 
        read_only_fields = ['id', 'numero_pedido', 'cliente_details','total_pedido'] # ID y numero_pedido son autogenerados/basados en ID


    def create(self, validated_data):
        # Extrae los datos de las líneas anidadas
        lineas_data = validated_data.pop('lineapedido_set')
        # Crea el objeto Pedido (sin las líneas aún)
        pedido = Pedido.objects.create(**validated_data)
        # Crea las líneas del pedido y asócialas al pedido recién creado
        for linea_data in lineas_data:
             LineaPedido.objects.create(pedido=pedido, **linea_data) # Esto funciona si validated_data ya tiene la instancia del Articulo

        return pedido

    def update(self, instance, validated_data):
        # Extrae los datos de las líneas anidadas (puede que no siempre vengan)
        lineas_data = validated_data.pop('lineapedido_set', None)

        # Actualiza los campos de la cabecera del pedido
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Lógica para actualizar/crear/eliminar líneas:
        if lineas_data is not None:
            # Identificar líneas existentes (con ID), actualizarlas; identificar líneas nuevas (sin ID), crearlas; identificar IDs de líneas existentes que NO están en los datos recibidos, eliminarlas. (Más complejo, requiere IDs en los datos de entrada)
            existing_line_ids = [linea.id for linea in instance.lineapedido_set.all()]
            incoming_line_ids = [linea.get('id') for linea in lineas_data if linea.get('id') is not None]

            # Eliminar líneas que ya no están
            for line_id in existing_line_ids:
                if line_id not in incoming_line_ids:
                    LineaPedido.objects.get(id=line_id).delete()

            # Crear o actualizar líneas
            for linea_data in lineas_data:
                line_id = linea_data.get('id', None)
                if line_id is None: # Es una línea nueva
                    LineaPedido.objects.create(pedido=instance, **linea_data)
                else: # Es una línea existente, actualizarla
                    linea_instance = LineaPedido.objects.get(id=line_id)
                    for attr, value in linea_data.items():
                         # Evita intentar asignar el ID o el pedido nuevamente
                         if attr not in ['id', 'pedido']:
                            setattr(linea_instance, attr, value)
                    linea_instance.save()


        return instance