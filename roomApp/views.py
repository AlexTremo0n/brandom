from django.shortcuts import get_object_or_404, render ,redirect
from roomApp import models as datos
from django.views import View
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import *
from django.http import HttpResponse
from django.http import JsonResponse
from .forms import *
from django.contrib.auth import login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Categoria
from django.db.models import Q
from django.contrib.auth.decorators import permission_required
from .models import AuthUser
from django.template.loader import render_to_string




def inicio(request):
    data = {'viajes': datos.pais}
    return render(request, 'inicio.html', data)

def personal(request):
    data = {
        'nombre':'jarvis',
        'paterno': 'orostigue',
        'materno': 'gomez',
        'edad': 19,
        'correo': 'orostiguejarvis39@gmail.com',
        'cargo': 'Estudiante'
    }
    return render(request,'front_end/habitaciones.html',data)


def catalogo(request):
    data = {
        'productos':datos.productos
    }
    return render(request,'front_end/habitaciones.html',data)


def info(request):
    data = {
        'info':datos.info
    }
    return render(request,'front_end/info.html',data)

def fotos(request):
    data = {
        'fotos':datos.fotos
    }
    return render(request,'front_end/fotos.html',data)


#las cajas de los paises

def paises(request, codigo):
    pais = datos.pais[codigo][0]
    codigos_ciudades = datos.pais[codigo][4]
    ciudades = {clave: valor for clave, valor in datos.ciudades.items() if clave in codigos_ciudades}
    return render(request, 'front_end/paises.html', {'pais': pais, 'ciudades': ciudades})

def hoteles(request, codigo):
    ciudad = datos.ciudades[codigo][2]
    codigos_hoteles = datos.ciudades[codigo][4]
    hoteles_list = []
    for clave in codigos_hoteles:
        hotel_data = datos.hoteles[clave]
        hoteles_list.append({
            'clave': clave,
            'nombre': hotel_data[2],
            'imagen': hotel_data[3],
            'ciudad': hotel_data[1],
        })
    return render(request, 'front_end/hoteles.html', {'ciudad': ciudad, 'hoteles': hoteles_list})

def hotel(request, codigo):
    hotel_data = datos.hoteles.get(codigo)
    if hotel_data:
        hotel = {
            'nombre': hotel_data[2],
            'descripcion': '',
            'imagen': hotel_data[3],
            'ciudad': hotel_data[1],
        }
        return render(request, 'front_end/hotel.html', {'hotel': hotel})
    else:
        return HttpResponse("Hotel no encontrado")

def obtener_datos_del_hotel(codigo_hotel):
    datos_por_hotel = {
        1: ['Washington', 'Los Ángeles', 'Nueva York'],
        2: ['Ottawa', 'Toronto', 'Montreal'],
    }

    ciudades = datos_por_hotel.get(codigo_hotel, [])

    return ciudades



###registro
class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'registro/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_superuser = form.cleaned_data.get('is_superuser', False)
            user.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Cuenta creada para {username}')
            return redirect('login')

        return render(request, self.template_name, {'form': form})

def LoginView(request):
    if request.method=="POST":
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request, user)
            
    else:
        form=AuthenticationForm()
    return render(request,'registro/login.html',{'form':form})


def salir(request):
    try:
        logout(request)
        messages.success(request, '¡Has cerrado sesión correctamente!')
    except Exception as e:
        messages.error(request, f'Hubo un problema al cerrar sesión: {e}')
    return redirect('index')

def login(request):
    data = {
        'login':datos.login
    }
    return render(request,'registro/login.html',data)



###Hoteles en la base de datos####
def categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'categorias/categorias.html', {'categorias': categorias})

 # Ajusta el permiso según tu configuración
def crear_hotel(request):
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('hoteles1')
        else:
            print(form.errors)
    else:
        form = HotelForm()
    
    return render(request, 'categorias/hotelAdd.html', {'form': form})


def todos_hoteles(request):
    hoteles = Hotel1.objects.all().order_by('nombre')
    print(hoteles)
    for hotel in hoteles:
        print(f"Hotel: {hotel.nombre}, Código: {hotel.codigoHotel}")
    data = {
        'hoteles': hoteles,
    }
    return render(request, 'categorias/hoteles1.html', data)


def cargar_editar_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel1,id=hotel_id)
    form = HotelForm(instance=hotel)
      
    return render(request,'categorias/hotelEdit.html',{'form':form,'hotel':hotel})


def editar_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel1,id=hotel_id)
    
    if request.method == 'POST':
        form = HotelForm(request.POST,request.FILES,instance=hotel)
        if form.is_valid():
            if 'foto' in request.FILES:
                hotel.foto = request.FILES['foto']
            form.save()
            return redirect("hoteles1")
    else:
        form = HotelForm(instance=hotel)
        
    return render(request,'categorias/hoteles1.html',{'form':form})  


def eliminar_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel1,id=hotel_id)
    
    if request.method == 'POST':
        hotel.delete()
        return redirect('hoteles1')
    
    return render(request,'categorias/hotelDel.html',{'hotel':hotel})



####################################################### CATEGORIAS

def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('categorias')
        else:
            print(form.errors)
    else:
        form = CategoriaForm()
    
    return render(request, 'categorias/categoriasAdd.html', {'form': form})

def todas_categorias(request):
    categorias = Categoria.objects.all().order_by('nombre')
    data = {
        'categorias': categorias,
    }
    return render(request, 'categorias/categorias.html', data)



def cargar_editar_categoria(request, categorias_id):
    categoria = get_object_or_404(Categoria, id=categorias_id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, request.FILES, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect("categorias")
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'categorias/categoriasEdit.html', {'form': form, 'categoria': categoria})




def editar_categoria(request, categorias_id):
    categoria = get_object_or_404(Categoria, id=categorias_id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, request.FILES, instance=categoria)
        if form.is_valid():
            if 'foto' in request.FILES:
                categoria.foto = request.FILES['foto']
            form.save()
            return redirect("categorias")
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'categorias/categorias.html', {'form': form})




def eliminar_categoria(request, categorias_id):
    categoria = get_object_or_404(Categoria, id=categorias_id)
    if request.method == 'POST':
        categoria.delete()
        return redirect('categorias')
    return render(request, 'categorias/categoriasDel.html', {'categoria': categoria})


####################Busqueda##################
def buscar_hoteles(request):
    query = request.GET.get('q', '')
    if query:
        hoteles = Hotel1.objects.filter(Q(nombre__icontains=query) | Q(codigoHotel__icontains=query))
    else:
        hoteles = Hotel1.objects.all().order_by('nombre')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'categorias/tabla_hoteles.html', {'hoteles': hoteles})
    
    return render(request, 'categorias/hoteles1.html', {'hoteles': hoteles})

def buscar_categorias(request):
    query = request.GET.get('q', '')
    if query:
        categorias = Categoria.objects.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query)
        )
    else:
        categorias = Categoria.objects.all().order_by('nombre')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'categorias/cards_categorias.html', {'categorias': categorias})
    
    return render(request, 'categorias/categorias.html', {'categorias': categorias})



def lista_usuarios(request):
    usuarios = AuthUser.objects.all()  # Obtener todos los usuarios

    # Pasar los usuarios a la plantilla
    return render(request, 'tablas/usuarios.html', {'usuarios': usuarios})

def editar_usuario(request, pk):
    usuario = get_object_or_404(AuthUser, pk=pk)
    # Lógica para editar el usuario aquí
    return HttpResponse("Página de edición de usuario")

def eliminar_usuario(request, pk):
    usuario = get_object_or_404(AuthUser, pk=pk)
    usuario.delete()
    # Redirecciona a alguna vista después de eliminar el usuario
    return redirect('index')

def buscar_usuarios(request):
    query = request.GET.get('q', '')
    
    if query:
        usuarios = User.objects.filter(username__icontains=query, is_superuser=True)
    else:
        usuarios = User.objects.filter(is_superuser=True)
    
    context = {
        'usuarios': usuarios,
    }
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html_result = render_to_string('tablas/usuarios_partial.html', context)
        return JsonResponse({'html_result': html_result})
    
    return render(request, 'tablas/usuarios.html', context)








def lista_usuarios_normales(request):
    usuarios = AuthUser.objects.filter(is_superuser=False)  # Obtener solo usuarios normales
    return render(request, 'tablas/clientes.html', {'usuarios': usuarios})

def buscar_usuarios_normales(request):
    query = request.GET.get('q', '')
    
    if query:
        usuarios = AuthUser.objects.filter(username__icontains=query, is_superuser=False)
    else:
        usuarios = AuthUser.objects.filter(is_superuser=False)
    
    context = {
        'usuarios': usuarios,
    }
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html_result = render_to_string('tablas/tabla_clientes.html', context)
        return JsonResponse({'html_result': html_result})
    
    return render(request, 'tablas/clientes.html', context)















############################################################################################################################3
def quienesomos(request):
    info = QuienesSomos.objects.all()
    data = {
        'quienesomos': info
    }
    return render(request, 'front_end/quienesomos.html', data)