import sqlite3
import sys

import pytest

from controller import crearBdController
from model.rutas import ruta_base_datos


@pytest.fixture
def bd(tmp_path, monkeypatch):
    """Base de datos vacía con el esquema completo, en una carpeta temporal.

    En desarrollo ruta_base_datos() usa ./database, así que basta con cambiar
    el directorio de trabajo. La base real del proyecto nunca se toca.
    """
    monkeypatch.chdir(tmp_path)
    crearBdController.existeBase()
    return ruta_base_datos()


@pytest.fixture
def consultar(bd):
    """Ejecuta una consulta directa sobre la base temporal y devuelve todas las filas."""
    def _consultar(sql, parametros=()):
        conexion = sqlite3.connect(bd)
        try:
            return conexion.execute(sql, parametros).fetchall()
        finally:
            conexion.close()
    return _consultar


@pytest.fixture
def empaquetado(tmp_path, monkeypatch):
    """Simula la app empaquetada con PyInstaller (sys.frozen, sys._MEIPASS, %APPDATA%)."""
    meipass = tmp_path / 'meipass'
    appdata = tmp_path / 'appdata'
    meipass.mkdir()
    monkeypatch.setattr(sys, 'frozen', True, raising=False)
    monkeypatch.setattr(sys, '_MEIPASS', str(meipass), raising=False)
    monkeypatch.setenv('APPDATA', str(appdata))
    return meipass, appdata
