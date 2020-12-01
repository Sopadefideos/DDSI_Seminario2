from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from random import randrange
from django.contrib import messages
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
        
        insertar = request.GET.get('insertar')
        if insertar == 'insertar':
            var = Pedido(Ccliente=randrange(500))
            var.save()

    pedido = Pedido.objects.all()
    detalle = detallePedido.objects.all()
    return render(request, 'index.html', {'pedido': pedido})

def add(request):
    if request.GET.get('id'):
        id_pedido = request.GET.get('id')
        print(id_pedido)
        cantidad_pedido = Stock.objects.all()
        return render(request, 'add.html', {'id_pedido': id_pedido, 'cantidad_pedido': cantidad_pedido})

    if request.GET.get('producto'):
        producto = request.GET.get('producto')
        cantidad = request.GET.get('cantidad')
        id_pedido = request.GET.get('id_pedido')
        print(id_pedido)
        stockDatos = Stock.objects.get(Cproducto=producto)
        
        if int(cantidad) > stockDatos.cantidad:
            messages.info(request, 'Cantidad mayor que la disponible en stock de: {0}!'.format(stockDatos.cantidad))
            cantidad_pedido = Stock.objects.all()
            return render(request, 'add.html', {'cantidad_pedido': cantidad_pedido})
        
        if int(cantidad) <= stockDatos.cantidad:
            inicial = Stock.objects.get(Cproducto=producto).cantidad
            var = Stock(Cproducto=producto, cantidad=inicial-int(cantidad))
            var.save(force_update=True)

            var2 = detallePedido(Cproducto=Stock.objects.get(Cproducto=producto), Cpedido=Pedido.objects.get(Cpedido=id_pedido), Cantidad=cantidad)
            var2.save()

            pedido = Pedido.objects.all()
            return HttpResponseRedirect("/")



    cantidad_pedido = Stock.objects.all()
    return render(request, 'add.html', {'cantidad_pedido': cantidad_pedido})
