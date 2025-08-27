from django.shortcuts import render
from .models import Usuario
# Create your views here.
def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/lista.html', {'usuarios': usuarios})