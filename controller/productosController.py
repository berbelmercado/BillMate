import sqlite3
from model.productos import  Productos


def formatearNombre(nombreProducto):
    #Primera letra de cada palabra en mayúscula y sin espacios a los lados
    return nombreProducto.strip().title()


def insertarProducto(nombreProducto):
    #Inserta un producto nuevo en la BD
    nombreProducto = formatearNombre(nombreProducto)
    if nombreProducto == '':
        return [0,'No se admiten campos vacíos']

    try:
        Productos(None, nombreProducto).insertarProductos()
        return [1,'Se insertó el producto correctamente']
    except sqlite3.IntegrityError:
        return [0, f'Ya existe un producto llamado "{nombreProducto}"']
    except sqlite3.Error as ex:
        return [0, f'No se insertó el producto: {ex}']


def consultarListaProductos():
    #Todos los productos, para llenar la tabla al abrir la vista
    try:
        return Productos(None, None).consultarListaProductos(), [1]
    except sqlite3.Error as ex:
        return [], [0, f'No fue posible consultar lista de productos: {ex}']


def consultarProductos(nombreProducto):
    #Productos cuyo nombre contiene el texto buscado
    try:
        return Productos(None, nombreProducto).consultarProductos(), [1]
    except sqlite3.Error as ex:
        return [], [0, f'No fue posible consultar productos: {ex}']


def editarProducto(productoId, nombreProducto):
    #Cambia el nombre de un producto existente
    nombreProducto = formatearNombre(nombreProducto)
    if nombreProducto == '':
        return [0,'No se admiten campos vacíos']

    try:
        Productos(productoId, nombreProducto).editarProductos()
        return [1,'Se modificó el producto correctamente']
    except sqlite3.IntegrityError:
        return [0, f'Ya existe un producto llamado "{nombreProducto}"']
    except sqlite3.Error as ex:
        return [0, f'No se modificó el producto: {ex}']
