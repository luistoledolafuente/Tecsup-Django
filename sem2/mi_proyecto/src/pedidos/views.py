from django.shortcuts import render,redirect
from .models import Pedido
from .forms import PedidoForm

from rest_framework import generics
from .serializers import PedidoSerializer

# Create your views here.

class PedidoListCreateAPIView(generics.ListCreateAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

def lista_pedidos(request):
    pedidos = Pedido.objects.select_related('usuario', 'producto').all()
    return render(request, 'pedidos/lista.html', {'pedidos': pedidos})

def crear_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_pedidos')  # O donde quieras redirigir
    else:
        form = PedidoForm()
    
    return render(request, 'pedidos/formulario.html', {'form': form})

    