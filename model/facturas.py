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
            sql = """INSERT INTO facturas VALUES (NULL, ?, ?, ?)
                """
            conexion.cursor.execute(sql, (self.numeroFactura
                                          ,self.valorTotalFactura
                                          ,self.fechaFactura)) #Se ejecuta la consulta
            facturaId = conexion.cursor.lastrowid #id de la factura creada
            conexion.desconectar()  #Se cierra la conexión
            return facturaId

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

         sql = """ SELECT * FROM facturas WHERE numeroFactura LIKE ? """

         conexion.cursor.execute(sql, (f'%{self.numeroFactura}%',))

         listaConsultaFacturas = conexion.cursor.fetchall()

         conexion.desconectar()

         return listaConsultaFacturas
    
    def modificarFacturas(self):
         
         conexion = con()#Conectamos con la base de datos

         sql = """ UPDATE facturas
                    SET numeroFactura = ?
                        ,valorTotalFactura = ?
                        ,fechaFactura = ?
                    WHERE facturaId = ?
                """

         conexion.cursor.execute(sql, (self.numeroFactura
                                       ,self.valorTotalFactura
                                       ,self.fechaFactura
                                       ,self.facturaId))

         conexion.desconectar()

         


