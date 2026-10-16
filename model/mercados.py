from model.conexionDb import ConexionDb as conn

class Mercados():
    #Constructor
    def __init__(self
                 ,mercadoId
                 ,compraId
                 ,descCompra
                 ,facturaId
                 ,numeroFactura
                 ,productoId
                 ,nombreProducto
                 ,comercioId
                 ,cantidad
                 ,precioUnidad
                 ,precioTotal
                 ,opcion):
        
        self.mercadoId = mercadoId
        self.compraId = compraId
        self.descCompra = descCompra
        self.facturaId = facturaId
        self.numeroFactura = numeroFactura
        self.productoId = productoId
        self.nombreProducto = nombreProducto
        self.comercioId = comercioId
        self.cantidad = cantidad
        self.precioUnidad = precioUnidad
        self.precioTotal = precioTotal
        self.opcion = opcion

        self.sqlOpciones = ['productos.nombreProducto'
                        ,'facturas.numeroFactura'
                        ,'compras.describcion'
                      ]
        self.sqlCampo =[self.nombreProducto
                   ,self.numeroFactura
                   ,self.descCompra
                  ]
    
    def consultarMercadosModel(self):

        listaMercado = []
        
        conexion = conn()

        #El nombre de la columna sale de la lista fija sqlOpciones; el texto buscado va como parámetro
        sql = f""" SELECT  mercados.mercadoId
                            ,productos.nombreProducto
                            ,mercados.cantidad
                            ,mercados.precioUnidad
                            ,mercados.precioTotal
                            ,facturas.numeroFactura
                            ,facturas.fechaFactura
                            ,comercios.nombreComercio
                            ,compras.describcion
                    FROM mercados
                            INNER JOIN productos
                                ON mercados.productoId = productos.productoId
                            INNER JOIN facturas
                                ON mercados.facturaId = facturas.facturaId
                            INNER JOIN comercios
                                ON mercados.comercioId = comercios.comercioId
                            INNER JOIN compras
                                ON mercados.compraId = compras.idCompra
                    WHERE {self.sqlOpciones[self.opcion]} like ?
                    ORDER BY mercados.mercadoId DESC
               """
        conexion.cursor.execute(sql, (f'%{self.sqlCampo[self.opcion]}%',))
        listaMercado =  conexion.cursor.fetchall()
        conexion.desconectar()

        return listaMercado

    def actualizarMercadosModel (self):

        conexion = conn() #Abrimos conexión
        #Consulta SQL
        sql = """ UPDATE  mercados
                   SET compraId = ?
                       ,facturaId = ?
                       ,productoId = ?
                       ,comercioId = ?
                       ,cantidad = ?
                       ,precioUnidad = ?
                       ,precioTotal = ?
                   WHERE mercadoId = ?
               """

        conexion.cursor.execute(sql, (self.compraId
                                      ,self.facturaId
                                      ,self.productoId
                                      ,self.comercioId
                                      ,self.cantidad
                                      ,self.precioUnidad
                                      ,self.precioTotal
                                      ,self.mercadoId))
        conexion.desconectar()

    def consultarKeysMercadosModel(self):
        #consultamos las llaves primarias desde la base de datos

        listaLlaves = []

        conexion= conn() #Abrimos conexión

        sql = """ SELECT  compraId
		                  ,facturaId
		                  ,productoId
                          ,comercioId
                   FROM mercados
                   WHERE mercadoId = ?
               """
        conexion.cursor.execute(sql, (self.mercadoId,)) #Ejecutamos consulta SQL
        
        listaLlaves = conexion.cursor.fetchall()

        conexion.desconectar()

        return listaLlaves

    def eliminarProductosModel(self):

        conexion = conn()

        sql = """ DELETE FROM mercados
                   WHERE mercadoId = ?
               """
        conexion.cursor.execute(sql, (self.mercadoId,))
        conexion.desconectar()
    
    def consultarUltimoMercado(self):
        
        conexion = conn()

        sql = f""" SELECT  mercados.mercadoId
                            ,productos.nombreProducto
                            ,mercados.cantidad
                            ,mercados.precioUnidad
                            ,mercados.precioTotal
                            ,facturas.numeroFactura
                            ,facturas.fechaFactura
                            ,comercios.nombreComercio
                            ,compras.describcion
                    FROM mercados 
                            INNER JOIN productos
                                ON mercados.productoId = productos.productoId
                            INNER JOIN facturas 
                                ON mercados.facturaId = facturas.facturaId
                            INNER JOIN comercios
                                ON mercados.comercioId = comercios.comercioId
                            INNER JOIN compras
                                ON mercados.compraId = compras.idCompra
                    WHERE mercados.compraId = (SELECT idCompra FROM compras ORDER BY idCompra DESC  LIMIT 1)
                    ORDER BY mercados.mercadoId DESC
                    """
            
        conexion.cursor.execute(sql)
        listaMercado =  conexion.cursor.fetchall()
        conexion.desconectar()

        return listaMercado