# Create your models here.
# Autor: Mario Guisado García
from django.db import models
from pydantic import BaseModel, FilePath, Field, EmailStr, ValidationError, validator
from pymongo import MongoClient
from pprint import pprint
from datetime import datetime
from typing import Any
import requests
import os
from django.http import HttpResponse
from bson.objectid import ObjectId


import logging
logger = logging.getLogger(__name__)


# https://requests.readthedocs.io/en/latest/
def getProductos(api):
	response = requests.get(api)
	return response.json()
				
# Esquema de la BD
# https://docs.pydantic.dev/latest/
# con anotaciones de tipo https://docs.python.org/3/library/typing.html
# https://docs.pydantic.dev/latest/usage/fields/

class Nota(BaseModel):
	puntuación: float = Field(ge=0., lt=5.)
	cuenta: int = Field(ge=1)
				
class Producto(BaseModel):
	_id: Any
	nombre: str
	precio: float
	descripción: str
	categoría: str
	imágen: str | None
	rating: Nota
	
	@validator('nombre')
	@classmethod
	def nombre_mayuscula(cls, value):
		if not value[0].isupper():
			raise ValueError("El nombre debe comenzar por mayúscula")
		return value

class Compra(BaseModel):
	_id: Any
	usuario: EmailStr
	fecha: datetime
	productos: list	



# Conexión con la BD				
# https://pymongo.readthedocs.io/en/stable/tutorial.html
client = MongoClient('mongo', 27017)

tienda_db = client.tienda                   # Base de Datos
productos_collection = tienda_db.productos  # Colección  

# añade a BD
compras_collection = tienda_db.compras  # Colección

def productos100_200():
	productos_electronica = productos_collection.find({
            'precio': {'$gte': 100, '$lte': 200},
            'categoría': 'electronics'
        }).sort('precio', -1)
	return productos_electronica

def guardar_producto(nombre, precio, descripcion, categoria, imagen, rating):
	dato = { 
		'nombre': nombre, 
		'precio': precio, 
		'descripción': descripcion, 
		'categoría': categoria,
		'imágen': imagen, 
		'rating': {'puntuación': rating['puntuación'], 'cuenta': rating['cuenta']} 
	}
	logger.info(dato)
	try:
		productos_collection.insert_one(dato) 
	except:
		logger.info("Error al insertar el producto")

def mostrar_productos(categoria = None):

	if categoria == "men":
		categoria = "men's clothing"
	elif categoria == "women":
		categoria = "women's clothing"
	elif categoria == "jewelry":
		categoria = "jewelery"
	else:
		categoria = "electronics"
		

	productos = productos_collection.find({'categoría': categoria})
	productos = list(productos)
	
	for producto in productos:
		producto["id"] = str(producto['_id'])
		del producto["_id"]

	return productos

def busqueda(busqueda):
	productos_busqueda = productos_collection.find({
			'$or': [
				{'nombre': {'$regex': fr'\b{busqueda}\b', '$options': 'i'}},
				{'descripción': {'$regex': fr'\b{busqueda}\b', '$options': 'i'}}
			]
		})
	productos_busqueda = list(productos_busqueda)
	
	for producto in productos_busqueda:
		producto["id"] = str(producto['_id'])
		del producto["_id"]
	return productos_busqueda

def GetProducto(id):
	resu = productos_collection.find_one({"_id": ObjectId(id)})
	resu["id"] = str(resu.get('_id'))
	del resu["_id"]
	return resu

def BorrarProducto(id):
	productos_collection.delete_one({"_id": ObjectId(id)})

def ModificarProducto(id, payload):
	nuevos_datos = {
		"$set": {
			"nombre": payload.title,
			"precio": payload.price,
			"descripción": payload.description,
			"categoría": payload.category,
			"rating": {"puntuación": payload.rating.rate, "cuenta": payload.rating.count},
		}
	}
	productos_collection.update_one({"_id": ObjectId(id)}, nuevos_datos)

def GetProductosDesde(desde, hasta):
	productos = productos_collection.find().skip(desde).limit(hasta - desde)
	return productos
    

def productos_mayor_4():
	productos_puntuacion = productos_collection.find({
		'rating.puntuación': {'$gt': 4}
	})

	productos_puntuacion = list(productos_puntuacion)
	
	for producto in productos_puntuacion:
		producto["id"] = str(producto['_id'])
		del producto["_id"]
	
	return productos_puntuacion
    
def ropa_hombre():
	productos_hombre = productos_collection.find({
			'categoría': "men's clothing"
		}).sort('rating.puntuación', -1)
	return productos_hombre

def facturacion():
	facturacion_total = 0
	for com in compras_collection.find():
		lista_productos = com.get('productos')
		
		for p in lista_productos:
			id = p.get("productId")
			cantidad = p.get("quantity")
			#Obtenemos el producto:
			producto = productos_collection.find().skip(id-1).limit(1)
			precio = 0
			#Al obtener un puntero, debemos iterar sobre él para poder acceder a sus atributos:
			for p in producto:
				precio = p.get("precio")
			facturacion_total = facturacion_total + (precio * cantidad)
		
	return round(facturacion_total,2)

def facturacion_categorias():

	facturacion_total = 0
	categorias = getProductos('https://fakestoreapi.com/products/categories')

	#Creamos un diccionario para almacenar pares categoría-facturación:
	facturacion_categorias = {}
	for categoria in categorias:
		facturacion_categorias[categoria] = 0

	for com in compras_collection.find():
		lista_productos = com.get('productos')
		for p in lista_productos:
			id = p.get("productId")
			cantidad = p.get("quantity")
			producto = productos_collection.find().skip(id-1).limit(1)
			precio = 0
			categoria = ""
			for p in producto:
				precio = p.get("precio")
				categoria = p.get("categoría")

			facturacion_categorias[categoria] = facturacion_categorias[categoria] + (precio * cantidad)
			
	# for categoria in facturacion_categorias:
	# 	print("Facturación ", categoria, facturacion_categorias[categoria])

	return facturacion_categorias


	



