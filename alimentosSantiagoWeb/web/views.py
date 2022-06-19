from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, ProductoForm, CarritoForm, ClienteForm
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib.auth import authenticate, login
from .models import Producto, Cliente, Carrito, Carrito_detalle, Tipo_producto, Pedido, Detalle_pedido, Tipo_pago
from django.db.models import Subquery
from django.contrib import messages
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q

#--------------------------------------------HOME PRODUCTOS
def home(request):   
    #Por cada producto verifica su stock, si no queda, producto no está disponible
    prods = Producto.objects.all()
    for p in prods:
        if p.stock <= 0:
            p.disponible = False
            p.save()
    
    categorias  = Tipo_producto.objects.all()
    se_busca = True if request.GET.get('q') != None else False
    #filtro para productos por categoria
    qc = request.GET.get('qc') if request.GET.get('qc') != None else ''
    #filtro para productos por barra busqueda
    q = request.GET.get('q') if request.GET.get('q') != None else qc
    categoria   = Tipo_producto.objects.get(nombre__icontains = qc) if qc != '' else None
    
    #Muestra los productos y se aplica filtro si se requiere
    productos = Producto.objects.filter(
        Q(tipo_producto__nombre__icontains = q) & Q(disponible=True) |
        Q(nombre__icontains = q)                & Q(disponible=True) |
        Q(restaurant__nombre__icontains = q)    & Q(disponible=True)
        )
    
    num_prods = productos.count()
    
    page = request.GET.get('page', 1)
    try:
        paginator = Paginator(productos, 12) #el numero es el maximo de platos por page
        productos = paginator.page(page)
    except:
        raise Http404
    
    data = {
        'entity'        : productos,
        'paginator'     : paginator,
        'categorias'    : categorias,
        'categoria'     : categoria,
        'num_prods'     : num_prods,
        'filtro'        : q,
        'se_busca'      : se_busca
        }
    return render(request, 'web/home.html', data)


#--------------------------------------------USUARIO

def registro(request):
    data = {
        'form': CustomUserCreationForm()
    }
    
    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            user = formulario.save()
            user.refresh_from_db()
            user.save()
            
            password = formulario.cleaned_data.get("password1")
            user = authenticate(username=user.username, password=password)
            login(request, user)
            messages.success(request, "Registro exitoso")
            
            return redirect(to="home")
        data["form"] = formulario
        
    return render(request, 'registration/registro.html', data)
    #return render(request, 'web/navbar.html', data)
    #return render(request, 'registration/registro_modal.html', data)
    

#DESDE EL PERFIL USUARIO, SE DEBIESE MANDAR UNA ALERTA CUANDO SE CUMPLA EL TIEMPO
#DE ENTREGA, ASÍ EL PEDIDO PASA A ENTREGADO, Y AL HISTORIAL
def perfil_usuario(request):
    #request.user es la data del User logeado
    cliente = get_object_or_404(Cliente, pk = request.user.id)
    
###-----------PODRÍA HABER UN BUG SI HAY MÁS DE UN PEDIDO ACTIVO A LA VEZ
    #Busca y rescata algun pedido actual
    if Pedido.objects.filter(cliente = request.user.id, pagado = True, entregado = False):
        pedidos = Pedido.objects.filter(cliente = request.user.id, pagado = True, entregado = False)
        if Detalle_pedido.objects.filter(pedido__in = pedidos):
            pedido_detalle  = Detalle_pedido.objects.filter(pedido__in = pedidos)
            if Producto.objects.filter(id__in=Subquery(pedido_detalle.values('producto'))):
                productos           = Producto.objects.filter(id__in=Subquery(pedido_detalle.values('producto')))
                hay_pedido_activo   = True
                idtab               = 'pedidoOpen'
                dia_entrega_est     = pedidos[0].dia_entrega_est()
                hora_entrega_est    = pedidos[0].hora_entrega_est()
    else: 
        pedidos             = None
        pedido_detalle      = None
        productos           = None
        hay_pedido_activo   = False
        idtab               = 'perfilOpen'
        dia_entrega_est     = ''
        hora_entrega_est    = ''
    
    #Busca y rescata algun pedido ya entregado HISTORIAL
    if Pedido.objects.filter(cliente = request.user.id, pagado = True, entregado = True):
        historial_pedidos = Pedido.objects.filter(cliente = request.user.id, pagado = True, entregado = True).order_by('-id')
        if Detalle_pedido.objects.filter(pedido__in = historial_pedidos):
            historial_pedido_detalle = Detalle_pedido.objects.filter(pedido__in = historial_pedidos)
            if Producto.objects.filter(id__in=Subquery(historial_pedido_detalle.values('producto'))):
                historial_productos = Producto.objects.filter(id__in=Subquery(historial_pedido_detalle.values('producto')))
    else: 
        historial_pedidos           = None
        historial_pedido_detalle    = None
        historial_productos         = None
    
    data = {
    'cliente'                   : cliente,
    'form'                      : ClienteForm(instance=cliente),
    'formUser'                  : CustomUserCreationForm(),
    'pedidos'                   : pedidos,
    'pedido_detalle'            : pedido_detalle,
    'productos'                 : productos,
    'historial_pedidos'         : historial_pedidos,
    'historial_pedido_detalle'  : historial_pedido_detalle,
    'historial_productos'       : historial_productos,
    'hay_pedido_activo'         : hay_pedido_activo,
    'idtab'                     : idtab,
    'dia_entrega_est'           : dia_entrega_est,
    'hora_entrega_est'          : hora_entrega_est
    }
    if request.method == 'POST':
        formulario = ClienteForm(data=request.POST, instance=cliente)
        formUser = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid() & formUser.is_valid():
            formulario.save()
            formUser.save()
            messages.success(request, "Perfil modificado correctamente")
        else:
            data['form'] = formulario
            data['formUser'] = formUser
    
    return render(request, 'web/perfil_usuario.html', data)


#--------------------------------------------CRUD PRODUCTOS

def listar_productos(request):
    productos = Producto.objects.all()
    #productos = Producto.objects.filter(disponible=True).order_by('id')
    
    page = request.GET.get('page', 1)
    try:
        paginator = Paginator(productos, 5) #el numero es el maximo de platos por page
        productos = paginator.page(page)
    except:
        raise Http404
    
    data = {
        'entity' : productos,
        'paginator' : paginator
        }
    return render(request, 'web/producto/listar.html', data)

def agregar_producto(request):
    data = {
        'form' : ProductoForm()
    }
    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Producto agregado correctamente")
        else:
            data['form'] = formulario
        
    return render(request, 'web/producto/agregar.html', data)

def modificar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    data = {
        'form': ProductoForm(instance=producto),
        'producto' : producto
    }
    
    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado correctamente")
            return redirect(to='listar_productos')
        data['form'] = formulario
            
    return render(request, 'web/producto/modificar.html', data)

def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    messages.success(request, "Eliminado correctamente")
    return redirect(to='listar_productos')


#--------------------------------------------CARRITO DE COMPRAS

#filtro para sacar todas las id producto del carrito 
# donde el id cliente sea la del usuario actual
#luego hacer una subquery para sacar los productos del carrito
def carrito_compras(request):
    carrito         = get_object_or_404(Carrito, pk = request.user.id)
    carrito_detalle = Carrito_detalle.objects.filter(carrito = request.user.id)
    productos       = Producto.objects.filter(id__in=Subquery(carrito_detalle.values('producto')))
    
    #si carrito esta vacio, reiniciar las variables, envio=True, etc
    carrito.reiniciar_valores()
        
    hora_entrega_est    = carrito.hora_entrega_est()
    dia_entrega_est     = carrito.dia_entrega_est()
    
    if not carrito.es_envio_domicilio:
        carrito.costo_envio = 0
    else:
        carrito.costo_envio = 1000
    
    #calculo actualizado de carrito , hay sumatorias
    for p in productos:
        for c in carrito_detalle:
            if c.producto.id == p.id:
                c.subtotal = p.precio * c.cantidad_producto
                carrito.numero_productos += c.cantidad_producto
                carrito.subtotal += p.precio * c.cantidad_producto
    carrito.total = carrito.subtotal + carrito.costo_envio - carrito.descuento
    #carrito.comprobar_fechas()
    carrito.save()
    
    data = {
        'form'              : CarritoForm(instance=carrito),
        'productos_carrito' : carrito_detalle,
        'productos'         : productos,
        'carrito'           : carrito,
        'dia_entrega_est'   : dia_entrega_est,
        'hora_entrega_est'  : hora_entrega_est
    }
    
    if request.method == 'POST':
        formulario = CarritoForm(data=request.POST, instance=carrito)
        if formulario.is_valid():
            carrito.comprobar_fechas()
            formulario.save()
            messages.success(request, f" fecha_entrega_estimada: {carrito.fecha_entrega_estimada}")
        else:
            messages.success(request, "Por favor indique fecha y hora programada para su envio")
            data["form"] = formulario
            
    return render(request, 'web/carrito.html', data)

def agregar_a_carrito(request, id):
    producto_obtenido   = get_object_or_404(Producto, disponible=True, id=id)
    carrito             = get_object_or_404(Carrito, pk = request.user.id)
    carrito_detalle     = Carrito_detalle.objects.filter(carrito = request.user.id)
    
###-----------DEBE PODER COMPARAR EL STOCK DEL PRODUCTO PRIMERO
    #Validación si existe producto en carrito, SUMA UNO MÁS
    if Carrito_detalle.objects.filter(carrito = request.user.id, producto = producto_obtenido.pk):
        messages.success(request, f"Se ha agregado un(a) {producto_obtenido} más al carrito")
        producto_en_carrito = Carrito_detalle.objects.get(carrito = request.user.id, producto = producto_obtenido.pk)
        producto_en_carrito.cantidad_producto += 1
        producto_en_carrito.save()
    else:
        carrito_detalle = Carrito_detalle(
            carrito             = carrito, 
            producto            = producto_obtenido, 
            cantidad_producto   = 1,
            subtotal            = producto_obtenido.precio)
        carrito_detalle.save()
        messages.success(request, f"Se ha agregado {producto_obtenido} al carrito")
    
    #return render(request, 'web/home.html')
    return redirect(to='/')

def eliminar_producto_carrito(request, id):
    producto    = get_object_or_404(Producto, disponible=True, id=id)
    carrito     = get_object_or_404(Carrito, pk = request.user.id)
    carrito_detalle = Carrito_detalle.objects.get(carrito = carrito, producto = producto)
    carrito_detalle.delete()
    messages.success(request, "Producto eliminado del carrito :c")
    return redirect(to='carrito_compras')


def restar_cantidad(request, id):
    producto = get_object_or_404(Producto, disponible=True, id=id)
    carrito = get_object_or_404(Carrito, pk = request.user.id)
    producto_en_carrito = Carrito_detalle.objects.get(carrito = carrito, producto = producto)
    producto_en_carrito.cantidad_producto -= 1
    producto_en_carrito.save()
    messages.success(request, "Producto -1")
    return redirect(to='carrito_compras')

def sumar_cantidad(request, id):
###-----------DEBE PODER COMPARAR EL STOCK DEL PRODUCTO PRIMERO
    
    producto = get_object_or_404(Producto, disponible=True, id=id)
    carrito = get_object_or_404(Carrito, pk = request.user.id)
    producto_en_carrito = Carrito_detalle.objects.get(carrito = carrito, producto = producto)
    producto_en_carrito.cantidad_producto += 1
    producto_en_carrito.save()
    messages.success(request, "Producto +1")
    return redirect(to='carrito_compras')

def opciones_pedido(request, bool):
    carrito = get_object_or_404(Carrito, pk = request.user.id)
    carrito.es_envio_domicilio = bool
    carrito.save()
    messages.success(request, f"envio domicilio: {carrito.es_envio_domicilio}")
    return redirect(to='carrito_compras')

def pedido_programado(request, bool):
    carrito = get_object_or_404(Carrito, pk = request.user.id)
    carrito.es_programado = bool
    carrito.save()
    messages.success(request, f"pedido programado: {carrito.es_programado} \
        fecha_entrega_estimada: {carrito.fecha_entrega_estimada}")
    return redirect(to='carrito_compras')


#--------------------------------------------PAGO

def pagar(request):
    cliente         = get_object_or_404(Cliente, pk = request.user.id)
    carrito         = get_object_or_404(Carrito, pk = request.user.id)
    carrito_detalle = Carrito_detalle.objects.filter(carrito = request.user.id)
    productos       = Producto.objects.filter(id__in=Subquery(carrito_detalle.values('producto')))
    metodo_pago     = Tipo_pago.objects.get(id=1)
    hora_compra     = datetime.now()
    
    #-----PEDIDO
    #se busca en tabla pedido, si no existe un pedido que corresponda a lo del carrito
    #que me cree un pedido nuevo, con la mayoria de datos del carrito
    #pero mientras está en espera de pago
    if Pedido.objects.filter(cliente = cliente, pagado = False, codigo = carrito.codigo):
        #Obtener el pedido y los pedido_detalle correspondiente
        pedido = get_object_or_404(Pedido, cliente = cliente, pagado = False, codigo = carrito.codigo)
        #Actualizar el pedido con los datos del carrito
        pedido.es_envio_domicilio      = carrito.es_envio_domicilio
        pedido.costo_envio             = carrito.costo_envio
        pedido.subtotal                = carrito.subtotal
        pedido.total                   = carrito.total
        pedido.num_productos           = carrito.numero_productos
        pedido.fecha_compra            = hora_compra
        pedido.tiempo_entrega_est      = carrito.tiempo_entrega_estimado
        pedido.fecha_entrega_estimada  = carrito.fecha_entrega_estimada
        pedido.es_programado           = carrito.es_programado
        pedido.fecha_programada        = carrito.fecha_programada
    else:
        #Se crea un nuevo pedido a partir del carrito
        pedido = Pedido(
            cliente                 = cliente, 
            codigo                  = carrito.codigo,
            metodo_pago             = metodo_pago, 
            es_envio_domicilio      = carrito.es_envio_domicilio,
            costo_envio             = carrito.costo_envio,
            subtotal                = carrito.subtotal,
            total                   = carrito.total,
            num_productos           = carrito.numero_productos,
            fecha_compra            = carrito.pedido_fecha_compra(),
            pagado                  = False,
            tiempo_entrega_est      = carrito.tiempo_entrega_estimado,
            fecha_entrega_estimada  = carrito.fecha_entrega_estimada,
            es_programado           = carrito.es_programado,
            fecha_programada        = carrito.fecha_programada,
            fecha_entregado         = None,
            entregado               = False)
    pedido.pedido_fecha_compra()
    pedido.save()
    
    #-----PEDIDO_DETALLE
    for p in productos:
            for c in carrito_detalle:
                if c.producto.id == p.id:
                    #coincide carrito con producto
                    #si en el detalle_pedido hay un producto con esa id, actualizar
                    if Detalle_pedido.objects.filter(pedido = pedido, producto=p): 
                        pedido_detalle = get_object_or_404(Detalle_pedido,pedido = pedido, producto = p)
                        pedido_detalle.cantidad_producto = c.cantidad_producto
                        pedido_detalle.subtotal = c.subtotal
                        pedido_detalle.save()
                    else:
                        #si no, crear
                        pedido_detalle_nuevo = Detalle_pedido(
                                    pedido = pedido,
                                    producto = p,
                                    cantidad_producto = c.cantidad_producto,
                                    subtotal = c.subtotal)
                        pedido_detalle_nuevo.save()
                        
    pedido_detalle = Detalle_pedido.objects.filter(pedido = pedido)
    #si en el pedido detalle quedó algun producto que ya se quitó del carrito, que se borre de aca tbn
    for d in pedido_detalle:
        prod = get_object_or_404(Producto, id = d.producto.id)
        if not Carrito_detalle.objects.filter(carrito = request.user.id, producto = prod):
            d.delete()
            
    pedido_detalle = Detalle_pedido.objects.filter(pedido = pedido)
    
    data = {
        'productos_carrito' : carrito_detalle,
        'productos'         : productos,
        'carrito'           : carrito,
        'cliente'           : cliente,
        'pedido'            : pedido,
        'pedido_detalle'    : pedido_detalle,
        'carrito_detalle'   : carrito_detalle
    }
    return render(request, 'web/pagar.html', data)


def pedido_metodo_pago(request, id):
    metodo_pago = Tipo_pago.objects.get(id=id)
    carrito     = get_object_or_404(Carrito, pk = request.user.id)
    pedido  = get_object_or_404(Pedido, cliente = request.user.id, pagado = False, codigo = carrito.codigo)
    pedido.metodo_pago = metodo_pago
    pedido.save()
    messages.success(request, f"Método de pago: {pedido.metodo_pago}")
    return redirect(to='pagar')


def confirmacion_pedido(request):
    cliente     = get_object_or_404(Cliente, pk = request.user.id)
    carrito     = get_object_or_404(Carrito, pk = request.user.id)
    pedido      = get_object_or_404(Pedido, cliente = request.user.id, pagado = False, codigo = carrito.codigo)
    detalle     = Detalle_pedido.objects.filter(pedido = pedido)
    productos   = Producto.objects.filter(id__in=Subquery(detalle.values('producto')))
    
    pago_saldo = Tipo_pago.objects.get(id=1)
    #Se updatea el pedido y se confirma el pagado
    pedido.pedido_fecha_compra()
    pedido.pagado = True
    pedido.save()
    
    #Cliente se le descuenta el total de su saldo
    if pedido.metodo_pago == pago_saldo:
        cliente.pagar_con_saldo(pedido.total)
        cliente.save()
    
    #Se vacia el carrito y se borran los productos de carrito detalle
    carrito_detalle = Carrito_detalle.objects.filter(carrito = request.user.id)
    carrito_detalle.delete()
    carrito.vaciar_carrito()
    carrito.save()
    
    #Y HAY QUE RESTAR STOCK A LOS PRODUCTOS COMPRADOS
    for p in productos:
        for d in detalle:
            if d.producto.id == p.id:
                p.restar_stock(d.cantidad_producto)
                p.save()
    
    return redirect(to='perfil_usuario')

def estadisticas(request):
    
    pedidos = Pedido.objects.filter(cliente = request.user.id, pagado = True)
        
    data = {
        'pedidos' : pedidos
    }
    return render(request, 'web/estadisticas/estadisticas.html', data)