from model.conexionDb import ConexionDb as conn


class Compras:
    def __init__(self, idCompra, describcionCompra, fechaCreacionCompra):

        self.idCompra = idCompra
        self.describcionCompra = describcionCompra
        self.fechaCreacionCompra = fechaCreacionCompra

    def insertarCompras(self):
        # abrimos la conexion
        conexion = conn()

        # sentencia SQL
        sql = """ INSERT INTO compras VALUES (NULL, ?, ?)
             """
        conexion.cursor.execute(sql, (self.describcionCompra, self.fechaCreacionCompra))  # Ejecutamos la sentencia

        conexion.desconectar()  # Cerramos conexion

    def buscarComprasRegistradas(self):
        # Función para buscar todas las compras registradas

        comprasRegistradas = []

        conexion = conn()  # Abrimos la conexión

        # Sentencia  SQL
        sql = f""" SELECT * FROM compras
              """

        conexion.cursor.execute(sql)  # Ejecutamos la consulta sql
        comprasRegistradas = conexion.cursor.fetchall()
        conexion.desconectar()  # Cerramos conexión

        return comprasRegistradas

    def consultarCompras(self):
        # Función para filtrar compras

        listadoCompras = []  # Inicializamos variable

        conexion = conn()  # Abrimos la conexión a la bd

        # Consulta SQL
        sql = """ SELECT * FROM compras WHERE descripcion LIKE ?
              """

        conexion.cursor.execute(sql, (f'%{self.describcionCompra}%',))
        listadoCompras = conexion.cursor.fetchall()

        conexion.desconectar()

        return listadoCompras

    def modificarCompras(self):
        # Fución para modificar las compras

        conexion = conn()  # Abrimos conexión

        sql = """ UPDATE compras
                   SET descripcion = ?
                   WHERE idCompra = ?
                   """
        conexion.cursor.execute(sql, (self.describcionCompra, self.idCompra))  # Ejecutamos consulta sql

        conexion.desconectar()  # Cerramos conexión
