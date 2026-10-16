"""Pruebas de controladores y modelos contra una base SQLite temporal."""
from controller.productosController import ProductosController
from controller.comerciosController import ComerciosController
from controller.facturasController import FacturaController
from controller.comprasController import ComprasController
from controller.mercadoTempController import MercadoTempController, fnCargarCompraController
from controller.mercadosController import MercadosController

OPCION_PRODUCTO, OPCION_FACTURA, OPCION_COMPRA = 0, 1, 2


def registrar_datos_base():
    #Producto, comercio, factura y compra con apóstrofes (id 1 en cada tabla)
    assert ProductosController(None, "D'onofrio").insertarProducto()[0] == 1
    assert ProductosController(None, 'Arroz').insertarProducto()[0] == 1
    assert ComerciosController(None, "Tienda D'Luis", 'Calle 5 #3-2').insertarComercios()[0] == 1
    assert FacturaController(None, "fe'001", '12500', '2026/10/15').insertarFacturas()[0] == 1
    assert ComprasController(None, "Mercado 'quincena'", '2026/10/15').insertarCompras()[0] == 1


def mercado_temp(mercadoId=None, productoId=1, cantidad='2 kg', precioUnidad='3500', precioTotal='7000'):
    return MercadoTempController(mercadoId, 1, 1, productoId, 1, cantidad, precioUnidad, precioTotal)


def mercados(mercadoId=None, precioUnidad=None, precioTotal=None, opcion=None, nombreProducto=None,
             numeroFactura=None, descCompra=None):
    return MercadosController(mercadoId, 1, descCompra, 1, numeroFactura, 1, nombreProducto, 1,
                              '3 kg', precioUnidad, precioTotal, opcion)


def cargar_una_compra():
    registrar_datos_base()
    assert mercado_temp().insertarMercadosTempController()[0] == 1
    assert mercado_temp(productoId=2, cantidad='1', precioUnidad='1200', precioTotal='1200').insertarMercadosTempController()[0] == 1
    assert fnCargarCompraController()[0] == 1


# --- Registro y búsqueda con apóstrofes ---

def test_registro_y_busqueda_con_apostrofes(bd):
    registrar_datos_base()

    assert ProductosController(None, "d'on").consultarProductos() == ([(1, "D'Onofrio")], [1])
    assert ComerciosController(None, "d'l", None).consultarComerciosController()[0] == [(1, "Tienda D'Luis", 'Calle 5 #3-2')]
    assert FacturaController(None, "FE'", None, None).consultarFacturasController()[0] == [(1, "FE'001", 12500.0, '2026/10/15')]
    assert ComprasController(None, "'quin", None).consultarCompra()[0] == [(1, "Mercado 'Quincena'", '2026/10/15')]


def test_busqueda_con_comodin_no_rompe(bd):
    registrar_datos_base()
    assert ProductosController(None, '%').consultarProductos()[1] == [1]


def test_modificar_registros(bd, consultar):
    registrar_datos_base()

    assert ProductosController(1, "pan d'bono").editarProductos()[0] == 1
    assert ComerciosController(1, 'Otro', 'Calle 1').modificarComerciosController()[0] == 1
    assert FacturaController(1, 'fe002', '9900', '2026/10/16').modificarFacturas()[0] == 1
    assert ComprasController(1, 'mercado mes', None).modificarCompra()[0] == 1

    assert consultar("SELECT nombreProducto FROM productos WHERE productoId=1") == [("Pan D'Bono",)]
    assert consultar("SELECT * FROM facturas") == [(1, 'FE002', 9900.0, '2026/10/16')]
    assert consultar("SELECT describcion FROM compras") == [('Mercado Mes',)]


# --- Flujo de compra: mercadosTemp -> mercados ---

def test_mercado_temporal_agregar_modificar_eliminar(bd, consultar):
    registrar_datos_base()
    mercado_temp().insertarMercadosTempController()
    mercado_temp(productoId=2).insertarMercadosTempController()

    assert mercado_temp(2, productoId=2, cantidad='1 lb', precioUnidad='1300', precioTotal='1300').actualizarProductosController()[0] == 1
    assert MercadoTempController(2, *[None] * 7).consultarKeysMercadosTempController() == ([(1, 1, 2, 1)], [1, ''])
    assert MercadoTempController(1, *[None] * 7).eliminarProductosTempController() == [1]

    assert consultar("SELECT mercadoIdTemp, cantidadTemp, precioUnidadTemp FROM mercadosTemp") == [(2, '1 lb', 1300.0)]


def test_cargar_compra_pasa_temporal_a_mercados(bd, consultar):
    cargar_una_compra()

    assert consultar("SELECT COUNT(*) FROM mercadosTemp") == [(0,)]
    assert consultar("SELECT COUNT(*) FROM mercados") == [(2,)]
    mensaje, filas = mercados().consultarUltimosMercadosController()
    assert mensaje == [1]
    assert filas[0] == (2, 'Arroz', '1', 1200.0, 1200.0, "FE'001", '2026/10/15', "Tienda D'Luis", "Mercado 'Quincena'")


def test_cargar_compra_reinicia_ids_temporales(bd, consultar):
    cargar_una_compra()
    mercado_temp().insertarMercadosTempController()
    assert consultar("SELECT mercadoIdTemp FROM mercadosTemp") == [(1,)]


def test_tipos_guardados_en_mercados(bd, consultar):
    cargar_una_compra()
    assert consultar("SELECT typeof(compraId), typeof(productoId), typeof(cantidad), "
                     "typeof(precioUnidad), typeof(precioTotal) FROM mercados LIMIT 1") == [
        ('integer', 'integer', 'text', 'real', 'real')]


def test_consultar_mercados_por_opcion(bd):
    cargar_una_compra()
    assert len(mercados(opcion=OPCION_PRODUCTO, nombreProducto="d'on").consultarMercadosController()[1]) == 1
    assert len(mercados(opcion=OPCION_FACTURA, numeroFactura="fe'").consultarMercadosController()[1]) == 2
    assert len(mercados(opcion=OPCION_COMPRA, descCompra="'quin").consultarMercadosController()[1]) == 2


def test_consultar_mercados_sin_opcion(bd):
    assert mercados().consultarMercadosController() == ([0, 'Por favor seleccione una opción'], [])


def test_actualizar_y_eliminar_mercado(bd, consultar):
    cargar_una_compra()

    assert mercados(1, '3600', '10800').actualizarProductosController() == [1, '']
    assert consultar("SELECT cantidad, precioUnidad, precioTotal FROM mercados WHERE mercadoId=1") == [('3 kg', 3600.0, 10800.0)]

    assert mercados(1).eliminarProductosController() == [1, 'Fue eliminado el producto']
    assert consultar("SELECT COUNT(*) FROM mercados WHERE mercadoId=1") == [(0,)]


def test_actualizar_mercado_rechaza_precios_invalidos(bd, consultar):
    cargar_una_compra()

    assert mercados(1, 'abc', '10800').actualizarProductosController()[0] == 0
    assert mercados(1, '3600', '').actualizarProductosController()[0] == 0
    assert consultar("SELECT precioUnidad, precioTotal FROM mercados WHERE mercadoId=1") == [(3500.0, 7000.0)]


# --- Errores de base de datos llegan como mensaje ---

def test_campos_vacios(bd):
    assert ProductosController(None, '   ').insertarProducto() == [0, 'No se admiten campos vacíos']
    assert ComprasController(None, '', None).insertarCompras()[0] == 0
    assert FacturaController(None, 'A1', '12abc', '2026/10/15').insertarFacturas()[0] == 2


def test_error_de_bd_se_devuelve_como_mensaje(bd, consultar):
    consultar("DROP TABLE productos")
    consultar("DROP TABLE mercados")

    assert ProductosController(None, 'Arroz').insertarProducto() == [0, 'No se insertó el producto: no such table: productos']
    assert mercados(1).eliminarProductosController() == [0, 'No es posible eliminar el producto: no such table: mercados']
