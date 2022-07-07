from distutils.command.upload import upload
import email
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User #para acceder al user de la base de datos
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, timedelta
import uuid

# Create your models here.

#----------------------FUNCIONES ESPECIALES
def pedido_espera():
    return datetime.now() + timedelta(minutes=30)
def pedido_ahora():
    return datetime.now() + timedelta(minutes=0)
def ajuste_hora_chile(fecha):
    fecha -= timedelta(hours=4)
    return fecha.strftime('%H:%M')
def ajuste_hora_chile_segs(fecha):
    fecha -= timedelta(hours=4)
    return fecha.strftime('%H:%M:%S')

def create_cod():
    cod = str(uuid.uuid1())
    return cod

#------------------------------MODELO PRODUCTO
class Restaurant(models.Model):
    nombre      = models.CharField(max_length=50)
    direccion   = models.CharField(max_length=100, blank=True, null=True)
    #tiempo_promedio_preparacion
    def __str__(self):
        return self.nombre

class Tipo_producto(models.Model):
    nombre = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre

class Tipo_menu(models.Model):
    nombre = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    restaurant          = models.ForeignKey(Restaurant, on_delete=models.PROTECT)
    tipo_producto       = models.ForeignKey(Tipo_producto, on_delete=models.PROTECT)
    tipo_menu           = models.ForeignKey(Tipo_menu, on_delete=models.PROTECT)
    nombre              = models.CharField(max_length=50)
    precio              = models.IntegerField()
    descripcion         = models.TextField()
    imagen              = models.ImageField(upload_to="platos", null=True)
    fecha_publicacion   = models.DateTimeField(default=timezone.now)
    stock               = models.IntegerField(null=True)
    disponible          = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre
    
    def restar_stock(self, resta):
        self.stock -= resta

#------------------------------MODELO CLIENTE
class Avatar(models.Model):
    nombre              = models.CharField(max_length=50)
    avatar              = models.ImageField(upload_to="avatar-cliente", null=True)
    def __str__(self):
        return self.nombre

class Cliente(models.Model):

    #toma datos de la base, tabla auth_user
    #debiese ser el user actualmente logeado
    #id_user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    
    #al importar el User de auth.models, ahora acceso directamente
    #id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    #nombre = models.ForeignKey(User.first_name, on_delete=models.CASCADE)
    #apellido = models.ForeignKey(User.last_name, on_delete=models.CASCADE)
    #email = models.ForeignKey(User.email, on_delete=models.CASCADE)
    
    #al usar el OneToOneField se tiene acceso a todo del user, y a su vez el user a todo del cliente
    user                = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    saldo               = models.IntegerField(default=0)
    direccion           = models.CharField(max_length=100, blank=True, null=True)
    rut                 = models.CharField(max_length=10, blank=True, null=True)
    numero_telefono     = models.IntegerField(blank=True, null=True)
    fecha_nacimiento    = models.DateField(blank=True, null=True)
    avatar              = models.ForeignKey(Avatar, on_delete=models.PROTECT, null=True)
        
    #cuando se crea/registra un user, a la vez se crea el cliente
    @receiver(post_save, sender=User)
    def update_cliente_signal(sender, instance, created, **kwargs):
        if created:
            Cliente.objects.create(user=instance)
        instance.cliente.save()
        
    #to string | accede al nombre del user
    def __str__(self):
        return self.user.username
    
    #me debe dar la ID
    def user_cliente(self):
        return self.user.pk
    
    #cargar más saldo a la cuenta
    def cargar_saldo(self, saldo):
        self.saldo += saldo
        return self.saldo
    
    #pagar con saldo de la cuenta
    ######AGREGAR
    #validaciones:
    #el saldo no puede ser menor a cero
    #el pago no debe superar el saldo
    def pagar_con_saldo(self, pago):
        self.saldo -= pago
        #return self.saldo

#------------------------------MODELO CARRITO
#cada carrito es unico a cada cliente
class Carrito(models.Model):
    cliente                 = models.OneToOneField(Cliente, on_delete=models.CASCADE, primary_key=True)
    codigo                  = models.CharField(max_length=50, default=create_cod) 
    numero_productos        = models.IntegerField(default=0)
    descuento               = models.IntegerField(default=0)
    subtotal                = models.IntegerField(default=0)
    total                   = models.IntegerField(default=0)
    
    es_envio_domicilio      = models.BooleanField(default=True)     #false= retiro en local
    costo_envio             = models.IntegerField(default=0)
    tiempo_entrega_estimado = models.IntegerField(default=30)       #30min
    fecha_entrega_estimada  = models.DateTimeField(default=pedido_espera)
    
    es_programado           = models.BooleanField(default=False)
    fecha_programada        = models.DateTimeField(blank=True, null=True, default=pedido_espera) #opcional
    
    #------------------------------FUNCIONES DEL CARRITO
    def vaciar_carrito(self):
        self.codigo                     = create_cod()
        self.numero_productos           = 0
        self.descuento                  = 0
        self.subtotal                   = 0
        self.total                      = 0
        self.es_envio_domicilio         = True
        self.costo_envio                = 0
        self.tiempo_entrega_estimado    = 30
        self.fecha_entrega_estimada     = pedido_espera()
        self.es_programado              = False
        self.fecha_programada           = None
    
    def reiniciar_valores(self):
        self.numero_productos=0
        self.subtotal=0
        self.total=0
        self.comprobar_fechas()
    
    def comprobar_fechas(self):
        self.fecha_entrega_estimada = pedido_espera()
        if self.fecha_programada == None:
            self.fecha_programada = pedido_espera()
        if self.es_programado:
            if self.fecha_programada.strftime('%d%m%Y%H%M') <=  pedido_espera().strftime('%d%m%Y%H%M'):
                self.fecha_programada = pedido_espera()
            self.fecha_entrega_estimada = self.fecha_programada
        else:
            self.fecha_entrega_estimada = pedido_espera()
            self.fecha_programada = pedido_espera()
            self.fecha_programada = None
        
    def dia_entrega_est(self):
        if self.fecha_entrega_estimada.strftime('%d') == datetime.now().strftime('%d'):
            return 'Hoy'
        return 'Mañana'
        
    def hora_entrega_est(self):
        return self.fecha_entrega_estimada.strftime('%H:%M')
    
    def pedido_fecha_compra(self):
        return pedido_ahora()
    
    #cuando se crea/registra un user, a la vez se crea el carrito
    @receiver(post_save, sender=Cliente)
    def update_cliente_signal(sender, instance, created, **kwargs):
        if created:
            Carrito.objects.create(cliente=instance)
        instance.carrito.save()

# Carrito_compras (user, producto, cant)    #trae todos los productos, where id del user
class Carrito_detalle(models.Model):
    carrito             = models.ForeignKey(Carrito, on_delete=models.PROTECT)
    producto            = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad_producto   = models.IntegerField(default=1)
    subtotal            = models.IntegerField(default=0)
    
    #funcion para calcular el subtotal en base a la cant
    def sacar_subtotal(self):
        #self.subtotal = self.subtotal*self.cantidad_producto
        #self.subtotal = producto.precio * self.cantidad_producto
        return self.subtotal
    
    #debiese hacer un def para validar la cantidad no supere el stock del producto comparando id

#------------------------------MODELO PEDIDO
class Tipo_pago(models.Model):
    nombre                  = models.CharField(max_length=50)   #saldo, tarjeta, efectivo
    def __str__(self):
        return self.nombre

class Envio(models.Model):
    nombre                  = models.CharField(max_length=50)   #cerca, lejos
    descripcion             = models.TextField()                #está a menos de 500mts, a más de 2000mts
    tiempo_promedio_entrega = models.IntegerField(default=30)   #30 min, 40min
    costo                   = models.IntegerField()             #1000, 2000
    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    #va de la mano con Detalle_pedido
    cliente                 = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    codigo                  = models.CharField(max_length=50, default=create_cod) 
    metodo_pago             = models.ForeignKey(Tipo_pago, on_delete=models.PROTECT)

    es_envio_domicilio      = models.BooleanField(default=True)
    costo_envio             = models.IntegerField(default=0)

    subtotal                = models.IntegerField()
    total                   = models.IntegerField()
    num_productos           = models.IntegerField(default=0)
    
    fecha_compra            = models.DateTimeField(default=pedido_ahora)
    pagado                  = models.BooleanField(default=False)        #falso: espera de pago | true: cliente pagó
    tiempo_entrega_est      = models.IntegerField(default=30)          #30min
    fecha_entrega_estimada  = models.DateTimeField(default=pedido_espera)
        
    es_programado           = models.BooleanField(default=False)
    fecha_programada        = models.DateTimeField(blank=True, null=True, default=pedido_espera) #opcional
        
    fecha_entregado         = models.DateTimeField(blank=True, null=True, default=pedido_espera)
    entregado               = models.BooleanField(default=False)
    
    def pedido_entregado(self):
        self.entregado = True
        self.fecha_entregado = pedido_ahora()
    
    def pedido_fecha_compra(self):
        self.fecha_compra = pedido_ahora()
    
    def dia_entrega_est(self):
        if self.fecha_entrega_estimada.strftime('%d/%m/%Y') == datetime.now().strftime('%d/%m/%Y'):
            return 'Hoy'
        else: return self.fecha_entrega_estimada
    
    def hora_entrega_est(self):
        a = ajuste_hora_chile(self.fecha_entrega_estimada)
        return a
    
    def reloj_fecha(self):
        return self.fecha_entrega_estimada.strftime('%d-%m-%Y')
    def reloj_hora(self):
        b = ajuste_hora_chile_segs(self.fecha_entrega_estimada)
        return b
    
    ##calificación del pedido | estrellitas
    #to string ???????????????????

class Detalle_pedido(models.Model):
    #va de la mano con Pedido
    pedido              = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto            = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad_producto   = models.IntegerField()
    subtotal            = models.IntegerField()

#------------------------------PREVEEDOR, REPARTIDOR, CLI_EMPRESA
class Proveedor(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant      = models.ForeignKey(Restaurant, on_delete=models.PROTECT)
    #direccion_local = models.CharField(max_length=100)
    #rut             = models.CharField(max_length=10)       ####?????
    
    def __str__(self):
        return self.user.username

class Repartidor(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    en_reparto      = models.BooleanField(default=False)
    #rut             = models.CharField(max_length=10)       ####?????
    
    def __str__(self):
        return self.user.username

class Empresa_convenio(models.Model):
    nombre                  = models.CharField(max_length=50)
    rut                     = models.CharField(max_length=11)
    direccion               = models.CharField(max_length=80)
    email                   = models.CharField(max_length=30)
    telefono                = models.IntegerField(default=0)
    cant_trabajadores       = models.IntegerField(default=0)
    gasto_total_mensual     = models.IntegerField(default=0)
    
    def __str__(self):
        return self.user.username

class Cliente_convenio(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    empresa         = models.ForeignKey(Empresa_convenio, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username

'''
#crear tabla:
##### Contacto_mensajes
##### Direccion_local o Direcciones         #para mantener multiples direcciones
##### Menu (dias_semana[], producto[])      #sería como un google calendar?
'''