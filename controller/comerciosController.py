import sqlite3
from model.comercios import Comercios


def formatearTexto(texto):
    #Primera letra de cada palabra en mayúscula y sin espacios a los lados
    return texto.strip().title()


def insertarComercio(nombreComercio, direccionComercio):
    #Inserta un comercio nuevo en la BD
    nombreComercio = formatearTexto(nombreComercio)
    direccionComercio = formatearTexto(direccionComercio)
    if nombreComercio == '' or direccionComercio == '':
        return [0, 'No se admiten campos vacíos']

    try:
        Comercios(None, nombreComercio, direccionComercio).insertarComercios()
        return [1, 'Se insertó correctamente el comercio']
    except sqlite3.Error as ex:
        return [0, f'No se pudo insertar el comercio: {ex}']


def consultarListaComercios():
    #Todos los comercios, para llenar la tabla al abrir la vista
    try:
        return Comercios(None, None, None).consultarComercios(), [1, '']
    except sqlite3.Error as ex:
        return [], [0, f'No se pudo consultar los comercios: {ex}']


def consultarComercios(nombreComercio):
    #Comercios cuyo nombre contiene el texto buscado
    try:
        return Comercios(None, nombreComercio, None).consultarComercioModel(), [1, '']
    except sqlite3.Error as ex:
        return [], [0, f'No se pudo consultar los comercios: {ex}']


def modificarComercio(comercioId, nombreComercio, direccionComercio):
    #Cambia el nombre y la dirección de un comercio existente
    nombreComercio = formatearTexto(nombreComercio)
    direccionComercio = formatearTexto(direccionComercio)
    if nombreComercio == '' or direccionComercio == '':
        return [0, 'No se admiten campos vacíos']

    try:
        Comercios(comercioId, nombreComercio, direccionComercio).modificarComerciosModel()
        return [1, 'Se actualizó el comercio']
    except sqlite3.Error as ex:
        return [0, f'No se pudo actualizar el comercio: {ex}']
