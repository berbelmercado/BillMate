from model.conexionDb import ConexionDb as conn


# Modelo Comercios
class Comercios:
    # Constructor
    def __init__(self, comercioId, nombreComercio, direccionComercio):

        self.comercioId = comercioId
        self.nombreComercio = nombreComercio
        self.direccionComercio = direccionComercio

    def insertarComercios(self):
        # Se inserta la información que envía el controlador
        conexion = conn()  # Conexión a la base de datos

        # Sentencia SQL
        sql = """ INSERT INTO comercios VALUES (NULL, ?, ?)
              """
        conexion.cursor.execute(sql, (self.nombreComercio, self.direccionComercio))  # Se ejecuta la consulta

        conexion.desconectar()  # Cerramos conexión

    def consultarComercios(self):
        # Se consultan todos los comercios registrados

        listaComercio = []

        conexion = conn()  # Conexión a la base de datos

        sql = f""" SELECT * FROM comercios """  # Sentencia SQL

        conexion.cursor.execute(sql)
        listaComercio = conexion.cursor.fetchall()

        return listaComercio

    def consultarComercioModel(self):

        conexion = conn()  # Conexión a la base de datos

        listaComercios = []

        sql = """ SELECT * FROM comercios WHERE nombreComercio LIKE ? """

        conexion.cursor.execute(sql, (f'%{self.nombreComercio}%',))  # Ejecutamos consulta SQL
        listaComercios = conexion.cursor.fetchall()  # Recuperamos los datos
        conexion.desconectar()

        return listaComercios

    def modificarComerciosModel(self):
        # Método para modificar comercios
        conexion = conn()

        sql = """  UPDATE comercios
                    SET nombreComercio = ?
                       ,direccionComercio = ?
                    WHERE  comercioId = ?
                """
        conexion.cursor.execute(sql, (self.nombreComercio, self.direccionComercio, self.comercioId))
        conexion.desconectar()
