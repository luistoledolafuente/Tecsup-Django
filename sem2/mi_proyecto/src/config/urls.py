"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from productos.views import lista_productos
from usuarios.views import lista_usuarios
from pedidos.views import lista_pedidos
from pedidos.views import crear_pedido

from pedidos.views import PedidoListCreateAPIView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('productos/', lista_productos, name='lista_productos'),
    path('usuarios/', lista_usuarios, name='lista_usuarios'),
    path('pedidos/', lista_pedidos, name='lista_pedidos'),
    path('pedidos/nuevo/', crear_pedido, name='crear_pedido'),
    path('api/pedidos/', PedidoListCreateAPIView.as_view(), name='api_pedidos'),

]
