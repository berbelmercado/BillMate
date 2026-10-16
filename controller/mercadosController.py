import sqlite3
from model.mercados import Mercados
from controller.validaciones import esNumero, convertirNumero

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
            except sqlite3.Error as ex:
                mensaje = [0, f'No se pudo realizar la consulta: {ex}']
        else:
            mensaje = [0, 'Por favor seleccione una opción']
        return mensaje, listaMercado 
    
    def actualizarProductosController(self):

        mensaje = []

        #Validamos los precios antes de actualizar
        if not esNumero(self.precioUnidad):
            return [0, 'El campo "Precio unidad" no es válido']
        if not esNumero(self.precioTotal):
            return [0, 'El campo "Precio Total" no es válido']

        self.precioUnidad = convertirNumero(self.precioUnidad)
        self.precioTotal = convertirNumero(self.precioTotal)

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

        except sqlite3.Error as ex:

            mensaje = [0,f'No se pudo actualizar el producto: {ex}']

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
            

        except sqlite3.Error as ex:

            mensaje= [0,f'Error al consultar llaves: {ex}']
        
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
        except sqlite3.Error as ex:
            mensaje = [0,f'No es posible eliminar el producto: {ex}']
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
        except sqlite3.Error as ex:
            mensaje = [0, f'No fue posible realizar la consulta: {ex}']
        return mensaje, listaMercado 