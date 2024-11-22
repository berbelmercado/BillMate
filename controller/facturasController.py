from model.facturas import Facturas

class FacturaController:
    #Controlador para facturas
    def __init__(self
                 ,facturaId
                 ,numeroFactura
                 ,valorTotalFactura
                 ,fechaFactura):
        self.facturaId = facturaId
        self.numeroFactura = numeroFactura
        self.valorTotalFactura = valorTotalFactura
        self.fechaFactura = fechaFactura
    
    def titleDatos(self):
        #Trasforma el texto poniendo la primera letra de cada palabra en mayusculas y elimina los espacios a los lados del texto
        self.numeroFactura = self.numeroFactura.strip().upper()       

    def validarCamposFacturas(self
                              ,numeroFactura
                              ,valorTotalFactura
                              ,fechaFactura
                              ):
            estado=None 
            try:
                        self.valorTotalFactura=float(self.valorTotalFactura)
            except:
                 estado=2
            #Validamos si se envía datos vacíos o letras en el campo de "Valor total factura"
            if numeroFactura.isspace()==True or numeroFactura=='' or valorTotalFactura.isspace()==True or valorTotalFactura=='' or fechaFactura.isspace()==True or fechaFactura=='' and  valorTotalFactura.isdecimal()==True:
                estado=0
            else:
                estado=1

            try:
                    self.valorTotalFactura=float(valorTotalFactura)
            except:
                 estado=2

            return estado
         
    def insertarFacturas(self):
        #Método para insertar facturas a la BD
        self.titleDatos()
        estado=self.validarCamposFacturas(self.numeroFactura
                                        ,self.valorTotalFactura
                                        ,self.fechaFactura)
        
        if estado==1:
            try:
                insertar=Facturas(None
                                  ,self.numeroFactura
                                  ,self.valorTotalFactura
                                  ,self.fechaFactura
                                  )
                insertar.insertarFacturas()
                mensageInserción = [1,'Factura ingresada correctamente']
            except NameError as ex :
                print (ex)
                mensageInserción = [0,'Error al insertar factura']
        elif estado==0:
            mensageInserción = [0, 'No se admiten campos vacíos. Por favor valide nuevamente']
        elif estado==2:
            mensageInserción = [2,'Solo se admiten caracteres númericos en el campo "Total Factura"']

        return mensageInserción
    
    def consultarListaFacturas(self):
        
        listadoFacturas = []
        
        try:
            listaFacturas = Facturas(None
                                     ,None
                                     ,None
                                     ,None)
            listadoFacturas = listaFacturas.consultarListaFacturas()
        except:
            messageConsulta = [0,'No se pudo obtener información de las facturas']

        return listadoFacturas
    
    def consultarFacturasController(self):

        listadoConsutaFactura = []

        try:
            objFactura = Facturas(None
                                  ,self.numeroFactura
                                  ,None
                                  ,None)
            listadoConsutaFactura = objFactura.consultarFacturasModel()
            mensajeConsulta = [1, '']
        except:
            mensajeConsulta = [0,'Problemas con la conexión a la base de datos']

        return listadoConsutaFactura, mensajeConsulta
    
    def modificarFacturas(self):
                #Método para insertar facturas a la BD
        self.titleDatos()

        estado=self.validarCamposFacturas(self.numeroFactura
                                        ,self.valorTotalFactura
                                        ,self.fechaFactura)
        if estado==1:
            try:
                objmodificarFactura=Facturas(self.facturaId
                                          ,self.numeroFactura
                                          ,self.valorTotalFactura
                                          ,self.fechaFactura
                                          )
                objmodificarFactura.modificarFacturas()
                mensageInserción = [1,'Factura ingresada correctamente']
                
            except:
                mensageInserción = [0,'Error al insertar factura']
        elif estado==0:
            mensageInserción = [0, 'No se admiten campos vacíos. Por favor valide nuevamente']
        elif estado==2:
            mensageInserción = [2,'Solo se admiten caracteres númericos en el campo "Total Factura"']

        return mensageInserción
            

