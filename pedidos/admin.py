from django.contrib import admin
from .models import Cliente, Articulo, Pedido, LineaPedido 

admin.site.register(Cliente)
admin.site.register(Articulo)
admin.site.register(Pedido)
admin.site.register(LineaPedido)
