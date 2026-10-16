import os
import sqlite3

import pytest

from controller import crearBdController
from controller.mercadoTempController import MercadoTempController, fnCargarCompraController
from model import migraciones
from model.crearTablasBd import CreacionBbBillMate
from model.rutas import ruta_base_datos


def consultar(ruta, sql):
    conexion = sqlite3.connect(ruta)
    try:
        return conexion.execute(sql).fetchall()
    finally:
        conexion.close()


def tablas(ruta):
    return {nombre for (nombre,) in consultar(ruta, "SELECT name FROM sqlite_master WHERE type='table'")}


def claves_foraneas(ruta, tabla):
    return sorted((fila[3], fila[2], fila[4]) for fila in consultar(ruta, f'PRAGMA foreign_key_list({tabla})'))


@pytest.fixture
def bd_v0(tmp_path, monkeypatch):
    """Base con el esquema original (versión 0) y datos como los de una instalación vieja."""
    monkeypatch.chdir(tmp_path)
    CreacionBbBillMate()
    ruta = ruta_base_datos()
    conexion = sqlite3.connect(ruta)
    conexion.executescript("""
        INSERT INTO productos VALUES (1, 'Arroz'), (2, 'Leche');
        INSERT INTO facturas VALUES (NULL, 'FE001', 12500.0, '2024/09/07');
        INSERT INTO comercios VALUES (NULL, 'Tienda', 'Calle 1');
        INSERT INTO compras VALUES (NULL, 'Quincena', '2024-09-08');
        INSERT INTO mercados VALUES (1, 1, 1, 1, 1, '2 kg', 3500.0, 7000.0);
        INSERT INTO mercados VALUES (30, 'None', 'None', 'None', 'None', '1', '', '');
        INSERT INTO mercados VALUES (31, 1, 1, 2, 1, '1', 4200.0, 4200.0);
    """)
    conexion.commit()
    conexion.close()
    return ruta


def test_base_nueva_queda_en_la_ultima_version(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    crearBdController.existeBase()
    ruta = ruta_base_datos()

    assert consultar(ruta, 'PRAGMA user_version') == [(len(migraciones.MIGRACIONES),)]
    assert claves_foraneas(ruta, 'mercados') == [
        ('comercioId', 'comercios', 'comercioId'),
        ('compraId', 'compras', 'idCompra'),
        ('facturaId', 'facturas', 'facturaId'),
        ('productoId', 'productos', 'productoId')]
    assert len(claves_foraneas(ruta, 'mercadosTemp')) == 4
    assert 'estado' not in tablas(ruta)
    assert 'descripcion' in [fila[1] for fila in consultar(ruta, 'PRAGMA table_info(compras)')]
    assert not os.path.exists(f'{ruta}.respaldo-v0')


def test_migracion_conserva_datos_y_borra_filas_basura(bd_v0):
    crearBdController.existeBase()

    assert consultar(bd_v0, 'SELECT * FROM mercados ORDER BY mercadoId') == [
        (1, 1, 1, 1, 1, '2 kg', 3500.0, 7000.0),
        (31, 1, 1, 2, 1, '1', 4200.0, 4200.0)]
    assert consultar(bd_v0, 'SELECT * FROM compras') == [(1, 'Quincena', '2024-09-08')]
    assert consultar(bd_v0, 'SELECT COUNT(*) FROM productos') == [(2,)]
    assert consultar(bd_v0, 'PRAGMA foreign_key_check') == []


def test_migracion_unifica_fechas_de_facturas(bd_v0):
    crearBdController.existeBase()

    assert consultar(bd_v0, 'SELECT fechaFactura FROM facturas') == [('2024-09-07',)]


def test_migracion_2_solo_cambia_fechas_con_formato_esperado(tmp_path, monkeypatch):
    #Base ya en la versión 1 (instalaciones de la 1.8) con fechas en varios formatos
    monkeypatch.chdir(tmp_path)
    crearBdController.existeBase()
    ruta = ruta_base_datos()
    conexion = sqlite3.connect(ruta)
    conexion.executescript("""
        DROP INDEX productos_nombre_unico;
        PRAGMA user_version = 1;
        INSERT INTO facturas VALUES (NULL, 'A', 1.0, '2026/10/15');
        INSERT INTO facturas VALUES (NULL, 'B', 1.0, '2026-10-16');
        INSERT INTO facturas VALUES (NULL, 'C', 1.0, '15/10/2026');
    """)
    conexion.commit()
    conexion.close()

    crearBdController.existeBase()

    assert consultar(ruta, 'SELECT fechaFactura FROM facturas ORDER BY numeroFactura') == [
        ('2026-10-15',), ('2026-10-16',), ('15/10/2026',)]
    assert consultar(ruta, 'PRAGMA user_version') == [(len(migraciones.MIGRACIONES),)]
    assert consultar(f'{ruta}.respaldo-v1', 'SELECT fechaFactura FROM facturas WHERE numeroFactura = \'A\'') == [('2026/10/15',)]


def test_migracion_3_une_productos_duplicados(tmp_path, monkeypatch):
    #Base en la versión 2, sin el índice único, con productos repetidos en uso
    monkeypatch.chdir(tmp_path)
    crearBdController.existeBase()
    ruta = ruta_base_datos()
    conexion = sqlite3.connect(ruta)
    conexion.executescript("""
        DROP INDEX productos_nombre_unico;
        PRAGMA user_version = 2;
        INSERT INTO productos VALUES (1, 'Arroz'), (2, 'Leche'), (3, 'Arroz'), (4, 'arroz ');
        INSERT INTO facturas VALUES (1, 'FE001', 12500.0, '2026-10-15');
        INSERT INTO comercios VALUES (1, 'Tienda', 'Calle 1');
        INSERT INTO compras VALUES (1, 'Quincena', '2026-10-15');
        INSERT INTO mercados VALUES (1, 1, 1, 3, 1, '1', 100.0, 100.0), (2, 1, 1, 2, 1, '1', 200.0, 200.0);
        INSERT INTO mercadosTemp VALUES (1, 1, 1, 4, 1, '1', 100.0, 100.0);
    """)
    conexion.commit()
    conexion.close()

    crearBdController.existeBase()

    assert consultar(ruta, 'SELECT * FROM productos ORDER BY productoId') == [(1, 'Arroz'), (2, 'Leche')]
    assert consultar(ruta, 'SELECT mercadoId, productoId FROM mercados ORDER BY mercadoId') == [(1, 1), (2, 2)]
    assert consultar(ruta, 'SELECT productoIdTemp FROM mercadosTemp') == [(1,)]
    assert consultar(ruta, 'PRAGMA foreign_key_check') == []
    assert consultar(f'{ruta}.respaldo-v2', 'SELECT COUNT(*) FROM productos') == [(4,)]


def test_migracion_crea_respaldo_con_los_datos_originales(bd_v0):
    crearBdController.existeBase()

    respaldo = f'{bd_v0}.respaldo-v0'
    assert consultar(respaldo, 'PRAGMA user_version') == [(0,)]
    assert consultar(respaldo, 'SELECT COUNT(*) FROM mercados') == [(3,)]
    assert 'estado' in tablas(respaldo)


def test_migrar_dos_veces_no_cambia_nada(bd_v0):
    crearBdController.existeBase()
    os.remove(f'{bd_v0}.respaldo-v0')
    antes = consultar(bd_v0, 'SELECT * FROM mercados')

    crearBdController.existeBase()

    assert consultar(bd_v0, 'SELECT * FROM mercados') == antes
    assert not os.path.exists(f'{bd_v0}.respaldo-v0')


def test_ids_temporales_siguen_reiniciandose_tras_migrar(bd_v0):
    crearBdController.existeBase()
    agregar = lambda: MercadoTempController(None, 1, 1, 1, 1, '1', '100', '100').insertarMercadosTempController()
    agregar()
    agregar()
    assert fnCargarCompraController()[0] == 1

    agregar()

    assert consultar(bd_v0, 'SELECT mercadoIdTemp FROM mercadosTemp') == [(1,)]
    assert consultar(bd_v0, 'SELECT MAX(mercadoId) FROM mercados') == [(33,)]


def test_claves_foraneas_activas_en_la_app(bd):
    #El producto 99 no existe: SQLite rechaza la fila y el controlador devuelve el error
    mensaje = MercadoTempController(None, 1, 1, 99, 1, '1', '100', '100').insertarMercadosTempController()
    assert mensaje[0] == 0
    assert 'FOREIGN KEY constraint failed' in mensaje[1]


def test_migracion_fallida_deja_la_base_intacta(bd_v0, monkeypatch):
    def migracion_que_falla(conexion):
        conexion.execute('DROP TABLE estado')
        raise RuntimeError('falla a propósito')

    monkeypatch.setattr(migraciones, 'MIGRACIONES', [migracion_que_falla])

    with pytest.raises(RuntimeError):
        crearBdController.existeBase()

    assert consultar(bd_v0, 'PRAGMA user_version') == [(0,)]
    assert 'estado' in tablas(bd_v0)
    assert consultar(bd_v0, 'SELECT COUNT(*) FROM mercados') == [(3,)]
