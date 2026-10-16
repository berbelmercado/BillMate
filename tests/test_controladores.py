"""Pruebas de controladores y modelos contra una base SQLite temporal."""
from controller import productosController
from controller import comerciosController
from controller import facturasController
from controller import comprasController
from controller import mercadoTempController
from controller import mercadosController
from controller.mercadosController import OPCION_PRODUCTO, OPCION_FACTURA, OPCION_COMPRA


def registrar_datos_base():
    #Producto, comercio, factura y compra con apóstrofes (id 1 en cada tabla)
    assert productosController.insertarProducto("D'onofrio")[0] == 1
    assert productosController.insertarProducto('Arroz')[0] == 1
    assert comerciosController.insertarComercio("Tienda D'Luis", 'Calle 5 #3-2')[0] == 1
    assert facturasController.insertarFactura("fe'001", '12500', '2026-10-15')[0] == 1
    assert comprasController.insertarCompra("Mercado 'quincena'", '2026-10-15')[0] == 1


def agregar_temp(productoId=1, cantidad='2 kg', precioUnidad='3500', precioTotal='7000'):
    #Agrega un ítem a la compra en curso con compra, factura y comercio 1
    return mercadoTempController.insertarMercadoTemp(1, 1, productoId, 1, cantidad, precioUnidad, precioTotal)


def actualizar_mercado(mercadoId, precioUnidad, precioTotal):
    return mercadosController.actualizarMercado(mercadoId, 1, 1, 1, 1, '3 kg', precioUnidad, precioTotal)


def cargar_una_compra():
    registrar_datos_base()
    assert agregar_temp()[0] == 1
    assert agregar_temp(productoId=2, cantidad='1', precioUnidad='1200', precioTotal='1200')[0] == 1
    assert mercadoTempController.cargarCompra()[0] == 1


# --- Registro y búsqueda con apóstrofes ---

def test_registro_y_busqueda_con_apostrofes(bd):
    registrar_datos_base()

    assert productosController.consultarProductos("d'on") == ([(1, "D'Onofrio")], [1])
    assert comerciosController.consultarComercios("d'l")[0] == [(1, "Tienda D'Luis", 'Calle 5 #3-2')]
    assert facturasController.consultarFacturas("FE'")[0] == [(1, "FE'001", 12500.0, '2026-10-15')]
    assert comprasController.consultarCompras("'quin")[0] == [(1, "Mercado 'Quincena'", '2026-10-15')]


def test_busqueda_con_comodin_no_rompe(bd):
    registrar_datos_base()
    assert productosController.consultarProductos('%')[1] == [1]


def test_modificar_registros(bd, consultar):
    registrar_datos_base()

    assert productosController.editarProducto(1, "pan d'bono")[0] == 1
    assert comerciosController.modificarComercio(1, 'Otro', 'Calle 1')[0] == 1
    assert facturasController.modificarFactura(1, 'fe002', '9900', '2026-10-16')[0] == 1
    assert comprasController.modificarCompra(1, 'mercado mes')[0] == 1

    assert consultar("SELECT nombreProducto FROM productos WHERE productoId=1") == [("Pan D'Bono",)]
    assert consultar("SELECT * FROM facturas") == [(1, 'FE002', 9900.0, '2026-10-16')]
    assert consultar("SELECT descripcion FROM compras") == [('Mercado Mes',)]


# --- Flujo de compra: mercadosTemp -> mercados ---

def test_mercado_temporal_agregar_modificar_eliminar(bd, consultar):
    registrar_datos_base()
    agregar_temp()
    agregar_temp(productoId=2)

    assert mercadoTempController.actualizarMercadoTemp(2, 1, 1, 2, 1, '1 lb', '1.300', '1300')[0] == 1
    assert mercadoTempController.consultarLlavesMercadoTemp(2) == ([(1, 1, 2, 1)], [1, ''])
    assert mercadoTempController.eliminarMercadoTemp(1) == [1]

    assert consultar("SELECT mercadoIdTemp, cantidadTemp, precioUnidadTemp FROM mercadosTemp") == [(2, '1 lb', 1300.0)]


def test_mercado_temporal_valida_producto_y_precios(bd, consultar):
    registrar_datos_base()
    assert agregar_temp(productoId=None) == [0, 'No se permiten campos vacíos']
    assert agregar_temp()[0] == 1

    assert mercadoTempController.actualizarMercadoTemp(1, 1, 1, 1, 1, '2 kg', 'abc', '7000') == [0, 'El campo "Precio unidad" no es válido']
    assert consultar("SELECT COUNT(*), MAX(precioUnidadTemp) FROM mercadosTemp") == [(1, 3500.0)]


def test_cargar_compra_pasa_temporal_a_mercados(bd, consultar):
    cargar_una_compra()

    assert consultar("SELECT COUNT(*) FROM mercadosTemp") == [(0,)]
    assert consultar("SELECT COUNT(*) FROM mercados") == [(2,)]
    filas, mensaje = mercadosController.consultarUltimoMercado()
    assert mensaje == [1]
    assert filas[0] == (2, 'Arroz', '1', 1200.0, 1200.0, "FE'001", '2026-10-15', "Tienda D'Luis", "Mercado 'Quincena'")


def test_cargar_compra_reinicia_ids_temporales(bd, consultar):
    cargar_una_compra()
    agregar_temp()
    assert consultar("SELECT mercadoIdTemp FROM mercadosTemp") == [(1,)]


def test_tipos_guardados_en_mercados(bd, consultar):
    cargar_una_compra()
    assert consultar("SELECT typeof(compraId), typeof(productoId), typeof(cantidad), "
                     "typeof(precioUnidad), typeof(precioTotal) FROM mercados LIMIT 1") == [
        ('integer', 'integer', 'text', 'real', 'real')]


def test_consultar_mercados_por_opcion(bd):
    cargar_una_compra()
    assert len(mercadosController.consultarMercados(OPCION_PRODUCTO, "d'on")[0]) == 1
    assert len(mercadosController.consultarMercados(OPCION_FACTURA, "fe'")[0]) == 2
    assert len(mercadosController.consultarMercados(OPCION_COMPRA, "'quin")[0]) == 2


def test_consultar_mercados_sin_opcion(bd):
    assert mercadosController.consultarMercados(None, 'arroz') == ([], [0, 'Por favor seleccione una opción'])
    assert mercadosController.consultarMercados(10, 'arroz') == ([], [0, 'Por favor seleccione una opción'])


def test_actualizar_y_eliminar_mercado(bd, consultar):
    cargar_una_compra()

    assert actualizar_mercado(1, '3600', '10800') == [1, '']
    assert consultar("SELECT cantidad, precioUnidad, precioTotal FROM mercados WHERE mercadoId=1") == [('3 kg', 3600.0, 10800.0)]

    assert mercadosController.eliminarMercado(1) == [1, 'Fue eliminado el producto']
    assert consultar("SELECT COUNT(*) FROM mercados WHERE mercadoId=1") == [(0,)]


def test_actualizar_mercado_rechaza_precios_invalidos(bd, consultar):
    cargar_una_compra()

    assert actualizar_mercado(1, 'abc', '10800')[0] == 0
    assert actualizar_mercado(1, '3600', '')[0] == 0
    assert consultar("SELECT precioUnidad, precioTotal FROM mercados WHERE mercadoId=1") == [(3500.0, 7000.0)]


# --- Precios con formato colombiano (12.500 = doce mil quinientos) ---

def test_precios_con_separador_de_miles_se_guardan_bien(bd, consultar):
    registrar_datos_base()
    assert facturasController.insertarFactura('fe002', '1.250.000', '2026-10-16')[0] == 1
    assert agregar_temp(precioUnidad='12.500', precioTotal='25.000')[0] == 1
    assert mercadoTempController.cargarCompra()[0] == 1
    assert actualizar_mercado(1, '13.500,50', '27.001') == [1, '']

    assert consultar("SELECT valorTotalFactura FROM facturas WHERE numeroFactura='FE002'") == [(1250000.0,)]
    assert consultar("SELECT precioUnidad, precioTotal FROM mercados WHERE mercadoId=1") == [(13500.5, 27001.0)]


# --- Errores de base de datos llegan como mensaje ---

def test_campos_vacios(bd):
    assert productosController.insertarProducto('   ') == [0, 'No se admiten campos vacíos']
    assert comprasController.insertarCompra('', None)[0] == 0
    assert comprasController.modificarCompra(1, '   ') == [0, 'No se permite enviar la descripción en blanco']
    assert facturasController.insertarFactura('A1', '12abc', '2026-10-15')[0] == 2
    assert comerciosController.insertarComercio(' ', 'Calle 1') == [0, 'No se admiten campos vacíos']
    assert comerciosController.modificarComercio(1, 'Otro', '') == [0, 'No se admiten campos vacíos']


def test_productos_repetidos_no_se_admiten(bd, consultar):
    registrar_datos_base()

    assert productosController.insertarProducto('  arroz ') == [0, 'Ya existe un producto llamado "Arroz"']
    assert productosController.editarProducto(2, "d'onofrio") == [0, 'Ya existe un producto llamado "D\'Onofrio"']
    assert productosController.editarProducto(2, 'arroz')[0] == 1
    assert consultar("SELECT COUNT(*) FROM productos") == [(2,)]


def test_insertar_devuelve_el_id_creado(bd):
    assert productosController.insertarProducto('Arroz') == [1, 'Se insertó el producto correctamente', 1]
    assert productosController.insertarProducto('Leche')[2] == 2
    assert comerciosController.insertarComercio('Exito', 'Calle 1')[2] == 1
    assert facturasController.insertarFactura('fe1', '100', '2026-10-16')[2] == 1
    assert comprasController.insertarCompra('Quincena', '2026-10-16')[2] == 1


def test_cuadre_por_factura(bd):
    registrar_datos_base()  #factura 1 por 12.500
    assert facturasController.insertarFactura('fe2', '5.000', '2026-10-16')[0] == 1
    assert agregar_temp()[0] == 1  #7.000
    assert agregar_temp(productoId=2, cantidad='1', precioUnidad='1200', precioTotal='1200')[0] == 1
    assert mercadoTempController.insertarMercadoTemp(1, 2, 1, 1, '1', '5000', '5000')[0] == 1

    assert mercadoTempController.cuadreFacturas() == ([(1, "FE'001", 8200.0, 12500.0, 4300.0)
                                                       ,(2, 'FE2', 5000.0, 5000.0, 0.0)], [1, ''])


def test_cuadre_sin_items(bd):
    assert mercadoTempController.cuadreFacturas() == ([], [1, ''])


def test_listados_completos(bd):
    registrar_datos_base()

    assert comerciosController.consultarListaComercios() == ([(1, "Tienda D'Luis", 'Calle 5 #3-2')], [1, ''])
    assert facturasController.consultarListaFacturas()[1] == [1, '']
    assert comprasController.consultarListaCompras()[1] == [1, '']


def test_listados_devuelven_error_de_bd(bd, consultar):
    consultar("DROP TABLE mercados")
    consultar("DROP TABLE comercios")
    consultar("DROP TABLE facturas")
    consultar("DROP TABLE compras")

    assert comerciosController.consultarListaComercios() == ([], [0, 'No se pudo consultar los comercios: no such table: comercios'])
    assert facturasController.consultarListaFacturas() == ([], [0, 'No se pudo obtener información de las facturas: no such table: facturas'])
    assert comprasController.consultarListaCompras() == ([], [0, 'Error al consultar compras registradas: no such table: compras'])


def test_error_de_bd_se_devuelve_como_mensaje(bd, consultar):
    consultar("DROP TABLE productos")
    consultar("DROP TABLE mercados")

    assert productosController.insertarProducto('Arroz') == [0, 'No se insertó el producto: no such table: productos']
    assert mercadosController.eliminarMercado(1) == [0,'No es posible eliminar el producto: no such table: mercados']
