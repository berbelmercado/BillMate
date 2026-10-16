#Validaciones compartidas por los controladores
import re

#Formato colombiano: punto como separador de miles y coma decimal (1.250.000,50)
_MILES_CON_PUNTO = re.compile(r'-?\d{1,3}(\.\d{3})+(,\d+)?')
_COMA_DECIMAL = re.compile(r'-?\d+(,\d+)?')
#Punto decimal, como se escribía antes (12.5) o como lo deja el cálculo del total (25000.0)
_PUNTO_DECIMAL = re.compile(r'-?\d+(\.\d+)?')


def convertirNumero(texto):
    """Convierte un precio escrito por el usuario a float, o devuelve None si no es válido.

    12500 -> 12500, 12.500 -> 12500, 1.250.000 -> 1250000, 564,6 -> 564.6,
    12.500,50 -> 12500.5. Un punto que no separa grupos de 3 dígitos se toma como
    decimal (12.5 -> 12.5); por eso 1.500 es 1500 y no 1.5.
    """
    if not isinstance(texto, str):
        return None
    texto = texto.strip()

    if _MILES_CON_PUNTO.fullmatch(texto):
        return float(texto.replace('.', '').replace(',', '.'))
    if _COMA_DECIMAL.fullmatch(texto):
        return float(texto.replace(',', '.'))
    if _PUNTO_DECIMAL.fullmatch(texto):
        return float(texto)
    return None


def formatearNumero(valor):
    #Texto que convertirNumero vuelve a leer igual: 37500.0 -> '37500', 190.125 -> '190,13'
    if valor == int(valor):
        return str(int(valor))
    return f'{valor:.2f}'.replace('.', ',')


def formatearMoneda(valor):
    #Valor para mostrar en pantalla: 12500 -> '$ 12.500', 12500.5 -> '$ 12.500,50', -3400 -> '-$ 3.400'
    signo = '-' if valor < 0 else ''
    texto = f'{abs(valor):,.2f}'.replace(',', ' ').replace('.', ',').replace(' ', '.')
    if texto.endswith(',00'):
        texto = texto[:-3]
    return f'{signo}$ {texto}'


#Número al inicio de la cantidad: '2', '0.8k', '1,5 kg'. Aquí el punto es decimal (1.558k = 1,558 kg)
_CANTIDAD = re.compile(r'\s*(\d+(?:[.,]\d+)?)')


def cantidadNumerica(texto):
    """Número con el que empieza la cantidad, para calcular el total; None si no empieza con un número.

    '2' -> 2, '0.8k' -> 0.8, '1.558k' -> 1.558, '1,5 kg' -> 1.5, 'media' -> None.
    No usa convertirNumero porque en las cantidades el punto es decimal, no separador de miles.
    """
    if not isinstance(texto, str):
        return None
    coincidencia = _CANTIDAD.match(texto)
    if coincidencia is None:
        return None
    return float(coincidencia.group(1).replace(',', '.'))


def esNumero(texto):
    #Devuelve True si el texto es un precio válido (vacío, espacios o letras no)
    return convertirNumero(texto) is not None
