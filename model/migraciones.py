"""Migraciones del esquema de BillMate.db.

La versión del esquema se guarda en PRAGMA user_version. CreacionBbBillMate
(model/crearTablasBd.py) crea la versión 0; cada función de MIGRACIONES lleva
la base a la versión siguiente. Para cambiar el esquema se agrega una función
al final de la lista; nunca se edita una migración ya publicada.
"""
import sqlite3


def migracion1(conexion):
    #Claves foráneas reales en mercados y mercadosTemp, elimina la tabla estado
    #y corrige la errata compras.describcion -> descripcion

    #Filas cuyas referencias no existen (p. ej. las guardadas con 'None' por un bug viejo).
    #No se ven en la app porque los INNER JOIN las descartan, y bloquearían las claves foráneas
    referencias = [('compraId', 'compras', 'idCompra')
                   ,('facturaId', 'facturas', 'facturaId')
                   ,('productoId', 'productos', 'productoId')
                   ,('comercioId', 'comercios', 'comercioId')]
    for tabla, sufijo in (('mercados', ''), ('mercadosTemp', 'Temp')):
        condicion = ' OR '.join(f'{columna}{sufijo} IS NULL OR {columna}{sufijo} NOT IN (SELECT {llave} FROM {padre})'
                                for columna, padre, llave in referencias)
        conexion.execute(f'DELETE FROM {tabla} WHERE {condicion}')

    #SQLite no permite agregar claves foráneas a una tabla existente: se reconstruye.
    #Se conserva el orden de columnas porque cargarCompraModel usa INSERT ... SELECT posicional
    for tabla, sufijo in (('mercados', ''), ('mercadosTemp', 'Temp')):
        conexion.execute(f'''CREATE TABLE {tabla}_nueva(
                                mercadoId{sufijo} INTEGER PRIMARY KEY AUTOINCREMENT
                                ,compraId{sufijo} INTEGER REFERENCES compras(idCompra)
                                ,facturaId{sufijo} INTEGER REFERENCES facturas(facturaId)
                                ,productoId{sufijo} INTEGER REFERENCES productos(productoId)
                                ,comercioId{sufijo} INTEGER REFERENCES comercios(comercioId)
                                ,cantidad{sufijo} TEXT
                                ,precioUnidad{sufijo} REAL
                                ,precioTotal{sufijo} REAL
                                )''')
        conexion.execute(f'INSERT INTO {tabla}_nueva SELECT * FROM {tabla}')
        conexion.execute(f'DROP TABLE {tabla}')
        conexion.execute(f'ALTER TABLE {tabla}_nueva RENAME TO {tabla}')

    conexion.execute('DROP TABLE estado')
    conexion.execute('ALTER TABLE compras RENAME COLUMN describcion TO descripcion')


MIGRACIONES = [migracion1]


def versionEsquema(conexion):
    return conexion.execute('PRAGMA user_version').fetchone()[0]


def aplicarMigraciones(ruta, respaldar):
    """Aplica las migraciones pendientes a la base en `ruta`.

    Si `respaldar` es verdadero y hay migraciones pendientes, antes se copia la base
    a BillMate.db.respaldo-v<versión> en la misma carpeta. Cada migración corre en
    su propia transacción: si falla, se revierte y se relanza la excepción.
    """
    conexion = sqlite3.connect(ruta, isolation_level=None)
    try:
        version = versionEsquema(conexion)
        if version >= len(MIGRACIONES):
            return

        if respaldar:
            respaldo = sqlite3.connect(f'{ruta}.respaldo-v{version}')
            conexion.backup(respaldo)
            respaldo.close()

        #Procedimiento recomendado por SQLite para reconstruir tablas: claves desactivadas
        #durante la migración y verificación con foreign_key_check antes de confirmar
        conexion.execute('PRAGMA foreign_keys = OFF')
        for numero in range(version + 1, len(MIGRACIONES) + 1):
            conexion.execute('BEGIN')
            try:
                MIGRACIONES[numero - 1](conexion)
                if conexion.execute('PRAGMA foreign_key_check').fetchall():
                    raise sqlite3.IntegrityError(f'La migración {numero} dejó referencias inválidas')
                conexion.execute(f'PRAGMA user_version = {numero}')
                conexion.execute('COMMIT')
            except Exception:
                conexion.execute('ROLLBACK')
                raise
    finally:
        conexion.close()
