from model.mercadoTemp import MercadoTemp
from model.mercadoTemp import cargarCompraModel

class MercadoTempController():

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

    def validacionCamposMercadosController(self):
        #Validamos los campos y los datos antes de hacer inserción
        
        estado = 1

        if self.compraIdTemp == None or self.facturaIdTemp == None or self.comercioIdTemp == None:
            #Si se envía uno o más campos vacíos no se hará la inserción
            estado = 0

        if self.precioUnidadTemp.isspace() or self.precioUnidadTemp == '' or self.precioUnidadTemp.isalpha() == True:
            #valida si el campo precio unidad está vacio o con espacio o con letras
            estado = 2


        if self.precioTotalTemp == None or self.precioTotalTemp== '' or self.precioTotalTemp.isalpha() == True:
            #valida si el campo precio total es vacío o se llena con espacio o con letras
            estado = 3

        return estado

    def insertarMercadosTempController(self):
        #Tratamos datos

        estado = self.validacionCamposMercadosController()

        if estado == 1: 
            self.precioUnidadTemp = float(self.precioUnidadTemp)
            self.precioTotalTemp = float(self.precioTotalTemp)

            mensaje = []

            try:
                objInsertarMercadosTemp = MercadoTemp(  self.mercadoIdTemp
                                                        ,self.compraIdTemp
                                                        ,self.facturaIdTemp
                                                        ,self.productoIdTemp
                                                        ,self.comercioIdTemp
                                                        ,self.cantidadTemp
                                                        ,self.precioUnidadTemp
                                                        ,self.precioTotalTemp
                                                        )
                objInsertarMercadosTemp.insertarMercadoTempral()

                mensaje = [1,'Producto agregado']

            except NameError as ex:
                mensaje = [0, 'No fue posible insertar el producto Error: {ex}']
        if estado ==0:
            mensaje = [0,'No se permiten campos vacíos']

        if estado == 2:
            
            mensaje = [0, 'El campo "Precio unidad" no es válido']
        
        if estado == 3:
            mensaje = [0, 'El campo "Precio Total" no es válido']

        return mensaje
    
    def  consultarMercadoTempController(self):
        mensaje = []

        listaMercadosTemp = []
        
        try:
            objConsultarMercadosTemp = MercadoTemp(  self.mercadoIdTemp
                                                    ,self.compraIdTemp
                                                    ,self.facturaIdTemp
                                                    ,self.productoIdTemp
                                                    ,self.comercioIdTemp
                                                    ,self.cantidadTemp
                                                    ,self.precioUnidadTemp
                                                    ,self.precioTotalTemp
                                                    )
            listaMercadosTemp = objConsultarMercadosTemp.consultarMercadosTemporal()
            mensaje=[1]
        except NameError as ex:

            mensaje = [0,f'No se pudo conectar a la bd error: {ex}']

        return listaMercadosTemp, mensaje
    
    def actualizarProductosController(self):

        mensaje = []

        try:
            objModificarMercadosTemp = MercadoTemp( self.mercadoIdTemp
                                                    ,self.compraIdTemp
                                                    ,self.facturaIdTemp
                                                    ,self.productoIdTemp
                                                    ,self.comercioIdTemp
                                                    ,self.cantidadTemp
                                                    ,self.precioUnidadTemp
                                                    ,self.precioTotalTemp
                                                    )
            objModificarMercadosTemp.actualizarProductoTemporal()

            mensaje = [1,'Producto Modificado']

        except NameError as ex:

            mensaje=[0,'No fue posible modificar el producto Error: {ex}']

        return mensaje
    
    def consultarKeysMercadosTempController(self):
        #consultamos las llaves primaris desde la base de datos

        listaLaves = []

        mensaje = []

        try:
            #Creamos objeto e instanciamos la clase
            objConsultaLavesMercadosTemp = MercadoTemp( self.mercadoIdTemp
                                                    ,None
                                                    ,None
                                                    ,None
                                                    ,None
                                                    ,None
                                                    ,None
                                                    ,None
                                                    )
            listaLaves = objConsultaLavesMercadosTemp.consultarKeysMercadosTempModel()#Traemos la lista de llaves
            
            mensaje= [1,'']

        except NameError as ex:

            mensaje= [0,f'Error al consultar llaves: {ex}']
        
        return listaLaves, mensaje

    def eliminarProductosTempController(self):
        #Elimina los productos de la tabla temporal
        mensaje = []
        try:
            #Instanciamos la clase
            objEliminarPoroductoTempController = MercadoTemp(self.mercadoIdTemp
                                                             ,None
                                                             ,None
                                                             ,None
                                                             ,None
                                                             ,None
                                                             ,None
                                                            ,None
                                                            )
            objEliminarPoroductoTempController.eliminarMercadoTemporal()

            mensaje = [1]
        except NameError as ex:

            mensaje = [0,'No se pudo eliminar el producto error: {ex}']
        
        return mensaje
    
def fnCargarCompraController():
    #Carga a la tabla mercados los productos de la tabla mercados temporal
    mensaje = []

    try:    
        cargarCompraModel()
        mensaje = [1, 'Se ha cargado la compra correctamente']
    except NameError as ex:
        mensaje = [0,f'No fue posible cargar la compra Error: {ex}']
    
    return mensaje