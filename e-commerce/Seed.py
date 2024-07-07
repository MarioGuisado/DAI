# Seed.py
# Autor: Mario Guisado García
from pydantic import BaseModel, FilePath, Field, EmailStr, ValidationError, ValidationInfo, validator
from pymongo import MongoClient
from pprint import pprint
from datetime import datetime
from typing import Any
import requests
import os



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


dato = { 
	'nombre': "MBJ Women's Solid Short Sleeve Boat Neck V ", 
	'precio': 9.85, 
	'descripción': '95% RAYON 5% SPANDEX, Made in USA or Imported, Do Not Bleach, Lightweight fabric with great stretch for comfort, Ribbed on sleeves and neckline / Double stitching on bottom hem', 'category': "women's clothing", 
	'categoría': "women's clothing",
	'imágen': None, 
	'rating': {'puntuación': 4.7, 'cuenta': 130}
}

# Valida con el esquema:
# daría error si no corresponde algún tipo 
producto = Producto(**dato)

# print(producto.descripción)
# pprint(producto.model_dump()) # Objeto -> python dict


# Conexión con la BD				
# https://pymongo.readthedocs.io/en/stable/tutorial.html
client = MongoClient('mongo', 27017)

tienda_db = client.tienda                   # Base de Datos
productos_collection = tienda_db.productos  # Colección  
productos_collection.delete_many({})
				
# print(productos_collection.count_documents({}))

# todos los productos
lista_productos_ids = []
for prod in productos_collection.find():
	# pprint(prod)
	# print(prod.get('_id'))   # Autoinsertado por mongo
	lista_productos_ids.append(prod.get('_id'))
	
# print(lista_productos_ids)
	
	
							
productos = getProductos('https://fakestoreapi.com/products')

#DESCARGAMOS IMÁGENES E INTRODUCIMOS LOS PRODUCTOS
#------------------------------------------------------------
contador = 0
for p in productos:
	titulo = "imagen" + str(contador) + ".jpg"
	if not os.path.exists(titulo):
		url_imagen = p["image"]
		response = requests.get(url_imagen)
		if response.status_code == 200:
			with open(titulo, 'wb') as file:
				file.write(response.content)
		else:
			print("Error al descargar la imagen.", response.status_code)
	contador = contador + 1
	
	dato = { 
		'nombre': p['title'].capitalize(), #Nos aseguramos que el nombre comience por mayúscula
		'precio': p['price'], 
		'descripción': p['description'], 
		'categoría': p['category'],
		'imágen': titulo, 
		'rating': {'puntuación': p['rating']['rate'], 'cuenta': p['rating']['count']}
	}
	producto = Producto(**dato)
	productos_collection.insert_one(producto.model_dump()) 

#------------------------------------------------------------

# añade a BD
compras_collection = tienda_db.compras  # Colección
compras_collection.delete_many({})

compras = getProductos('https://fakestoreapi.com/carts')
for com in compras:
	#Creamos la compra:
	nueva_compra = {
		'usuario': 'fulanito@correo.com',
		'fecha': datetime.now(),
		'productos': com.get('products')
	}
	compra = Compra(**nueva_compra)
	compras_collection.insert_one(compra.model_dump())


print("A continuación, se muestran los productos de eletrónica entre 100 y 200 euros \n")
productos_electronica = productos_collection.find({
        'precio': {'$gte': 100, '$lte': 200},
        'categoría': 'electronics'
    }).sort('precio', -1)
for producto in productos_electronica:
    print(producto.get("nombre"),"\n", producto.get("precio"),"\n",producto.get("descripción"),"\n",producto.get("imágen"),"\n")

print("\n A continuación, se muestran los productos que contienen la palabra pocket en su descripción \n")

productos_pocket = productos_collection.find({
        'descripción': {'$regex': 'pocket', '$options': 'i'}
    })
for producto in productos_pocket:
    print(producto.get("nombre"),"\n", producto.get("precio"),"\n",producto.get("descripción"),"\n",producto.get("imágen"),"\n")

print("\n A continuación, se muestran los productos con puntuación mayor que 4 \n")

productos_puntuacion = productos_collection.find({
        'rating.puntuación': {'$gt': 4}
    })
for producto in productos_puntuacion:
    print(producto.get("nombre"),"\n", producto.get("precio"),"\n",producto.get("descripción"),"\n",producto.get("imágen"),"\n")

print("\n A continuación, se muestra ropa de hombre, ordenada por puntuación \n")

productos_hombre = productos_collection.find({
        'categoría': "men's clothing"
    }).sort('rating.puntuación', -1)
for producto in productos_hombre:
    print(producto.get("nombre"),"\n", producto.get("precio"),"\n",producto.get("descripción"),"\n",producto.get("imágen"),"\n")

print("\n A continuación, se muestra la facturación total \n")


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
	
print(round(facturacion_total,2))

print("\n A continuación, se muestra la facturación por categoría de producto \n")

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

for categoria in facturacion_categorias:
	print("Facturación ", categoria, facturacion_categorias[categoria])
	



