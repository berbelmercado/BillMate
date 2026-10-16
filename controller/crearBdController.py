import os
from model.crearTablasBd import CreacionBbBillMate, existeBd
from model.rutas import ruta_base_datos

def  existeBase():
        
        estado = existeBd()

        if estado==1:
            pass
        if estado==0:
              objCreacionBD = CreacionBbBillMate()

def abrirCarpetaDatosController():
    #Abre en el Explorador la carpeta donde está BillMate.db
    mensaje = []

    try:
        os.startfile(os.path.dirname(ruta_base_datos()))
        mensaje = [1, '']
    except OSError as ex:
        mensaje = [0, f'No se pudo abrir la carpeta de datos: {ex}']

    return mensaje
