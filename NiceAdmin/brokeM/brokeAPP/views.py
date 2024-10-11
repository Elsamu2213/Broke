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








# registro de usuarios 


def crear_usuario(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono', '')
        rol = request.POST.get('rol', 'Empleado')
        contrasena = request.POST.get('contrasena')

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
        except Exception as e:
            messages.error(request, f'Error al registrar usuario:')

    return render(request, 'brokeapp1/Registrar.html')  # Renderiza la plantilla con los mensajes

# registro de usuarios end------------------------------------



#editar y borrar_____________________________________________________________
def lista_usuarios(request):
    usuarios = Usuario.objects.all()  # Obtén todos los usuarios
    return render(request, 'brokeapp1/lista_usuarios.html', {'usuarios': usuarios})

def editar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        rol = request.POST.get('rol')

        usuario.nombre = nombre
        usuario.apellido = apellido
        usuario.email = email
        usuario.telefono = telefono
        usuario.rol = rol

        try:
            usuario.save()
            messages.success(request, 'Usuario actualizado correctamente.')
        except Exception as e:
            messages.error(request, f'Error al actualizar usuario: {str(e)}')

        return redirect('lista_usuarios')

    return render(request, 'brokeapp1/editar_usuario.html', {'usuario': usuario})

    

def borrar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    try:
        usuario.delete()
        messages.success(request, 'Usuario borrado correctamente.')
    except Exception as e:
        messages.error(request, f'Error al borrar usuario: {str(e)}')
    return redirect('lista_usuarios')



# asignar tareas-----------------------------------------------------

def asignar_tarea(request):
    empleados = Usuario.objects.all()  # Obtener todos los empleados
    tareas = Tarea.objects.all()  # Obtener todas las tareas

    if request.method == 'POST':
        usuario_id = request.POST.get('usuario')
        descripcion = request.POST.get('descripcion')
        fecha_vencimiento = request.POST.get('fecha_vencimiento')

        usuario = get_object_or_404(Usuario, id=usuario_id)
        tarea = Tarea(usuario=usuario, descripcion=descripcion, fecha_vencimiento=fecha_vencimiento)
        tarea.save()

        return redirect('asignar')  # Redirigir a la página de asignación

    return render(request, 'brokeapp1/asignar.html', {'empleados': empleados, 'tareas': tareas})


