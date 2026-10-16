import pytest

from controller.validaciones import esNumero, convertirNumero, formatearNumero, formatearMoneda, cantidadNumerica
from controller import facturasController
from controller import mercadoTempController


@pytest.mark.parametrize('texto, esperado', [
    ('12500', 12500),
    ('12.500', 12500),
    ('1.250.000', 1250000),
    ('564,6', 564.6),
    ('12.500,50', 12500.5),
    ('1.500', 1500),         #punto con grupo de 3 dígitos: miles, no 1.5
    ('12.5', 12.5),          #punto que no agrupa de a 3: decimal, como antes
    ('25000.0', 25000),
    (' 7 ', 7),
    ('-3', -3),
    ('0', 0),
])
def test_convertir_numero(texto, esperado):
    assert convertirNumero(texto) == esperado
    assert esNumero(texto)


@pytest.mark.parametrize('texto', ['', '   ', 'abc', '12abc', '12,500.00', '1.2.3', '12.50.0', '1,2,3', '.5', None])
def test_es_numero_rechaza_lo_demas(texto):
    assert convertirNumero(texto) is None
    assert not esNumero(texto)


@pytest.mark.parametrize('valor, texto', [(37500.0, '37500'), (190.125, '190,12'), (1693.8000000000002, '1693,80')])
def test_formatear_numero_se_vuelve_a_leer_igual(valor, texto):
    assert formatearNumero(valor) == texto
    assert convertirNumero(texto) == round(valor, 2)


@pytest.mark.parametrize('valor, texto', [
    (12500, '$ 12.500'),
    (12500.5, '$ 12.500,50'),
    (1250000.0, '$ 1.250.000'),
    (0, '$ 0'),
    (999.999, '$ 1.000'),
    (-3400, '-$ 3.400'),
])
def test_formatear_moneda(valor, texto):
    assert formatearMoneda(valor) == texto


@pytest.mark.parametrize('texto, esperado', [
    ('2', 2),
    ('0.8k', 0.8),
    ('1.558k', 1.558),       #en cantidades el punto es decimal, no separador de miles
    ('1,5 kg', 1.5),
    (' 3 und', 3),
    ('media', None),
    ('', None),
    (None, None),
])
def test_cantidad_numerica(texto, esperado):
    assert cantidadNumerica(texto) == esperado


@pytest.mark.parametrize('numero, valor, fecha, esperado', [
    ('A1', '12500', '2026-10-15', 1),
    ('', '12500', '2026-10-15', 0),
    ('A1', '   ', '2026-10-15', 0),
    ('A1', '12500', '', 0),
    ('A1', '12abc', '2026-10-15', 2),
])
def test_validar_campos_facturas(numero, valor, fecha, esperado):
    assert facturasController.validarCamposFactura(numero, valor, fecha) == esperado


@pytest.mark.parametrize('precioUnidad, precioTotal, compraId, productoId, esperado', [
    ('3500', '7000', 1, 1, 1),
    ('3500', '7000', None, 1, 0),
    ('3500', '7000', 1, None, 0),
    ('12abc', '7000', 1, 1, 2),
    ('', '7000', 1, 1, 2),
    ('3500', '   ', 1, 1, 3),
])
def test_validacion_campos_mercado_temporal(precioUnidad, precioTotal, compraId, productoId, esperado):
    assert mercadoTempController.validarCamposMercadoTemp(compraId, 1, productoId, 1, precioUnidad, precioTotal) == esperado
