from django.urls import path
from . import views  # Asegúrate de importar views
from django.urls import path
from . import views

urlpatterns = [
    path('asignar/', views.asignar_view, name='asignar'),  # Aquí defines una ruta para tu vista de perfil
    path('tablas/', views.tablas_view, name='tablas'),  # Aquí defines una ruta para tu vista de perfil
    path('dashboardA/', views.dashboardA_view, name='dashboardA'),  # Aquí defines una ruta para tu vista de perfil
    path('loginAdmin/', views.loginAdmin_view, name='loginAdmin'),  # Aquí defines una ruta para tu vista de perfil
    path('loginUser/', views.loginUser_view, name='loginUser'),  # Aquí defines una ruta para tu vista de perfil
    path('Registrar/', views.Registrar_view, name='Registrar'),  # Aquí defines una ruta para tu vista de perfil
    path('Correo/', views.Correo_view, name='Correo'),  # Aquí defines una ruta para tu vista de perfil
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),  # Aquí defines una ruta para tu vista de perfil
    
    
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('editar_usuario/<int:id>/', views.editar_usuario, name='editar_usuario'),
    path('borrar_usuario/<int:id>/', views.borrar_usuario, name='borrar_usuario'),





]
