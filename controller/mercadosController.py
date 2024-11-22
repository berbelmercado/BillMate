from model.mercados import Mercados

class MercadosController():
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
    
    def consultarMercadosController(self):
        #Consultamos los productos de la base de datos dependiendo la opción escogida 
        mensaje=[]
        
        listaMercado=[]
        if self.opcion != None:

            try:
                objMercadosModel = Mercados(self.mercadoId
                                            ,self.compraId
                                            ,self.descCompra
                                            ,self.facturaId
                                            ,self.numeroFactura
                                            ,self.productoId
                                            ,self.nombreProducto
                                            ,self.comercioId
                                            ,self.cantidad
                                            ,self.precioUnidad
                                            ,self.precioTotal
                                            ,self.opcion
                                            )
                listaMercado = objMercadosModel.consultarMercadosModel()
                mensaje =[1]
            except:
                mensaje = [0, 'No se pudo realizar la consulta']
        else:
            mensaje = [0, 'Por favor seleccione una opción']
        return mensaje, listaMercado 
    
    def actualizarProductosController(self):

        mensaje = []

        try:
            #Objeto
            objActualizarProductosController = Mercados(self.mercadoId
                                            ,self.compraId
                                            ,self.descCompra
                                            ,self.facturaId
                                            ,self.numeroFactura
                                            ,self.productoId
                                            ,self.nombreProducto
                                            ,self.comercioId
                                            ,self.cantidad
                                            ,self.precioUnidad
                                            ,self.precioTotal
                                            ,self.opcion
                                            )
            objActualizarProductosController.actualizarMercadosModel()#Ejecutamos función del modelo

            mensaje =[1,'']

        except:
            
            mensaje = [0,'No se pudo actualizar el producto :c']

        return mensaje

    def consultarKeysMercadosController(self):
        #consultamos las llaves primaris desde la base de datos

        listaLaves = []

        mensaje = []

        try:
            #Creamos objeto e instanciamos la clase
            objConsultaLavesMercadosTemp = Mercados( self.mercadoId
                                                    ,None
                                                    ,None
                                                    ,None
                                                    ,None
                                                    ,None
                                                    ,None
                                                    ,None
                                                    ,None
                                                    ,None
                                                    ,None
                                                    ,None
                                                    )
            listaLaves = objConsultaLavesMercadosTemp.consultarKeysMercadosModel()#Traemos la lista de llaves
            
            mensaje= [1,'']
            

        except:

            mensaje= [0,f'Error al consultar llaves']
        
        return listaLaves, mensaje
    
    def eliminarProductosController(self):

        try:
            objEliminarProductosController = Mercados(self.mercadoId
                                            ,self.compraId
                                            ,self.descCompra
                                            ,self.facturaId
                                            ,self.numeroFactura
                                            ,self.productoId
                                            ,self.nombreProducto
                                            ,self.comercioId
                                            ,self.cantidad
                                            ,self.precioUnidad
                                            ,self.precioTotal
                                            ,self.opcion)
            objEliminarProductosController.eliminarProductosModel()

            mensaje = [1,'Fue eliminado el producto']
        except:
            mensae = [0,'No se es posible eliminar el producto']
        return mensaje
    
    
    def consultarUltimosMercadosController(self):
        #Consultamos los productos de la base de datos dependiendo la opción escogida 
        mensaje=[]
        
        listaMercado=[]

        try:
            objMercadosModel = Mercados(self.mercadoId
                                        ,self.compraId
                                        ,self.descCompra
                                        ,self.facturaId
                                        ,self.numeroFactura
                                        ,self.productoId
                                        ,self.nombreProducto
                                        ,self.comercioId
                                        ,self.cantidad
                                        ,self.precioUnidad
                                        ,self.precioTotal
                                        ,self.opcion
                                        )
            listaMercado = objMercadosModel.consultarUltimoMercado()
            mensaje =[1]
        except:
            mensaje = [0, 'No fue posible realizar la consulta']
        return mensaje, listaMercado 