from django.shortcuts import render, redirect
from django.http import HttpResponse
from random import randrange
from .models import *

# Create your views here.

def index(request):
    # MEDIANTE METODO GET TENDREMOS SI EL USER QUIERE BORRAR LAS TABLAS
    # SI EXISTE GET
    if request.GET:
        # RECOGEMOS EL GET EN UNA VARIABLE LLAMADA OPTION
        option = request.GET.get('option')
        # SI OPTION ES 'SI'
        if option == 'si':
            # ELIMINA DE STOCK TODOS LOS ELEMENTOS QUE HAY EN DICHA TABLA
            Stock.objects.all().delete()
            Pedido.objects.all().delete()
            detallePedido.objects.all().delete()
            # BUCLE FOR EN EL QUE SE INSERTA EN LA TABLA STOCK 10 PRODUCTOS
            # CON SUS DIFERENTES ID'S
            for x in range(10):
                var = Stock(Cproducto=x, cantidad=randrange(10)+1)
                var.save()

    return render(request, 'index.html')
