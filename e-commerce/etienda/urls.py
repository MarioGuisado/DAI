from django.urls import path
from .api import api
from . import views

import logging
logger = logging.getLogger(__name__)

urlpatterns = [
    path("", views.index, name="index"),
    path("productos100_200", views.productos100_200, name="productos100_200"),
    path("descripcion_pocket", views.descripcion_pocket, name="descripcion_pocket"),
    path("productos_mayor_4", views.productos_mayor_4, name="productos_mayor_4"),
    path("ropa_hombre", views.ropa_hombre, name="ropa_hombre"),
    path("facturacion_total", views.facturacion_total, name="facturacion_total"),
    path("facturacion_categorias", views.facturacion_categorias, name="facturacion_categorias"),
    path("mostrar_productos", views.mostrar_productos, name="mostrar_productos"),
    path("busqueda", views.busqueda, name="busqueda"),
    path("nuevo_producto", views.nuevo_producto, name="nuevo_producto"),
    path("api/", api.urls),
]