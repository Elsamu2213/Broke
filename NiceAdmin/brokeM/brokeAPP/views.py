from django.shortcuts import render
from .models import Usuario
from django.shortcuts import render, get_object_or_404


from django.shortcuts import render, redirect

from django.contrib import messages



def index(request):
    return render(request, 'brokeAPP/index.html')


def asignar_view(request):
    return render(request, 'brokeapp1/asignar.html')  # Cambia 'brokeapp1/profile.html' según tu estructura de carpetas


def tablas_view(request):
    return render(request, 'brokeapp1/tablas.html')  # Cambia 'brokeapp1/profile.html' según tu estructura de carpetas


def dashboardA_view(request):
    return render(request, 'brokeapp1/dashboardA.html')  # Cambia 'brokeapp1/profile.html' según tu estructura de carpetas

def loginAdmin_view(request):
    return render(request, 'brokeapp1/loginAdmin.html')  # Cambia 'brokeapp1/profile.html' según tu estructura de carpetas
    
def loginUser_view(request):
    return render(request, 'brokeapp1/loginUser.html')  # Cambia 'brokeapp1/profile.html' según tu estructura de carpetas

def Registrar_view(request):
    return render(request, 'brokeapp1/Registrar.html')  # Cambia 'brokeapp1/profile.html' según tu estructura de carpetas

def Correo_view(request):
    return render(request, 'brokeapp1/Correo.html')  # Cambia 'brokeapp1/profile.html' según tu estructura de carpetas



def lista_usuarios(request):
    usuarios = Usuario.objects.all()  # Obtiene todos los usuarios
    return render(request, 'brokeapp1/lista_usuarios.html', {'usuarios': usuarios})



def crear_usuario(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono', '')
        rol = request.POST.get('rol', 'Empleado')
        contrasena = request.POST.get('contrasena')

        # Crear y guardar el nuevo usuario
        usuario = Usuario(
            nombre=nombre,
            apellido=apellido,
            email=email,
            telefono=telefono,
            rol=rol,
            contrasena=contrasena
        )

        try:
            usuario.save()
            messages.success(request, 'Usuario registrado exitosamente.')
            return redirect('lista_usuarios')
        except Exception as e:
            messages.error(request, f'Error al registrar usuario: {str(e)}')

    return render(request, 'Registrar.html')





def lista_usuarios(request):
    usuarios = Usuario.objects.all()  # Obtiene todos los usuarios
    return render(request, 'brokeapp1/lista_usuarios.html', {'usuarios': usuarios})






