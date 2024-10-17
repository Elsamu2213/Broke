from django.shortcuts import render
from .models import Usuario
from django.shortcuts import render, get_object_or_404


from django.shortcuts import render, redirect

from django.contrib import messages



from .models import Tarea
from .forms import TareaForm
from .models import Tarea

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


#para corroborar los usuarios______________________________________inicio
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


#para corroborar los usuarios______________________________________end

from .decorators import admin_required



from django.contrib.auth import login  # Importa la función login de Django


from django.contrib.auth import login as auth_login  # Renombrar la función de inicio de sesión de Django





def index(request):
    return render(request, 'brokeAPP/index.html')


def asignar_view(request):
    return render(request, 'brokeapp1/asignar.html')  # Cambia 'brokeapp1/profile.html' según tu estructura de carpetas

@admin_required
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

def empleados(request):
    return render(request, 'brokeapp1/empleadosPrueba.html')  # Cambia 'brokeapp1/profile.html' según tu estructura de carpetas








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




# Vista para listar las tareas

def listar_tareas(request):
    tareas_no_asignadas = Tarea.objects.filter(usuario__isnull=True)  # Tareas no asignadas
    tareas_asignadas = Tarea.objects.filter(usuario__isnull=False)  # Tareas asignadas
    usuarios = Usuario.objects.all()  # Obtener todos los usuarios

    return render(request, 'brokeapp1/asignar.html', {
        'tareas_no_asignadas': tareas_no_asignadas,
        'tareas_asignadas': tareas_asignadas,
        'usuarios': usuarios
    })

@csrf_exempt
def asignar_tarea(request, tarea_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        usuario_id = data.get('usuario_id')

        if not usuario_id:
            return JsonResponse({'success': False, 'error': 'No se ha proporcionado un usuario'})

        try:
            tarea = Tarea.objects.get(id=tarea_id)
            usuario = Usuario.objects.get(id=usuario_id)
            tarea.usuario = usuario  # Asignar el usuario a la tarea
            tarea.save()  # Guardar los cambios

            return JsonResponse({'success': True})
        except Tarea.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Tarea no encontrada'})
        except Usuario.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Usuario no encontrado'})

    return JsonResponse({'success': False, 'error': 'Método no permitido'})

#tareas ya asignadas________________________________________________________


def modificar_asignacion(request, tarea_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Cargar el cuerpo de la solicitud JSON
            usuario_id = data.get('usuario_id')
            tarea = get_object_or_404(Tarea, id=tarea_id)
            usuario = get_object_or_404(Usuario, id=usuario_id)

            # Asignar el nuevo usuario a la tarea
            tarea.usuario = usuario
            tarea.save()

            return JsonResponse({'message': 'Asignación modificada exitosamente.'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

#para verificar usuarios Administrador_______________________________________







def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Intentar obtener el usuario a partir del correo electrónico
        try:
            usuario = Usuario.objects.get(email=email)

            # Verificar si la contraseña coincide (considera usar un método de hash)
            if usuario.contrasena == password:
                # Verifica si el usuario es un administrador
                if usuario.rol == 'Admin':
                    # Almacena el ID del usuario en la sesión
                    request.session['user_id'] = usuario.id  
                    return redirect('dashboardA')  # Redirige al panel de administrador
                else:
                    # Si el usuario es un empleado, muestra un error
                    messages.error(request, 'No tienes acceso a la parte de administración.')
                    return redirect('loginUser')  # Redirige al login de empleados
            else:
                messages.error(request, 'Credenciales inválidas.')
        except Usuario.DoesNotExist:
            messages.error(request, 'Credenciales inválidas.')

    return render(request, 'brokeapp1/loginUser.html')  # Renderiza la página de login



#para verificar usuarios empleado_______________________________________

def login_employee_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Intentar obtener el usuario a partir del correo electrónico
        try:
            usuario = Usuario.objects.get(email=email)

            # Verificar si la contraseña coincide (considera usar un método de hash)
            if usuario.contrasena == password:
                # Verifica si el usuario es un empleado
                if usuario.rol == 'Empleado':
                    # Almacena el ID del usuario en la sesión
                    request.session['user_id'] = usuario.id  
                    return redirect('empleadosPrueba')  # Redirige al panel de empleados
                else:
                    # Si el usuario es un administrador, muestra un error
                    messages.error(request, 'No tienes acceso a la parte de empleados.')
                    return redirect('home')  # Redirige al login de administradores
            else:
                messages.error(request, 'Credenciales inválidas.')
        except Usuario.DoesNotExist:
            messages.error(request, 'Credenciales inválidas.')

    return render(request, 'brokeapp1/loginUser.html')  # Renderiza la página de login


