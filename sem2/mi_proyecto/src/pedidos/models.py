from django.db import models
from usuarios.models import Usuario
from productos.models import Producto 

# Create your models here.
class Pedido(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"pedido de {self.usuario}- {self.producto} ({self.cantidad})"