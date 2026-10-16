from model.conexionDb import ConexionDb as con
from model.rutas import ruta_base_datos
import os

class CreacionBbBillMate:
        
        def __init__(self):
                self.crearTablaProductos()
                self.crearTablaFacturas()
                self.crearTablaComercios()
                self.crearTablaMercadosTemp()
                self.crearTablaMercados()
                self.crearTablaEstado()
                self.creaTablaCompras()
                self.iniciaTablaEstadoBD()



        #clase para crear tablas si la base de datos no existe
        def crearTablaProductos(self):
                conexion = con()

                #Creamos tabla productos
                sql = ''' CREATE TABLE productos(
                                        productoId INTEGER, 
                                        nombreProducto VARCHAR(90),
                                        PRIMARY KEY (productoId)
                                        )
                '''
                conexion.cursor.execute(sql) #ejecutamos la consulta sql
                conexion.desconectar() #cerramos la conexión (ejecutando commit dentro de la función desconectar)

        def crearTablaFacturas(self):
                conexion = con()

                sql = '''CREATE TABLE facturas(facturaId INTEGER PRIMARY KEY AUTOINCREMENT,
                                            numeroFactura VARCHAR(90),
                                            valorTotalFactura float,
                                            fechaFactura TEXT)
                '''
                conexion.cursor.execute(sql)
                conexion.desconectar()

        def crearTablaComercios(self):

                conexion= con()

                sql = '''CREATE TABLE comercios(comercioId INTEGER PRIMARY KEY AUTOINCREMENT,
                                        nombreComercio VARCHAR(100),
                                        direccionComercio VARCHAR(100)
                                        )
                '''
                conexion.cursor.execute(sql)
                conexion.desconectar()

        def crearTablaMercados(self):

                conexion= con()

                sql = '''CREATE TABLE mercados(mercadoId INTEGER PRIMARY KEY AUTOINCREMENT,
                                        compraId INTERGER FOREING KEY,
                                        facturaId INTEGER FOREING KEY,
                                        productoId INTEGER FOREING KEY,
                                        comercioId INTEGER FOREING KEY,
                                        cantidad VARCHAR(30),
                                        precioUnidad REAL,
                                        precioTotal  REAL
                                        )
                       '''
                conexion.cursor.execute(sql)
                conexion.desconectar()

        def crearTablaMercadosTemp(self):

                conexion= con()

                sql = '''CREATE TABLE mercadosTemp(mercadoIdTemp INTEGER PRIMARY KEY AUTOINCREMENT,
                                        compraIdTemp INTERGER FOREING KEY,
                                        facturaIdTemp INTEGER FOREING KEY,
                                        productoIdTemp INTEGER FOREING KEY,
                                        comercioIdTemp INTEGER FOREING KEY,
                                        cantidadTemp VARCHAR(30),
                                        precioUnidadTemp REAL,
                                        precioTotalTemp  REAL
                                        )
                       '''
                conexion.cursor.execute(sql)
                conexion.desconectar()

        def crearTablaEstado(self):

                conexion=con()

                sql = '''CREATE TABLE estado(estado INTEGER COLLATE BINARY)
                      '''
                conexion.cursor.execute(sql)
                conexion.desconectar()

        def iniciaTablaEstadoBD(self):

                conexion = con()

                sql= f""" INSERT INTO estado VALUES(1) """

                conexion.cursor.execute(sql)
                conexion.desconectar()

        def creaTablaCompras(self):

                conexion  = con() #Creamos conexion

                sql = f""" CREATE TABLE compras (idCompra INTEGER PRIMARY KEY AUTOINCREMENT
                                                ,describcion VARCHAR(100)
                                                ,fechaCreacion TEXT)  
                        """
                
                conexion.cursor.execute(sql)

                conexion.desconectar()

def  existeBd():
        """Asegura que la base de datos exista."""
        if not os.path.exists(ruta_base_datos()):
                estado=0
        else:
                estado=1  
        return estado
