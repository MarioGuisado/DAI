from django.shortcuts import render

from . import models
from .forms import ProductoForm

# Create your views here.
from django.http import HttpResponse
from django.template import Template, Context, loader
from django.contrib import messages

import logging
logger = logging.getLogger(__name__)

def index(request):

    productos_pagina_inicial = models.productos_mayor_4()
    contexto = {
        "productos_pagina_inicial": productos_pagina_inicial
    }

    return render(request,'index.html', contexto)

def nuevo_producto(request):

    formulario = ProductoForm()
    rating = {
        "puntuación": 0,
        "cuenta": 1
    }
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            
            nombre = form.cleaned_data['nombre']
            precio = form.cleaned_data['precio']
            descripcion = form.cleaned_data['descripcion']
            categoria = form.cleaned_data['categoria']

            #Descarga la imagen y la guarda en la carpeta static
            imagen = form.cleaned_data['imagen']
            with open('static/' + nombre + ".jpg", 'wb+') as destination:
                for chunk in imagen.chunks():
                    destination.write(chunk)
            nombre_imagen = nombre + ".jpg"

            models.guardar_producto(nombre,precio,descripcion,categoria,nombre_imagen,rating)
            messages.success(request, 'Producto guardado correctamente')
        
        else:
            messages.error(request, 'Error en el formulario') 
            
            for field in form:
                for error in field.errors:
                    messages.error(request, error)


    contexto = {
        "form" : formulario
    }
    
    return render(request,'nuevo_producto.html', contexto)

def mostrar_productos(request):
    categoria_seleccionada = request.GET.get('categoria')
    productos = models.mostrar_productos(categoria_seleccionada)
    contexto = {
        "productos": productos,
    }
    return render(request, 'mostrar_productos.html', contexto)

def busqueda(request):
    busqueda = request.GET.get("busqueda")
    productos_busqueda = models.busqueda(busqueda)
    contexto = {
        "productos_busqueda": productos_busqueda,
    }
    return render(request, 'busqueda.html', contexto)

def productos100_200(request):
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Electrónica entre 100 y 200 €</title>
    </head>
    <body>
        <h1>Electrónica entre 100 y 200 €</h1>
        <ul>

        """
    
    productos_electronica = models.productos100_200()

    for producto in productos_electronica:
        url_imagen = str(producto.get("imágen"))
        url_imagen = "." + url_imagen
        html = html + f'<li><strong>{producto.get("nombre")}</strong> <img src="{url_imagen}" alt="Imagen"> </li>'
    html = html + '</ul> </body></html>'
  
    response = HttpResponse(html, content_type='text/html')

    return response

def descripcion_pocket(request):
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Productos con la palabra pocket</title>
    </head>
    <body>
        <h1>Productos con la palabra pocket</h1>
        <ul>

        """
    
    productos_pocket = models.productos_pocket()
    for producto in productos_pocket:
        html = html + f'<li><strong>{producto.get("nombre")}</strong><br>{producto.get("descripción")}</li>'
    html = html + '</ul> </body></html>'
  
    response = HttpResponse(html, content_type='text/html')

    return response

def productos_mayor_4(request):
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Productos puntuación mayor que 4</title>
    </head>
    <body>
        <h1>Productos puntuación mayor que 4</h1>
        <ul>

        """

    productos_mayor_4 = models.productos_mayor_4()
    for producto in productos_mayor_4:
        puntuacion = producto["rating"]["puntuación"]
        html = html + f'<li><strong>{producto.get("nombre")}</strong><br> Puntuación: {puntuacion}</li>'
    html = html + '</ul> </body></html>'
  
    response = HttpResponse(html, content_type='text/html')

    return response

def ropa_hombre(request):
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Ropa de hombre, ordenada por puntuación</title>
    </head>
    <body>
        <h1>Ropa de hombre, ordenada por puntuación</h1>
        <ul>

        """

    productos_hombre = models.ropa_hombre()
    for producto in productos_hombre:
        puntuacion = producto["rating"]["puntuación"]
        html = html + f'<li><strong>{producto.get("nombre")}</strong><br> Puntuación: {puntuacion}</li>'
    html = html + '</ul> </body></html>'
  
    response = HttpResponse(html, content_type='text/html')

    return response

def facturacion_total(request):
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Facturación total</title>
    </head>
    <body>
        <h1>Facturación total</h1>
        <ul>

        """

    facturacion_total = models.facturacion()
    html = html + f'<li>La facturación total es: {facturacion_total} €</li></ul> </body></html>'
  
    response = HttpResponse(html, content_type='text/html')

    return response

def facturacion_categorias(request):
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Facturación por categorías</title>
    </head>
    <body>
        <h1>Facturación por categorías</h1>
        <ul>

        """

    facturacion_categorias = models.facturacion_categorias()
          
    for categoria in facturacion_categorias:
        html = html + f'<li><strong>{categoria.capitalize()}</strong><br> Facturación: {facturacion_categorias[categoria]} €</li>'

    html = html + f'</ul></body></html>'
  
    response = HttpResponse(html, content_type='text/html')

    return response