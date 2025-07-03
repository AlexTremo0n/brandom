from django.contrib import admin
from django.urls import path,include
from roomApp import views as vista
from .views import LoginView, inicio, RegisterView, salir
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',vista.inicio,name='index'),
    path('habitaciones/',vista.personal,name='habitaciones'),
    path('catalogo/',vista.catalogo,name='habitaciones'),
   
    path('info/',vista.info,name='info'),
    path('fotos/',vista.fotos,name='fotos'),
    path('paises/<int:codigo>/', vista.paises, name='paises'),
    path('hoteles/<int:codigo>/', vista.hoteles, name='hoteles'),
    path('hotel/<int:codigo>/', vista.hotel, name='hotel'),
    path('register/', RegisterView.as_view(), name='register'),
    path('salirse/', salir, name='salirse'),
    path('login/', vista.LoginView, name='login'),
    path('categorias/', vista.categorias, name='categorias'),
   
   
    path('hoteles1/',vista.todos_hoteles,name='hoteles1'),
    path('hotelEdit/<int:hotel_id>/',vista.cargar_editar_hotel,name='editarHotel'),
    path('hotelEditado/<int:hotel_id>',vista.editar_hotel,name='hotelEditado'),
    path('hotelDel/<int:hotel_id>',vista.eliminar_hotel,name='eliminarHotel'),
    path('buscar_hoteles/', vista.buscar_hoteles, name='buscar_hoteles'),
    path('crearHotel/', vista.crear_hotel, name='crearHotel'),
#####################################################################################
    path('categoriasEdit/<int:categorias_id>/',vista.cargar_editar_categoria,name='editarCategoria'),
    path('categoriasEditado/<int:categorias_id>',vista.editar_categoria,name='categoriaEditado'),
    path('categoriasDel/<int:categorias_id>',vista.eliminar_categoria,name='eliminarCategoria'),
    path('crearCategoria/',vista.crear_categoria, name='crearCategoria'),
    path('buscar_categorias/', vista.buscar_categorias, name='buscar_categorias'),
#####################################################################################333
    path('quienesomos/', vista.quienesomos, name='quienesomos'),
    path('accounts/',include('django.contrib.auth.urls')),
##############################################################################################33
    path('usuarios/', vista.lista_usuarios, name='lista_usuarios'),
    path('editar/<int:pk>/', vista.editar_usuario, name='editarUsuario'),
    path('eliminar/<int:pk>/', vista.eliminar_usuario, name='eliminarUsuario'),
    path('buscar_usuarios/', vista.buscar_usuarios, name='buscar_usuarios'),
    path('clientes/', vista.lista_usuarios_normales, name='lista_clientes'),
    path('buscar_clientes/', vista.buscar_usuarios_normales, name='buscar_clientes'),





##############################################
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
