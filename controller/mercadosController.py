import sqlite3
from model.mercados import Mercados, gastoDelMesModel
from controller.validaciones import esNumero, convertirNumero

#Opciones de búsqueda de Consultar Mercados (índices de Mercados.sqlOpciones)
OPCION_PRODUCTO, OPCION_FACTURA, OPCION_COMPRA = 0, 1, 2


def mercado(mercadoId=None, compraId=None, facturaId=None, productoId=None, comercioId=None
            ,cantidad=None, precioUnidad=None, precioTotal=None, opcion=None, texto=None):
    #Objeto del modelo; el texto buscado ocupa el campo de las tres opciones de búsqueda
    return Mercados(mercadoId, compraId, texto, facturaId, texto, productoId, texto
                    ,comercioId, cantidad, precioUnidad, precioTotal, opcion)


def consultarMercados(opcion, texto):
    #Mercados cuyo producto, factura o compra (según la opción) contiene el texto buscado
    if opcion not in (OPCION_PRODUCTO, OPCION_FACTURA, OPCION_COMPRA):
        return [], [0, 'Por favor seleccione una opción']
    try:
        return mercado(opcion=opcion, texto=texto).consultarMercadosModel(), [1]
    except sqlite3.Error as ex:
        return [], [0, f'No se pudo realizar la consulta: {ex}']


def consultarUltimoMercado():
    #Ítems de la compra más reciente, para la tabla de la ventana principal
    try:
        return mercado().consultarUltimoMercado(), [1]
    except sqlite3.Error as ex:
        return [], [0, f'No fue posible realizar la consulta: {ex}']


def gastoDelMes(anioMes):
    #Total comprado en el mes 'AAAA-MM' (por fecha de factura), para la pantalla de inicio
    try:
        return gastoDelMesModel(anioMes), [1]
    except sqlite3.Error as ex:
        return 0, [0, f'No fue posible calcular el gasto del mes: {ex}']


def actualizarMercado(mercadoId, compraId, facturaId, productoId, comercioId, cantidad, precioUnidad, precioTotal):
    #Modifica un ítem ya cargado en mercados
    if not esNumero(precioUnidad):
        return [0, 'El campo "Precio unidad" no es válido']
    if not esNumero(precioTotal):
        return [0, 'El campo "Precio Total" no es válido']

    try:
        mercado(mercadoId, compraId, facturaId, productoId, comercioId, cantidad
                ,convertirNumero(precioUnidad), convertirNumero(precioTotal)).actualizarMercadosModel()
        return [1,'']
    except sqlite3.Error as ex:
        return [0,f'No se pudo actualizar el producto: {ex}']


def consultarLlavesMercado(mercadoId):
    #compraId, facturaId, productoId y comercioId del ítem
    try:
        return mercado(mercadoId).consultarKeysMercadosModel(), [1,'']
    except sqlite3.Error as ex:
        return [], [0,f'Error al consultar llaves: {ex}']


def eliminarMercado(mercadoId):
    #Borra un ítem de mercados
    try:
        mercado(mercadoId).eliminarProductosModel()
        return [1,'Fue eliminado el producto']
    except sqlite3.Error as ex:
        return [0,f'No es posible eliminar el producto: {ex}']
