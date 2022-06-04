from django.urls import path
from .views import home, registro, agregar_producto, listar_productos, modificar_producto, \
    eliminar_producto, favoritos, perfil_usuario, \
    carrito_compras, agregar_a_carrito, eliminar_producto_carrito, pagar, restar_cantidad, sumar_cantidad, \
    opciones_pedido, pedido_programado, fecha, pedido_metodo_pago, confirmacion_pedido
    

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
    path('favoritos/', favoritos, name="favoritos"),
    path('eliminar-producto-carrito/<id>/', eliminar_producto_carrito, name="eliminar_producto_carrito"),
    path('restar-cantidad/<id>/', restar_cantidad, name="restar_cantidad"),
    path('sumar-cantidad/<id>/', sumar_cantidad, name="sumar_cantidad"),
    path('opciones-pedido/<bool>/', opciones_pedido, name="opciones_pedido"),
    path('pedido-programado/<bool>/', pedido_programado, name="pedido_programado"),
    path('pagar', pagar, name="pagar"),
    path('pedido-metodo-pago/<id>/', pedido_metodo_pago, name="pedido_metodo_pago"),
    path('confirmacion-pedido', confirmacion_pedido, name="confirmacion_pedido"),
    path('fecha', fecha, name="fecha"), #fecha es un test de date calendar en test.html
]


