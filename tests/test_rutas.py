import sqlite3

from controller import crearBdController
from model.rutas import ruta_base_datos

TABLAS = ['comercios', 'compras', 'facturas', 'mercados', 'mercadosTemp', 'productos']


def tablas_de(ruta):
    conexion = sqlite3.connect(ruta)
    filas = conexion.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'").fetchall()
    conexion.close()
    return sorted(nombre for (nombre,) in filas)


def test_desarrollo_usa_carpeta_database(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert ruta_base_datos() == str(tmp_path / 'database' / 'BillMate.db')
    assert (tmp_path / 'database').is_dir()


def test_empaquetado_usa_appdata(empaquetado):
    _, appdata = empaquetado
    assert ruta_base_datos() == str(appdata / 'BillMate' / 'BillMate.db')


def test_empaquetado_migra_base_de_la_version_1_6(empaquetado):
    meipass, appdata = empaquetado
    (meipass / 'Database').mkdir()
    vieja = sqlite3.connect(meipass / 'Database' / 'BillMate.db')
    vieja.execute("CREATE TABLE marca(x)")
    vieja.execute("INSERT INTO marca VALUES(42)")
    vieja.commit()
    vieja.close()

    ruta = ruta_base_datos()

    assert sqlite3.connect(ruta).execute("SELECT x FROM marca").fetchone() == (42,)


def test_migracion_no_sobrescribe_base_existente(empaquetado):
    meipass, _ = empaquetado
    (meipass / 'Database').mkdir()
    vieja = sqlite3.connect(meipass / 'Database' / 'BillMate.db')
    vieja.execute("CREATE TABLE vieja(x)")
    vieja.close()
    ruta = ruta_base_datos()

    conexion = sqlite3.connect(ruta)
    conexion.execute("CREATE TABLE nueva(x)")
    conexion.commit()
    conexion.close()
    ruta_base_datos()

    assert 'nueva' in tablas_de(ruta)


def test_instalacion_nueva_crea_esquema_completo(empaquetado):
    crearBdController.existeBase()
    assert tablas_de(ruta_base_datos()) == TABLAS
