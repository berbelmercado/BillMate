import sqlite3
from model.facturas import Facturas
from controller.validaciones import convertirNumero

VACIOS = [0, 'No se admiten campos vacíos. Por favor valide nuevamente']
NO_NUMERICO = [2, 'Solo se admiten caracteres númericos en el campo "Total Factura"']


def validarCamposFactura(numeroFactura, valorTotalFactura, fechaFactura):
    #0 si hay campos vacíos, 2 si el total no es numérico (acepta 12.500 y 12.500,50), 1 si todo está bien
    if numeroFactura.strip()=='' or valorTotalFactura.strip()=='' or fechaFactura.strip()=='':
        return 0
    if convertirNumero(valorTotalFactura) is None:
        return 2
    return 1


def insertarFactura(numeroFactura, valorTotalFactura, fechaFactura):
    #Inserta una factura nueva en la BD
    estado = validarCamposFactura(numeroFactura, valorTotalFactura, fechaFactura)
    if estado == 0:
        return list(VACIOS)
    if estado == 2:
        return list(NO_NUMERICO)

    try:
        facturaId = Facturas(None
                             ,numeroFactura.strip().upper()
                             ,convertirNumero(valorTotalFactura)
                             ,fechaFactura).insertarFacturas()
        return [1,'Factura ingresada correctamente', facturaId]
    except sqlite3.Error as ex:
        return [0,f'Error al insertar factura: {ex}']


def consultarListaFacturas():
    #Todas las facturas, para llenar la tabla al abrir la vista
    try:
        return Facturas(None, None, None, None).consultarListaFacturas(), [1,'']
    except sqlite3.Error as ex:
        return [], [0,f'No se pudo obtener información de las facturas: {ex}']


def consultarFacturas(numeroFactura):
    #Facturas cuyo número contiene el texto buscado
    try:
        return Facturas(None, numeroFactura, None, None).consultarFacturasModel(), [1, '']
    except sqlite3.Error as ex:
        return [], [0,f'Problemas con la conexión a la base de datos: {ex}']


def modificarFactura(facturaId, numeroFactura, valorTotalFactura, fechaFactura):
    #Cambia número, total y fecha de una factura existente
    estado = validarCamposFactura(numeroFactura, valorTotalFactura, fechaFactura)
    if estado == 0:
        return list(VACIOS)
    if estado == 2:
        return list(NO_NUMERICO)

    try:
        Facturas(facturaId
                 ,numeroFactura.strip().upper()
                 ,convertirNumero(valorTotalFactura)
                 ,fechaFactura).modificarFacturas()
        return [1,'Factura modificada correctamente']
    except sqlite3.Error as ex:
        return [0,f'Error al modificar factura: {ex}']
