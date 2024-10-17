from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.rol == 'Administrador':  # Asegúrate de que el campo 'rol' sea correcto
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied  # O puedes redirigirlo a otra página con: return redirect('ruta_no_autorizado')
    return wrapper


def usuario_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if 'user_id' in request.session:  # Verifica si el usuario está autenticado
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
    return _wrapped_view