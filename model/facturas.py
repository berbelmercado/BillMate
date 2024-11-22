#importamos la clase de conexión 
from model.conexionDb import ConexionDb as con

#Modelo Facturas
class Facturas:
    #Constructor
    def __init__(self
                 ,facturaId
                 ,numeroFactura
                 ,valorTotalFactura
                 ,fechaFactura):
        self.facturaId = facturaId
        self.numeroFactura = numeroFactura
        self.valorTotalFactura = valorTotalFactura
        self.fechaFactura = fechaFactura

    def insertarFacturas(self):
            #Se inserta la información que envía el controlador
            #se conecta a la base de datos
            conexion=con()
             #Se crea sentencia sql
            sql = f"""INSERT INTO facturas VALUES ({'NULL'}
                                                    ,'{self.numeroFactura}'
                                                    ,'{self.valorTotalFactura}'
                                                    ,'{self.fechaFactura}'
                                                    )
                """
            conexion.cursor.execute(sql) #Se ejecuta la consulta
            conexion.desconectar()  #Se cierra la conexión

    def consultarListaFacturas(self):
        #Creamos conexión
        conexion=con()

        listaFacturas = [] #Declaración de variable

        sql = f""" SELECT * FROM facturas """ #Sentencia SQL

        conexion.cursor.execute(sql) #Ejecutamos la sentencia SQL

        listaFacturas = conexion.cursor.fetchall() #Recuperamos la información

        conexion.desconectar()

        return listaFacturas
    
    def consultarFacturasModel(self):
         conexion = con()#Conectamos con la base de datos

         listaConsultaFacturas = []

         sql = f""" SELECT * FROM facturas WHERE numeroFactura LIKE'%{self.numeroFactura}%' """

         conexion.cursor.execute(sql)

         listaConsultaFacturas = conexion.cursor.fetchall()

         conexion.desconectar()

         return listaConsultaFacturas
    
    def modificarFacturas(self):
         
         conexion = con()#Conectamos con la base de datos

         sql = f""" UPDATE facturas
                    SET numeroFactura = '{self.numeroFactura}'
                        ,valorTotalFactura = '{self.valorTotalFactura}'
                        ,fechaFactura = '{self.fechaFactura}'
                    WHERE facturaId = {self.facturaId}
                """

         conexion.cursor.execute(sql)

         conexion.desconectar()

         


