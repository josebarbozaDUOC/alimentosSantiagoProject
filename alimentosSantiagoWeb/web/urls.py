from django.urls import path
from .views import home, registro, agregar_producto, listar_productos, modificar_producto, \
    eliminar_producto, perfil_usuario, \
    carrito_compras, agregar_a_carrito, eliminar_producto_carrito, pagar, restar_cantidad, sumar_cantidad, \
    opciones_pedido, pedido_programado, pedido_metodo_pago, confirmacion_pedido, pedido_entregado, \
    estadisticas, contacto, contacto_empresas, proveedor, repartidor, permisos
    

# arriba importar cada view
# aqui van las rutas para cada html
# la ruta siempre debe terminar con /

urlpatterns = [
    path('', home, name="home"),
    path('registro/', registro, name="registro"),
    path('agregar-producto/', agregar_producto, name="agregar_producto"),
    path('listar-productos/', listar_productos, name="listar_productos"),
    path('modificar-producto/<id>/', modificar_producto, name="modificar_producto"),
    path('eliminar-producto/<id>/', eliminar_producto, name="eliminar_producto"),
    path('perfil-usuario/', perfil_usuario, name="perfil_usuario"),
    path('agregar-a-carrito/<id>/', agregar_a_carrito, name="agregar_a_carrito"),
    path('carrito-compras/', carrito_compras, name="carrito_compras"),
    path('eliminar-producto-carrito/<id>/', eliminar_producto_carrito, name="eliminar_producto_carrito"),
    path('restar-cantidad/<id>/', restar_cantidad, name="restar_cantidad"),
    path('sumar-cantidad/<id>/', sumar_cantidad, name="sumar_cantidad"),
    path('opciones-pedido/<bool>/', opciones_pedido, name="opciones_pedido"),
    path('pedido-programado/<bool>/', pedido_programado, name="pedido_programado"),
    path('pagar', pagar, name="pagar"),
    path('pedido-metodo-pago/<id>/', pedido_metodo_pago, name="pedido_metodo_pago"),
    path('confirmacion-pedido', confirmacion_pedido, name="confirmacion_pedido"),
    path('pedido-entregado/<id>/', pedido_entregado, name="pedido_entregado"),
    path('estadisticas', estadisticas, name="estadisticas"),
    path('contacto', contacto, name="contacto"),
    path('contacto-empresas', contacto_empresas, name="contacto_empresas"),
    path('proveedor', proveedor, name="proveedor"),
    path('repartidor', repartidor, name="repartidor"),
    path('permisos', permisos, name="permisos"),
]


