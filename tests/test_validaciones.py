import pytest

from controller.validaciones import esNumero
from controller.facturasController import FacturaController
from controller.mercadoTempController import MercadoTempController


@pytest.mark.parametrize('texto', ['12500', '12.5', '-3', ' 7 ', '0'])
def test_es_numero_acepta_numeros(texto):
    assert esNumero(texto)


@pytest.mark.parametrize('texto', ['', '   ', 'abc', '12abc', '12,5', None])
def test_es_numero_rechaza_lo_demas(texto):
    assert not esNumero(texto)


@pytest.mark.parametrize('numero, valor, fecha, esperado', [
    ('A1', '12500', '2026/10/15', 1),
    ('', '12500', '2026/10/15', 0),
    ('A1', '   ', '2026/10/15', 0),
    ('A1', '12500', '', 0),
    ('A1', '12abc', '2026/10/15', 2),
])
def test_validar_campos_facturas(numero, valor, fecha, esperado):
    factura = FacturaController(None, numero, valor, fecha)
    assert factura.validarCamposFacturas(numero, valor, fecha) == esperado


def mercado_temp(precioUnidad, precioTotal, compraId=1):
    return MercadoTempController(None, compraId, 1, 1, 1, '1', precioUnidad, precioTotal)


@pytest.mark.parametrize('precioUnidad, precioTotal, compraId, esperado', [
    ('3500', '7000', 1, 1),
    ('3500', '7000', None, 0),
    ('12abc', '7000', 1, 2),
    ('', '7000', 1, 2),
    ('3500', '   ', 1, 3),
])
def test_validacion_campos_mercado_temporal(precioUnidad, precioTotal, compraId, esperado):
    assert mercado_temp(precioUnidad, precioTotal, compraId).validacionCamposMercadosController() == esperado
