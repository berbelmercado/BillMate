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
        sql = f""" INSERT INTO compras VALUES ({'NULL'}
                                                ,'{self.describcionCompra}'
                                                ,'{self.fechaCreacionCompra}'
                                                )
             """
        conexion.cursor.execute(sql)  # Ejecutamos la sentencia

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
        sql = f""" SELECT * FROM compras WHERE describcion LIKE '%{self.describcionCompra}%'
              """

        conexion.cursor.execute(sql)
        listadoCompras = conexion.cursor.fetchall()

        conexion.desconectar()

        return listadoCompras

    def modificarCompras(self):
        # Fución para modificar las compras

        conexion = conn()  # Abrimos conexión

        sql = f""" UPDATE compras 
                   SET describcion = '{self.describcionCompra}'
                   WHERE idCompra = {self.idCompra}                
                   """
        conexion.cursor.execute(sql)  # Ejecutamos consulta sql

        conexion.desconectar()  # Cerramos conexión
