from django.db import models
from datetime import datetime
# Create your models here.

class Stock(models.Model):
    Cproducto = models.CharField(max_length=50, primary_key=True)
    cantidad = models.IntegerField()

class Pedido(models.Model):
    Cpedido = models.CharField(max_length=50, primary_key=True)
    Ccliente = models.CharField(max_length=50)
    FechaPedido = models.DateField(default=datetime.now)

class detallePedido(models.Model):
    Cpedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    Cproducto = models.ForeignKey(Stock, on_delete=models.CASCADE)
    Cantidad = models.IntegerField()
