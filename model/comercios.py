from model.conexionDb import ConexionDb as conn

#Modelo Comercios
class Comercios:
    #Constructor
    def __init__ (self
                  ,comercioId
                  ,nombreComercio
                  , direccionComercio):
        
        self.comercioId = comercioId
        self.nombreComercio = nombreComercio
        self.direccionComercio = direccionComercio

    def insertarComercios(self):
        #Se inserta la información que envía el controlador
        conexion = conn() #Conexión a la base de datos

        #Sentencia SQL
        sql = f""" INSERT INTO comercios VALUES ({'NULL'}
                                                ,'{self.nombreComercio}'
                                                ,'{self.direccionComercio}'
                                                )
              """ 
        conexion.cursor.execute(sql) #Se ejecuta la consulta

        conexion.desconectar()  #Cerramos conexión
    
    def consultarComercios(self):
        #Se consultan todos los comercios registrados

        listaComercio = []

        conexion = conn() #Conexión a la base de datos

        sql = f""" SELECT * FROM comercios """ #Sentencia SQL

        conexion.cursor.execute(sql)
        listaComercio = conexion.cursor.fetchall()

        return listaComercio
    
    def consultarComercioModel(self):
        
        conexion = conn()#Conexión a la base de datos

        listaComercios = []

        sql = f""" SELECT * FROM comercios WHERE nombreComercio LIKE'%{self.nombreComercio}%' """

        conexion.cursor.execute(sql) #Ejecutamos consulta SQL
        listaComercios = conexion.cursor.fetchall() #Recuperamos los datos
        conexion.desconectar()

        return listaComercios
    
    def modificarComerciosModel(self):
        #Método para modificar comercios
        conexion = conn()

        sql = f"""  UPDATE comercios
                    SET nombreComercio = '{self.nombreComercio}'
                       ,direccionComercio = '{self.direccionComercio}'
                    WHERE  comercioId = {self.comercioId}
                """
        conexion.cursor.execute(sql)
        conexion.desconectar()


