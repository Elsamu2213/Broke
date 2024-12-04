


from django.utils.decorators import method_decorator

from .models import Tarea  # Asegúrate de importar tu modelo
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404


from django.shortcuts import render, redirect

from django.contrib import messages



from .models import Tarea
from .forms import TareaForm
from .models import Tarea
from .models import UsuarioCustomizado 

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
from django.contrib.auth import get_user_model
Usuario = get_user_model()  # Obtiene el modelo de usuario actual

from django.contrib.auth import authenticate, login

import re

from django.db import IntegrityError

from django.contrib.auth import update_session_auth_hash


from django.contrib.auth import logout  


#discord_____________________________
import asyncio
import discord
from django.http import HttpResponse
from django.conf import settings


#correos_______________________________
from django.core.mail import EmailMessage
from django.conf import settings

from django.shortcuts import render, redirect
from django.contrib import messages
from .utils import enviar_correo_mailjet

def index(request):
    return render(request, 'brokeAPP/index.html')

@admin_required
def asignar_view(request):
    return render(request, 'brokeapp1/asignar.html')  # Cambia 'brokeapp1/profile.html' según tu estructura de carpetas

@admin_required
def tablas_view(request):
    return render(request, 'brokeapp1/tablas.html')  # Cambia 'brokeapp1/profile.html' según tu estructura de carpetas

@admin_required
def dashboardA_view(request):
    return render(request, 'brokeapp1/dashboardA.html')  # Cambia 'brokeapp1/profile.html' según tu estructura de carpetas

def loginAdmin_view(request):
    return render(request, 'brokeapp1/loginAdmin.html')  # Cambia 'brokeapp1/profile.html' según tu estructura de carpetas
    
def loginUser_view(request):
    return render(request, 'brokeapp1/loginUser.html')  # Cambia 'brokeapp1/profile.html' según tu estructura de carpetas
@admin_required
def Registrar_view(request):
    return render(request, 'brokeapp1/Registrar.html')  # Cambia 'brokeapp1/profile.html' según tu estructura de carpetas
@admin_required
def Correo_view(request):
    return render(request, 'brokeapp1/Correo.html')  # Cambia 'brokeapp1/profile.html' según tu estructura de carpetas

def empleados(request):
    return render(request, 'brokeapp1/empleadosPrueba.html')  # Cambia 'brokeapp1/profile.html' según tu estructura de carpetas

@admin_required
def chatAdmin(request):
    return render(request, 'brokeapp1/chatAdmin.html')  # Cambia 'brokeapp1/profile.html' según tu estructura de carpetas


# registro de usuarios 


def crear_usuario(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono', '')
        rol = request.POST.get('rol', 'Empleado')
        contrasena = request.POST.get('contrasena')
        confirmar_contrasena = request.POST.get('confirmar_contrasena')

        # Validar que las contraseñas coincidan
        if contrasena != confirmar_contrasena:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'brokeapp1/Registrar.html')

        # Validar que el nombre y apellido solo contengan letras
        if not re.match("^[A-Za-záéíóúÁÉÍÓÚÑñ ]+$", nombre):
            messages.error(request, 'El nombre solo puede contener letras.')
            return render(request, 'brokeapp1/Registrar.html')

        if not re.match("^[A-Za-záéíóúÁÉÍÓÚÑñ ]+$", apellido):
            messages.error(request, 'El apellido solo puede contener letras.')
            return render(request, 'brokeapp1/Registrar.html')

        # Genera un username a partir del nombre y apellido
        username = f"{nombre}.{apellido}".lower()

        # Crea una instancia del usuario personalizado
        usuario = UsuarioCustomizado(
            username=username,
            first_name=nombre,
            last_name=apellido,
            email=email,
            telefono=telefono,
            rol=rol
        )

        # Guarda el usuario en la base de datos
        try:
            usuario.set_password(contrasena)  # Establece la contraseña de manera segura
            usuario.save()
            messages.success(request, 'Usuario registrado exitosamente.')
            return redirect('lista_usuarios')  # Redirige a la vista correspondiente
        except IntegrityError:
            messages.error(request, 'El número de teléfono ya está en uso. Por favor, ingrese uno diferente.')
        except Exception as e:
            messages.error(request, f'Error al registrar usuario: {str(e)}')

    return render(request, 'brokeapp1/Registrar.html')

#editar y borrar_____________________________________________________________

def lista_usuarios(request):
    usuarios = Usuario.objects.all()  # Obtén todos los usuarios
    return render(request, 'brokeapp1/lista_usuarios.html', {'usuarios': usuarios})


def editar_usuario(request, id):
    usuario = UsuarioCustomizado.objects.get(id=id)
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        rol = request.POST.get('rol')
        password = request.POST.get('password')
        confirmar_password = request.POST.get('confirmar_password')

        # Actualiza los campos básicos
        usuario.first_name = nombre
        usuario.last_name = apellido
        usuario.email = email
        usuario.telefono = telefono
        usuario.rol = rol
        
        # Si se ha proporcionado una nueva contraseña
        if password:
            if password == confirmar_password:
                usuario.set_password(password)  # Establece la nueva contraseña
                update_session_auth_hash(request, usuario)  # Actualiza la sesión para que no se cierre al cambiar la contraseña
                messages.success(request, 'Contraseña actualizada correctamente.')
            else:
                messages.error(request, 'Las contraseñas no coinciden.')
                return render(request, 'brokeapp1/editar_usuario.html', {'usuario': usuario})

        try:
            usuario.save()  # Guarda los cambios en el usuario
            messages.success(request, 'Usuario actualizado correctamente.')
            return redirect('lista_usuarios')  # Cambia esta redirección según sea necesario
        except Exception as e:
            messages.error(request, f'Error al actualizar usuario: {str(e)}')
    
    return render(request, 'brokeapp1/editar_usuario.html', {'usuario': usuario})

def borrar_usuario(request, id):
    UsuarioCustomizado = get_user_model()
    usuario = get_object_or_404(UsuarioCustomizado, id=id)
    try:
        usuario.delete()
        messages.success(request, 'Usuario borrado correctamente.')
    except Exception as e:
        messages.error(request, f'Error al borrar usuario: {str(e)}')
    return redirect('lista_usuarios')



# asignar tareas-----------------------------------------------------




# Vista para listar las tareas
@admin_required
def listar_tareas(request):
    tareas_no_asignadas = Tarea.objects.filter(usuario__isnull=True)  # Tareas no asignadas
    tareas_asignadas = Tarea.objects.filter(usuario__isnull=False, completada=False)  # Tareas asignadas pero no completadas
    tareas_completadas = Tarea.objects.filter(completada=True)  # Tareas completadas
    usuarios = Usuario.objects.all()  # Obtener todos los usuarios

    return render(request, 'brokeapp1/asignar.html', {
        'tareas_no_asignadas': tareas_no_asignadas,
        'tareas_asignadas': tareas_asignadas,
        'tareas_completadas': tareas_completadas,
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
            usuario = UsuarioCustomizado.objects.get(id=usuario_id)  # Cambia aquí para usar UsuarioCustomizado
            tarea.usuario = usuario  # Asignar el usuario a la tarea
            tarea.save()  # Guardar los cambios

            return JsonResponse({'success': True})
        except Tarea.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Tarea no encontrada'})
        except UsuarioCustomizado.DoesNotExist:  # Cambia aquí para usar UsuarioCustomizado
            return JsonResponse({'success': False, 'error': 'Usuario no encontrado'})

    return JsonResponse({'success': False, 'error': 'Método no permitido'})
#tareas ya asignadas________________________________________________________
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Tarea, UsuarioCustomizado

@csrf_exempt
def completar_tarea(request, tarea_id):
    if request.method == 'POST':
        print("Solicitud para completar tarea recibida")  # Mensaje de depuración
        try:
            tarea = Tarea.objects.get(id=tarea_id)
            tarea.completada = True
            tarea.save()
            return JsonResponse({'success': True})
        except Tarea.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Tarea no encontrada'})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})


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

        # Autenticar al usuario con su email
        usuario = authenticate(request, username=email, password=password)

        if usuario is not None:
            login(request, usuario)  # Inicia sesión usando el sistema de autenticación de Django
            if usuario.rol == 'Admin':
                return redirect('dashboardA')  # Redirige al panel de administrador
            else:
                return redirect('empleadosPrueba')  # Redirige al panel de empleados
        else:
            messages.error(request, 'Credenciales inválidas.')
    
    return render(request, 'brokeapp1/loginUser.html')  # Renderiza la página de login




def login_employee_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Autenticar al usuario
        usuario = authenticate(request, username=email, password=password)

        if usuario is not None:
            login(request, usuario)  # Inicia sesión usando el sistema de autenticación de Django
            if usuario.rol == 'Empleado':
                return redirect('AccesoUs')  # Redirige al panel de empleados
            else:
                messages.error(request, 'No tienes acceso a la parte de empleados.')
                return redirect('home')  # Redirige al login de administradores
        else:
            messages.error(request, 'Credenciales inválidas.')

    return render(request, 'brokeapp1/loginUser.html')  # Renderiza la página de login




#cerrar sesion_________________________________________________________________________________________________________

def logout_view(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect('home')  # Redirige al login

#discord _________________________________________________________________________________________________________

def Ubica_view(request):
    return render(request, 'brokeapp1/ubica.html')

def AccesoUs_view(request):
    return render(request, 'brokeapp1/AccesoUs.html')

def PagoUsuario_view(request):
    return render(request, 'brokeapp1/PagoUsuario.html')

# Reemplaza 'your_token_here' con el token de tu bot
TOKEN = 'MTI5ODU0MjUyNTkwODM4NTgxMw.GN504t.7M-B0owLgS2e7mlWbmC6Jzr4T53Vy7CVm1VxHU'
# Reemplaza 'your_channel_id_here' con el ID del canal donde quieres enviar mensajes
CHANNEL_ID = 1298417233290072087  # Asegúrate de que sea un entero
 
async def enviar_mensaje_a_discord(mensaje):
    client = discord.Client(intents=discord.Intents.default())
    await client.login(TOKEN)
    channel = await client.fetch_channel(CHANNEL_ID)
    await channel.send(mensaje)
    await client.close()
 
def enviar_mensajeD(request):
    if request.method == 'POST':
        # Obtén el mensaje personalizado del formulario o request POST
        mensaje_personalizado = request.POST.get('mensaje', 'Hola desde Django!')
        # Envía el mensaje usando discord.py
        asyncio.run(enviar_mensaje_a_discord(mensaje_personalizado))
        return HttpResponse("Mensaje enviado a Discord!")
    else:
        return HttpResponse("Método no soportado.", status=405)



import base64

from django.shortcuts import render, redirect
from django.contrib import messages
from .utils import enviar_correo_mailjet

def enviar_correo_view(request):
    if request.method == 'POST':
        destinatario = request.POST['destinatario']
        asunto = request.POST['asunto']
        mensaje = request.POST['mensaje']
        archivo_adjunto = request.FILES.get('archivo')
        
        adjunto_b64 = None
        if archivo_adjunto:
            adjunto_b64 = base64.b64encode(archivo_adjunto.read()).decode('utf-8')

        if enviar_correo_mailjet(destinatario, asunto, mensaje, adjunto_b64):
            messages.success(request, 'Correo enviado con éxito.')
        else:
            messages.error(request, 'Hubo un error al enviar el correo.')
        
        return redirect('enviar_correo')
    
    return render(request, 'brokeapp1/correo.html')



#Funcion de observaciones Tabla asignar
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json
from .models import Tarea

@csrf_exempt  # Si estás manejando el CSRF manualmente, pero es mejor usar el token CSRF
@require_POST
def guardar_observacion(request, tarea_id):
    data = json.loads(request.body)
    observacion = data.get('observacion')

    try:
        tarea = Tarea.objects.get(id=tarea_id)
        tarea.observaciones = observacion
        tarea.save()
        return JsonResponse({'message': 'Observación guardada.'}, status=200)
    except Tarea.DoesNotExist:
        return JsonResponse({'message': 'Tarea no encontrada.'}, status=404)
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)

def vista_ubica(request):
    tareas = Tarea.objects.values('fecha_asignacion', 'direccion', 'actividad', 'num_cajero')
    return render(request, 'ubica.html', {'tareas': tareas})


# Estado de la tabla proceso 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Tarea
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import TareaAvanzada  # Asegúrate de importar la clase correcta
import json

@csrf_exempt
def actualizar_estado(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            tarea_id = data.get("id")
            nuevo_estado = data.get("estado")

            tarea = Tarea.objects.get(id=tarea_id)
            tarea.estado = nuevo_estado
            tarea.save()

            return JsonResponse({"success": True, "message": "Estado actualizado exitosamente"})
        except Tarea.DoesNotExist:
            return JsonResponse({"success": False, "error": "Tarea no encontrada"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    else:
        return JsonResponse({"success": False, "error": "Método no permitido"})


import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from .models import Tarea

from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
from .models import Tarea

import pandas as pd
from django.core.exceptions import ValidationError

def cargar_excel(request):
    if request.method == "POST" and request.FILES.get("archivo_excel"):
        archivo_excel = request.FILES["archivo_excel"]
        try:
            # Leer el archivo Excel
            df = pd.read_excel(archivo_excel)

            # Verificar si la columna 'CP' o 'Cod_postal' existe
            if 'CP' not in df.columns and 'Cod_postal' not in df.columns:
                raise ValidationError("Faltan las siguientes columnas requeridas: CP o Cod_postal")
            
            # Procesar cada fila del archivo y cargarla en la base de datos
            for index, row in df.iterrows():
                direccion = row['direccion']
                Cod_postal = row['Cod_postal'] if 'CP' in row else row['Cod_postal']
                num_cajero = row['num_cajero']
                
                # Crear la tarea
                tarea = Tarea.objects.create(
                    direccion=direccion,
                    num_cajero=num_cajero,
                    # Aquí deberías mapear otros campos necesarios
                    # Por ejemplo, actividad, observaciones, etc.
                )

            return JsonResponse({"success": "Archivo procesado correctamente"})
        
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error al procesar el archivo: {str(e)}"}, status=400)
    return JsonResponse({"error": "Método no permitido"}, status=405)



