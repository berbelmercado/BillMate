"""Ubicación de la base de datos de BillMate."""
import os
import shutil
import sys


def ruta_base_datos():
    """Devuelve la ruta de BillMate.db y crea su carpeta si no existe.

    Empaquetado (PyInstaller): %APPDATA%\\BillMate. Se puede escribir sin permisos de
    administrador y el instalador no la toca, así que los datos sobreviven a
    actualizaciones y desinstalaciones.
    En desarrollo: la carpeta database del proyecto.
    """
    if getattr(sys, 'frozen', False):
        carpeta = os.path.join(os.environ['APPDATA'], 'BillMate')
    else:
        carpeta = os.path.abspath('database')

    os.makedirs(carpeta, exist_ok=True)
    ruta = os.path.join(carpeta, 'BillMate.db')

    if not os.path.exists(ruta):
        migrarBdAnterior(ruta)

    return ruta


def migrarBdAnterior(rutaNueva):
    #Hasta la versión 1.6 la base viajaba dentro del ejecutable (_internal\Database).
    #Si existe, se copia a la nueva ubicación para no perder los datos del usuario.
    if not getattr(sys, 'frozen', False):
        return

    rutaAnterior = os.path.join(sys._MEIPASS, 'Database', 'BillMate.db')
    if os.path.exists(rutaAnterior):
        shutil.copy2(rutaAnterior, rutaNueva)
