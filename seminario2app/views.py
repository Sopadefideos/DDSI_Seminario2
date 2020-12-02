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
        #SI POR GET EXISTE UNA VARIABLE ID_BORRAR
        if request.GET.get('id_borrar'):
            #GUARDAMOS LA VARIABLE
            id_borrar = request.GET.get('id_borrar')
            #ACCEDEMOS A LA TABLA DETALLES DONDE APAREZCA EL ID DEL PEDIDO A BORRAR SUS DETALLES
            details = detallePedido.objects.filter(Cpedido_id=id_borrar)
            #ESTE FOR SE ENCARGARA DE DEVOLVER AL STOCK LA CANTIDAD DE PRODUCTOS QUE TENIA EL PEDIDO
            for detail in details:
                id_producto = detail.Cproducto_id
                cantidadDevolver = detail.Cantidad
                productoStock = Stock.objects.get(Cproducto=id_producto)
                var = Stock(Cproducto = id_producto, cantidad = productoStock.cantidad + cantidadDevolver)
                var.save(force_update=True)
            #CONSULTA QUE ELIMINARA TODOS LOS DETALLES QUE APAREZCAN CON EL ID DEL PEDIDO
            detallePedido.objects.filter(Cpedido_id=id_borrar).delete()
            return HttpResponseRedirect("/")

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
            #VOLVEMOS AL INDEX LIMPIANDO LA URL DE POSIBLES DATOS MALICIOSOS QUE SE QUEDAN DE RESTO
            return HttpResponseRedirect("/")

        #RECOGEMOS POR GET LA VARIABLE INSERTAR PARA AÑADIR UN PEDIDO A LA TABLA PEDIDO
        insertar = request.GET.get('insertar')
        if insertar == 'insertar':
            var = Pedido(Ccliente=randrange(500))
            var.save()
            #VOLVEMOS AL INDEX LIMPIANDO LA URL DE POSIBLES DATOS MALICIOSOS QUE SE QUEDAN DE RESTO
            return HttpResponseRedirect("/")

    #GUARDAMOS COMO DICCIONARIOS LA TABLA PEDIDOS PARA PODER LISTAR EN NUESTRO INDEX
    pedido = Pedido.objects.all()
    return render(request, 'index.html', {'pedido': pedido})



def add(request):

    #SI TENEMOS EL ID DEL PEDIDO
    if request.GET.get('id'):
        #GUARDAMOS EN UNA VARIABLE DICHO ID
        id_pedido = request.GET.get('id')
        cantidad_pedido = Stock.objects.all()
        #RENDERIZAMOS DE NUEVO LA PAGINA ADD.HTML CON EL ID_PEDIDO PARA TENER LA CLAVE FORANEA Y EL STOCK PARA EL FORMULARIO
        return render(request, 'add.html', {'id_pedido': id_pedido, 'cantidad_pedido': cantidad_pedido})

    #SI DESDE EL FORMULARIO TENEMOS EL ID DEL PRODUCTO
    if request.GET.get('producto'):
        #GUARDAMOS EN VARIABLES EL PRODUCTO Y LA CANTIDAD QUE EL USUARIO QUIERE AÑADIR AL PRODCUCTO
        producto = request.GET.get('producto')
        cantidad = request.GET.get('cantidad')
        id_pedido = request.GET.get('id_pedido')
        stockDatos = Stock.objects.get(Cproducto=producto)
        
        #SI LA CANTIDAD QUE HA INGRESADO EL USUARIO ES MAYOR A LA QUE HAY EN STOCK DEVUELVE UN MENSAJE
        if int(cantidad) > stockDatos.cantidad:
            messages.info(request, 'Cantidad mayor que la disponible en stock de: {0}!'.format(stockDatos.cantidad))
            #RENDERIZAMOS LA PAGINA CON EL STOCK PARA RECARGAR EL FORMULARIO
            cantidad_pedido = Stock.objects.all()
            return render(request, 'add.html', {'cantidad_pedido': cantidad_pedido})
        
        #SI LA CANTIDAD CORRESPONDE CON LOS PARAMETROS DEL STOCK
        if int(cantidad) <= stockDatos.cantidad:
            inicial = Stock.objects.get(Cproducto=producto).cantidad
            #MODIFICAMOS CON UN UPDATE LA TABLA STOCK RESTANDO LA CANTIDAD QUE HAN INGRESADO POR EL FORMULARIO
            var = Stock(Cproducto=producto, cantidad=inicial-int(cantidad))
            var.save(force_update=True)
            #AÑADIMOS A LA TABLE DETALLES DE PEDIDO LOS DATOS
            var2 = detallePedido(Cproducto=Stock.objects.get(Cproducto=producto), Cpedido=Pedido.objects.get(Cpedido=id_pedido), Cantidad=cantidad)
            var2.save()
            #VOLVEMOS AL INDEX LIMPIANDO LA URL DE POSIBLES DATOS MALICIOSOS QUE SE QUEDAN DE RESTO
            return HttpResponseRedirect("/")



    cantidad_pedido = Stock.objects.all()
    return render(request, 'add.html', {'cantidad_pedido': cantidad_pedido})


def see(request):
    #FUNCION QUE SE ENCARGA DE MOSTRARNOS LOS DIFERENTES PRODUCTOS QUE TIENE UN PEDIDO
    #GUARDAMOS EN UNA VARIABLE EL ID DEL PRODUCTO
    id_pedido = request.GET.get('id')
    #GUARDAMOS LOS DETALLES DEL PEDIDO CON UN SELECT DEL ID_PEDIDO
    details = detallePedido.objects.filter(Cpedido=id_pedido)
    #GUARDAMOS EL ATRIBUTO DE LA FECHA QUE TIENE EL PEDIDO
    fechaPedido = Pedido.objects.get(Cpedido=id_pedido).FechaPedido
    #RENDERIZAMOS SEE.HTML CON LAS DISTINTAS VARIABLES PARA PODER MOSTRARLAS DE MANERA DINAMICA Y PODER VER COMO
    #ESTA EL ESTADO DEL PEDIDO CON SUS DETALLES
    return render(request, 'see.html', {'details': details, 'id_pedido': id_pedido, 'fechaPedido': fechaPedido})
