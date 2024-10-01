from django.urls import path
from . import views  # Asegúrate de importar views

urlpatterns = [
    path('asignar/', views.asignar_view, name='asignar'),  # Aquí defines una ruta para tu vista de perfil
    path('tablas/', views.tablas_view, name='tablas'),  # Aquí defines una ruta para tu vista de perfil
    path('dashboardA/', views.dashboardA_view, name='dashboardA'),  # Aquí defines una ruta para tu vista de perfil
    path('loginAdmin/', views.loginAdmin_view, name='loginAdmin'),  # Aquí defines una ruta para tu vista de perfil
    path('loginUser/', views.loginUser_view, name='loginUser'),  # Aquí defines una ruta para tu vista de perfil

    # Puedes agregar más rutas aquí según lo necesites

]
