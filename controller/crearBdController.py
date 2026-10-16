import os
from model.crearTablasBd import CreacionBbBillMate, existeBd
from model.migraciones import aplicarMigraciones
from model.rutas import ruta_base_datos

def  existeBase():
        #Crea la base si no existe (esquema versión 0) y la lleva a la versión actual
        estado = existeBd()

        if estado==0:
              objCreacionBD = CreacionBbBillMate()

        #Solo se respalda una base que ya tenía datos
        aplicarMigraciones(ruta_base_datos(), respaldar=(estado==1))

def abrirCarpetaDatosController():
    #Abre en el Explorador la carpeta donde está BillMate.db
    mensaje = []

    try:
        os.startfile(os.path.dirname(ruta_base_datos()))
        mensaje = [1, '']
    except OSError as ex:
        mensaje = [0, f'No se pudo abrir la carpeta de datos: {ex}']

    return mensaje
