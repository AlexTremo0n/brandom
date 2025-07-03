from django.db import models
from django.utils import timezone
import os
from django.dispatch import receiver
from django.db.models.signals import post_migrate
from django.contrib.auth.models import User
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

productos = {
    101:['Estandar Twin','Agrega',['2 personas','Cama King'],80000,'estandartwin.jpg'],
    102:['Suite Doble','No Agrega',['1 persona','Cama King'],60000,'suitedoble.jpg'],
    103:['Suite Individual','Agrega',['3 personas','Suite'],80000,'suiteindividual.jpg'],
    104:['Habitacion Comunicada','Agrega',['4 personas','Estandar'],120000,'piezacomunicada.jpg'],

}

info = {
    101:['Fotos','Agrega',['2 personas','Cama King'],80000,'hotel.jpg'],
    102:['Comentarios','No Agrega',['1 persona','Cama King'],60000,'comentarios.jpg'],
    103:['Disponibilidad','Agrega',['3 personas','Suite'],80000,'disponible.jpg'],

}

fotos = {
    100:['Estandar twin','maravillosa vista al mar, Superficie total alreedor de 15 mts, altura del techo de 3.5 a 4 mts, ancho de la habitacion de 5 mts',['2 personas','2 baños,'],180000,'estandartwin.jpg'],
    101:['Suite Doble','Con una superficie total de alrededor de 13 metros cuadrados, esta habitación ofrece un espacio para relajarte y disfrutar de la brisa marina, altura de techo que oscila entre 3.5 y 4 metros, El ancho de la habitación, de 5 metros, te brinda un espacio cómodo y funcional',['2 persona','2 baños,','inmuebles importados'],80000,'suitedoble.jpg'],
    102:['Suite individual','Una habitacion en particular de 6 mts cuadrados, un amplio espacio pero perfecto para ponerte comodo, cuenta con internet y television',['1 persona',' cama simple, piso flotante'],60000,'suiteindividual.jpg'],
    103:['Habitacion comunicada','la siguiente habitacion cuenta con dos camas de 1 plaza y media cada una, sabanas y frazadas de seda, y ademas cuenta con calefaccion ',['2 personas','Habitacion comunicada'],110000,'piezacomunicada.jpg'],

}

# hoteles.py
pais = {
    1: ['Estados Unidos', '', '', 'eeuu.jpg', [1, 2, 3]],
    2: ['Mexico', '', '', 'mexico.jpg', [4, 5, 6]],
    3: ['Chile', '', '', 'chile.jpg', [7, 8, 9]],
}

ciudades = {
    1: ['Washington', 'Norteamérica', 'Washington', 'washington.jpg', [1, 2, 3]],
    2: ['Nueva York', 'Norteamérica', 'Nueva York', 'nuevayork.jpg', [4, 5, 6]],
    3: ['Miami', 'Norteamérica', 'Miami', 'miami.jpg', [7, 8, 9]],
    4: ['Ciudad de Mexico', 'Norteamérica', 'Ciudad de Mexico', 'ciudaddemexico.jpg', [10, 11, 12]],
    5: ['Guadalajara', 'Norteamérica', 'Guadalajara', 'guadalajara.jpg', [13, 14, 15]],
    6: ['Cancún', 'Norteamérica', 'Cancún', 'cancun.jpg', [16, 17, 18]],
    7: ['Santiago', 'Sudamérica', 'Santiago', 'santiago.jpg', [19, 20, 21]],
    8: ['Valparaíso', 'Sudamérica', 'Valparaíso', 'valparaiso.jpg', [22, 23, 24]],
    9: ['La Serena', 'Sudamérica', 'La Serena', 'laserena.jpg', [25, 26, 27]],
}

hoteles = {
    1: ['EE.UU.', 'Washington', 'Hotel Estrella del Norte', 'hotel1.webp', 150],
    2: ['EE.UU.', 'Washington', 'Hotel Luna de Plata', 'hotel2.jpg'],
    3: ['EE.UU.', 'Washington', 'Hotel Paraíso del Mar', 'hotel3.jpg'],
    4: ['EE.UU.', 'Nueva York', 'Hotel Aurora Palace', 'hotel4.webp'],
    5: ['EE.UU.', 'Nueva York', 'Hotel Cielo Alto', 'hotel5.jpg'],
    6: ['EE.UU.', 'Nueva York', 'Gran Hotel Mediterráneo', 'hotel6.jpg'],
    7: ['EE.UU.', 'Miami', 'Hotel Aurora Palace', 'hotel7.webp'],
    8: ['EE.UU.', 'Miami', 'Hotel Cielo Alto', 'hotel8.jpg'],
    9: ['EE.UU.', 'Miami', 'Gran Hotel Mediterráneo', 'hotel9.jpg'],

}


hotel = {
    1: ['EE.UU.', 'Washington', 'Hotel Estrella del Norte', 'hotel1.webp'],
    2: ['EE.UU.', 'Washington', 'Hotel Luna de Plata', 'hotel2.jpg'],
}



class ValidatePermissionRequiredMixin(object):
    permission_required = ''
    url_redirect = None




########################################################
#Usuario register y login

class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


########################################################################################



class Categoria(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()

    def generar_nombre_categoria(instance, filename):
        extension = filename.split('.')[-1]
        ruta = 'hoteles1'
        fecha = timezone.now().strftime("%d%m%Y_%H%M%S")
        nombre = f"{fecha}.{extension}"
        return f"{ruta}/{nombre}"
    
    def __str__(self):
        return self.nombre
    foto = models.ImageField(upload_to=generar_nombre_categoria, null=True, default='categorias/categorias.png')



########################################################################################################


class Cargo(models.Model):
    nombre = models.CharField(max_length=100,verbose_name="Nombre del cargo")
    creado = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.nombre}"
    
    class Meta:
        db_table = 'cargo'
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'

class Departamento(models.Model):
    codigo = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Departamento")
    creado = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'departamento'
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'




class Hotel1(models.Model):
    id = models.CharField(max_length=10, verbose_name="ID del hotel", primary_key=True)
    codigoHotel = models.PositiveIntegerField(default=450000, verbose_name="codigoHotel")
    nombre = models.CharField(max_length=50, verbose_name="Nombre")
    descripcion = models.CharField(max_length=255, verbose_name="Descripción")  # Ajusta max_length según tus necesidades
    precio = models.PositiveIntegerField(default=450000, verbose_name="Precio")
    categoria = models.ForeignKey(Categoria, null=False, on_delete=models.CASCADE, verbose_name="Categoría")
    departamento = models.ForeignKey(Departamento, null=False, on_delete=models.CASCADE, verbose_name="Ubicación")
    creado = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.nombre
    

    def generar_nombre_archivo(instance, filename):
        extension = filename.split('.')[-1]
        ruta = 'hoteles'
        fecha = timezone.now().strftime("%d%m%Y_%H%M%S")
        nombre = f"{fecha}.{extension}"
        return f"{ruta}/{nombre}"
    
    foto = models.ImageField(upload_to=generar_nombre_archivo, null=True, default='hoteles/hotel.png')

    def __str__(self):
        return f"{self.nombre} - {self.categoria}"

    class Meta:
        db_table = 'hotel'
        verbose_name = 'Hotel'
        verbose_name_plural = 'Hoteles'
        ordering = ['nombre']

#############################################################################33
class QuienesSomos(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.titulo



class Command(BaseCommand):
    help = 'Create groups and assign permissions'

    def handle(self, *args, **kwargs):
        # Crear grupo 'admin'
        admin_group, created = Group.objects.get_or_create(name='admin')
        if created:
            permissions = Permission.objects.all()
            admin_group.permissions.set(permissions)
            self.stdout.write(self.style.SUCCESS("Grupo 'admin' creado y permisos asignados"))

        # Crear grupo 'cliente'
        client_group, created = Group.objects.get_or_create(name='cliente')
        if created:
            content_type = ContentType.objects.get_for_model(Permission)  # Ajustar según el modelo necesario
            view_permissions = Permission.objects.filter(codename__startswith='view_')
            client_group.permissions.set(view_permissions)
            self.stdout.write(self.style.SUCCESS("Grupo 'cliente' creado y permisos asignados"))
