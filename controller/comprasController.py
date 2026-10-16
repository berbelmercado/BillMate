import sqlite3
from model.compras import Compras

EN_BLANCO = 'No se permite enviar la descripción en blanco'


def formatearDescripcion(descripcionCompra):
    #Primera letra de cada palabra en mayúscula y sin espacios a los lados
    return descripcionCompra.strip().title()


def insertarCompra(descripcionCompra, fechaCreacionCompra):
    #Registra una compra nueva; la fecha llega en AAAA-MM-DD
    descripcionCompra = formatearDescripcion(descripcionCompra)
    if descripcionCompra == '':
        return [0, EN_BLANCO]

    try:
        idCompra = Compras(None, descripcionCompra, fechaCreacionCompra).insertarCompras()
        return [1,'Se insertó correctamente la compra', idCompra]
    except sqlite3.Error as ex:
        return [0,f'Error al insertar la compra: {ex}']


def consultarListaCompras():
    #Todas las compras, para llenar la tabla al abrir la vista
    try:
        return Compras(None, None, None).buscarComprasRegistradas(), [1,'']
    except sqlite3.Error as ex:
        return [], [0,f'Error al consultar compras registradas: {ex}']


def consultarCompras(descripcionCompra):
    #Compras cuya descripción contiene el texto buscado
    try:
        return Compras(None, descripcionCompra, None).consultarCompras(), [1]
    except sqlite3.Error as ex:
        return [], [0,f'Error al consultar la compra: {ex}']


def modificarCompra(idCompra, descripcionCompra):
    #Cambia la descripción de una compra existente
    descripcionCompra = formatearDescripcion(descripcionCompra)
    if descripcionCompra == '':
        return [0, EN_BLANCO]

    try:
        Compras(idCompra, descripcionCompra, None).modificarCompras()
        return [1,'Se modificó la compra correctamente']
    except sqlite3.Error as ex:
        return [0,f'Error al modificar la compra: {ex}']
