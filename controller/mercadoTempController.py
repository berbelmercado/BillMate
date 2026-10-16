import sqlite3
from model.mercadoTemp import MercadoTemp
from model.mercadoTemp import cargarCompraModel
from controller.validaciones import esNumero, convertirNumero

MENSAJES_VALIDACION = {0: 'No se permiten campos vacíos'
                       ,2: 'El campo "Precio unidad" no es válido'
                       ,3: 'El campo "Precio Total" no es válido'}


def validarCamposMercadoTemp(compraId, facturaId, productoId, comercioId, precioUnidad, precioTotal):
    #1 si todo está bien; 0 si falta compra, factura, producto o comercio;
    #2 si el precio unidad no es un número; 3 si el precio total no lo es (el último error encontrado gana)
    estado = 1
    if compraId is None or facturaId is None or productoId is None or comercioId is None:
        estado = 0
    if not esNumero(precioUnidad):
        estado = 2
    if not esNumero(precioTotal):
        estado = 3
    return estado


def insertarMercadoTemp(compraId, facturaId, productoId, comercioId, cantidad, precioUnidad, precioTotal):
    #Agrega un ítem a la compra en curso (tabla mercadosTemp)
    estado = validarCamposMercadoTemp(compraId, facturaId, productoId, comercioId, precioUnidad, precioTotal)
    if estado != 1:
        return [0, MENSAJES_VALIDACION[estado]]

    try:
        MercadoTemp(None, compraId, facturaId, productoId, comercioId, cantidad
                    ,convertirNumero(precioUnidad), convertirNumero(precioTotal)).insertarMercadoTempral()
        return [1,'Producto agregado']
    except sqlite3.Error as ex:
        return [0, f'No fue posible insertar el producto Error: {ex}']


def consultarMercadoTemp():
    #Ítems de la compra en curso
    try:
        return MercadoTemp(*[None] * 8).consultarMercadosTemporal(), [1]
    except sqlite3.Error as ex:
        return [], [0,f'No se pudo conectar a la bd error: {ex}']


def actualizarMercadoTemp(mercadoIdTemp, compraId, facturaId, productoId, comercioId, cantidad, precioUnidad, precioTotal):
    #Modifica un ítem de la compra en curso
    estado = validarCamposMercadoTemp(compraId, facturaId, productoId, comercioId, precioUnidad, precioTotal)
    if estado != 1:
        return [0, MENSAJES_VALIDACION[estado]]

    try:
        MercadoTemp(mercadoIdTemp, compraId, facturaId, productoId, comercioId, cantidad
                    ,convertirNumero(precioUnidad), convertirNumero(precioTotal)).actualizarProductoTemporal()
        return [1,'Producto Modificado']
    except sqlite3.Error as ex:
        return [0,f'No fue posible modificar el producto Error: {ex}']


def consultarLlavesMercadoTemp(mercadoIdTemp):
    #compraId, facturaId, productoId y comercioId del ítem
    try:
        return MercadoTemp(mercadoIdTemp, *[None] * 7).consultarKeysMercadosTempModel(), [1,'']
    except sqlite3.Error as ex:
        return [], [0,f'Error al consultar llaves: {ex}']


def eliminarMercadoTemp(mercadoIdTemp):
    #Quita un ítem de la compra en curso
    try:
        MercadoTemp(mercadoIdTemp, *[None] * 7).eliminarMercadoTemporal()
        return [1]
    except sqlite3.Error as ex:
        return [0,f'No se pudo eliminar el producto error: {ex}']


def cargarCompra():
    #Pasa los ítems de mercadosTemp a mercados y vacía la compra en curso
    try:
        cargarCompraModel()
        return [1, 'Se ha cargado la compra correctamente']
    except sqlite3.Error as ex:
        return [0,f'No fue posible cargar la compra Error: {ex}']
