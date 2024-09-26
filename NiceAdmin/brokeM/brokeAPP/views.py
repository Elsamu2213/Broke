from django.shortcuts import render

def index(request):
    return render(request, 'brokeAPP/index.html')


def profile_view(request):
    return render(request, 'brokeapp1/users-profile.html')  # Cambia 'brokeapp1/profile.html' según tu estructura de carpetas


def profile_view(request):
    return render(request, 'brokeapp1/tablas.html')  # Cambia 'brokeapp1/profile.html' según tu estructura de carpetas

