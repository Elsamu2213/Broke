from django.urls import path
from . import views  # Asegúrate de importar views

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),  # Aquí defines una ruta para tu vista de perfil
    path('tablas/', views.profile_view, name='tablas'),  # Aquí defines una ruta para tu vista de perfil

    # Puedes agregar más rutas aquí según lo necesites

]
