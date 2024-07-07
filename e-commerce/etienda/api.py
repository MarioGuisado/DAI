from ninja_extra import NinjaExtraAPI, api_controller, http_get
from ninja import Schema, NinjaAPI, File
from ninja.files import UploadedFile
from .models import BorrarProducto, GetProducto, GetProductosDesde, ModificarProducto, guardar_producto, mostrar_productos, busqueda
import logging
from typing import List
from ninja import NinjaAPI, File
from ninja.files import UploadedFile
import os


logger = logging.getLogger(__name__)
api = NinjaExtraAPI()

class Rate(Schema):
    rate: float
    count: int
    
class ProductSchema(Schema):  # serves for validation and documentation
    id: str
    title: str
    price: float
    description: str
    category: str
    image: str = None
    rating: Rate
	
	
class ProductSchemaIn(Schema):
	title: str
	price: float
	description: str
	category: str
	rating: Rate
	
	
class ErrorSchema(Schema):
	message: str
	
class AcceptedSchema(Schema):
    message: str

@api.put("/productos/{id}", tags=['TIENDA DAI'], response={202: AcceptedSchema, 404: ErrorSchema})
def Modifica_producto(request, id: str, payload: ProductSchemaIn):
    try:
        ModificarProducto(id, payload)
        return 202, {'message': 'Aceptado'}
    except:
        return 404, {'message': 'no encontrado'}


@api.get("/productos/{id}", tags=['TIENDA DAI'], response = {202: ProductSchema, 404: ErrorSchema})
def Detalle_producto(request, id: str):
	try:
		data = GetProducto(id)
		producto = ProductSchema(
            id=id,
            title=data.get('nombre'),
            price=data.get('precio'),
            description=data.get('descripción'),
            category=data.get("categoría"),
            image=data.get("imágen"),
            rating=Rate(rate=data.get("rating").get("puntuación"), count=data.get("rating").get("cuenta"))
        )
		return 202, producto
	except:
		return 404, {'message': 'no encontrado'}
	
@api.delete("/productos/{id}", tags=['TIENDA DAI'], response = {202: AcceptedSchema, 404: ErrorSchema})
def Delete_producto(request, id: str):
	try:
		print(GetProducto(id))
		BorrarProducto(id)
		return 202, {'message': 'Producto borrado'}
	except:
		return 404, {'message': 'Error'}


@api.post("/productos/", tags=['TIENDA DAI'], response = {202: AcceptedSchema, 404: ErrorSchema})
def Add_producto(request, payload: ProductSchemaIn, file: UploadedFile):
    try:
        rating = {
            "puntuación": 0,
            "cuenta": 1
        }
        with open('static/' + file.name, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        nombre_imagen = file.name
        guardar_producto(payload.title, payload.price, payload.description, payload.category, nombre_imagen, rating)

        return 202, {'message': 'Producto añadido'}
    except:
        return 404, {'message': 'Error'}
	

@api.get("/productos", tags=['TIENDA DAI'], response={200: List[ProductSchema], 404: ErrorSchema})
def Get_productos(request, desde: int = 0, hasta: int = 4):
	try:
		productos = GetProductosDesde(desde, hasta)
		lista: List[ProductSchema] = []
		for producto in productos:
			datos = ProductSchema(
                id=str(producto.get('_id')),
                title=producto.get('nombre'),
                price=producto.get("precio"),
                description=producto.get("descripción"),
                category=producto.get("categoría"),
                image=producto.get("imágen"),
                rating=Rate(rate=producto.get("rating").get("puntuación"), count=producto.get("rating").get("cuenta"))
            )
			lista.append(datos)
        
		return 200, lista
	except:
		return 404, {'message': 'no encontrado'}
	
@api.get("/productosCategoria/{categoria}", tags=['TIENDA DAI'], response={200: List[ProductSchema], 404: ErrorSchema})
def Productos_categoria(request, categoria:str):
	try:
		productos = mostrar_productos(categoria)
		lista: List[ProductSchema] = []
		for producto in productos:
			datos = ProductSchema(
                id=str(producto.get('_id')),
                title=producto.get('nombre'),
                price=producto.get("precio"),
                description=producto.get("descripción"),
                category=producto.get("categoría"),
                image=producto.get("imágen"),
                rating=Rate(rate=producto.get("rating").get("puntuación"), count=producto.get("rating").get("cuenta"))
            )
			lista.append(datos)
        
		return 200, lista
	except:
		return 404, {'message': 'no encontrado'}
	
@api.get("/productosBusqueda/{producto}", tags=['TIENDA DAI'], response={200: List[ProductSchema], 404: ErrorSchema})
def Productos_busqueda(request, producto:str):
	try:
		productos = busqueda(producto)
		lista: List[ProductSchema] = []
		for producto in productos:
			datos = ProductSchema(
                id=str(producto.get('_id')),
                title=producto.get('nombre'),
                price=producto.get("precio"),
                description=producto.get("descripción"),
                category=producto.get("categoría"),
                image=producto.get("imágen"),
                rating=Rate(rate=producto.get("rating").get("puntuación"), count=producto.get("rating").get("cuenta"))
            )
			lista.append(datos)
        
		return 200, lista
	except:
		return 404, {'message': 'no encontrado'}