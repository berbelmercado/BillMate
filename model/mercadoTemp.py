from model.conexionDb import ConexionDb as conn

class MercadoTemp ():
    def __init__(self
                 ,mercadoIdTemp
                 ,compraIdTemp
                 ,facturaIdTemp
                 ,productoIdTemp
                 ,comercioIdTemp
                 ,cantidadTemp
                 ,precioUnidadTemp
                 ,precioTotalTemp):
        
        self.mercadoIdTemp = mercadoIdTemp
        self.compraIdTemp = compraIdTemp
        self.facturaIdTemp = facturaIdTemp
        self.productoIdTemp = productoIdTemp
        self.comercioIdTemp = comercioIdTemp
        self.cantidadTemp = cantidadTemp
        self.precioUnidadTemp = precioUnidadTemp
        self.precioTotalTemp = precioTotalTemp
        
    def insertarMercadoTempral(self) :

        conexion = conn()#Abrimos conexion

        sql = """  INSERT INTO mercadosTemp  VALUES(NULL, ?, ?, ?, ?, ?, ?, ?)
               """

        conexion.cursor.execute(sql, (self.compraIdTemp
                                      ,self.facturaIdTemp
                                      ,self.productoIdTemp
                                      ,self.comercioIdTemp
                                      ,self.cantidadTemp
                                      ,self.precioUnidadTemp
                                      ,self.precioTotalTemp))#Ejecutamos consulta

        conexion.desconectar()#Cerramos conexión
    
    def consultarMercadosTemporal(self):
        
        listaMercadoTemporal = []

        conexion = conn()

        sql = f"""  SELECT  mercadosTemp.mercadoIdTemp
                            ,productos.nombreProducto
                            ,mercadosTemp.cantidadTemp
                            ,mercadosTemp.precioUnidadTemp
                            ,mercadosTemp.precioTotalTemp
                            ,facturas.numeroFactura
                            ,comercios.nombreComercio
                            ,compras.descripcion
                    FROM mercadosTemp 
                            INNER JOIN productos
                                ON mercadosTemp.productoIdTemp = productos.productoId
                            INNER JOIN facturas 
                                ON mercadosTemp.facturaIdTemp = facturas.facturaId
                            INNER JOIN comercios
                                ON mercadosTemp.comercioIdTemp = comercios.comercioId
                            INNER JOIN compras
                                ON mercadosTemp.compraIdTemp = compras.idCompra
                    
                    ORDER BY mercadosTemp.mercadoIdTemp DESC
              """

        conexion.cursor.execute(sql)

        listaMercadoTemporal = conexion.cursor.fetchall()

        conexion.desconectar()

        return listaMercadoTemporal
    
    def actualizarProductoTemporal(self):
        conexion= conn()

        sql = """ UPDATE mercadosTemp
                   SET compraIdTemp = ?
                       ,facturaIdTemp = ?
                       ,productoIdTemp = ?
                       ,comercioIdTemp = ?
                       ,cantidadTemp = ?
                       ,precioUnidadTemp = ?
                       ,precioTotalTemp = ?
                    WHERE mercadoIdTemp = ?
               """
        conexion.cursor.execute(sql, (self.compraIdTemp
                                      ,self.facturaIdTemp
                                      ,self.productoIdTemp
                                      ,self.comercioIdTemp
                                      ,self.cantidadTemp
                                      ,self.precioUnidadTemp
                                      ,self.precioTotalTemp
                                      ,self.mercadoIdTemp))

        conexion.desconectar()

    def eliminarMercadoTemporal(self):
        
        conexion = conn()

        sql = """ DELETE FROM mercadosTemp WHERE mercadoIdTemp = ?
               """

        conexion.cursor.execute(sql, (self.mercadoIdTemp,))

        conexion.desconectar()

    def consultarKeysMercadosTempModel(self):
        #consultamos las llaves primaris desde la base de datos

        listaLlaves = []

        conexion= conn() #Abrimos conexión

        sql = f""" SELECT compraIdTemp
		                  ,facturaIdTemp
		                  ,productoIdTemp
		                  ,comercioIdTemp
                   FROM mercadosTemp 
                   WHERE mercadoIdTemp = ?
               """
        conexion.cursor.execute(sql, (self.mercadoIdTemp,)) #Ejecutamos consulta SQL
        
        listaLlaves = conexion.cursor.fetchall()

        conexion.desconectar()

        return listaLlaves

def cuadreFacturasModel():
    #Por cada factura con ítems en la compra en curso: id, número, suma de los ítems y total de la factura
    conexion = conn()

    sql = """ SELECT facturas.facturaId
                     ,facturas.numeroFactura
                     ,SUM(mercadosTemp.precioTotalTemp)
                     ,facturas.valorTotalFactura
              FROM mercadosTemp
                     INNER JOIN facturas
                         ON mercadosTemp.facturaIdTemp = facturas.facturaId
              GROUP BY facturas.facturaId
              ORDER BY MIN(mercadosTemp.mercadoIdTemp)
          """
    conexion.cursor.execute(sql)
    filas = conexion.cursor.fetchall()
    conexion.desconectar()

    return filas

def cargarCompraModel():
    #Carga a la tabla mercados los productos de la tabla mercados temporal
    conexion =conn()

    sql = f""" INSERT INTO mercados 
               SELECT {'NULL'}
                      ,compraIdTemp
                      ,facturaIdTemp
                      ,productoIdTemp
                      ,comercioIdTemp
                      ,cantidadTemp
                      ,precioUnidadTemp
                      ,precioTotalTemp
               FROM mercadosTemp
          """
    #Reseteamos la primary key autoincremente nuevamente a cero
    sql2 = f""" UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='mercadosTemp'
            """
    #Limpiamos tabla temporal
    sql3 =  f""" DELETE FROM mercadosTemp """
    
    conexion.cursor.execute(sql)
    conexion.cursor.execute(sql3)
    conexion.cursor.execute(sql2)

    conexion.desconectar()