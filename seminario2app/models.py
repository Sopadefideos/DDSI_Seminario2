from django.db import models
from datetime import datetime
# Create your models here.

class Stock(models.Model):
    Cproducto = models.IntegerField( primary_key=True)
    cantidad = models.IntegerField()

class Pedido(models.Model):
    Cpedido = models.AutoField(primary_key=True)
    Ccliente = models.IntegerField()
    FechaPedido = models.DateField(default=datetime.now)

class detallePedido(models.Model):
    Cpedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    Cproducto = models.ForeignKey(Stock, on_delete=models.CASCADE)
    Cantidad = models.IntegerField()
