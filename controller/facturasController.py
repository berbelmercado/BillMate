import sqlite3
from model.facturas import Facturas
from controller.validaciones import convertirNumero

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
            #Validamos si se envía datos vacíos
            if numeroFactura.strip()=='' or valorTotalFactura.strip()=='' or fechaFactura.strip()=='':
                return 0

            #Validamos que "Valor total factura" sea numérico (acepta 12.500 y 12.500,50)
            valor = convertirNumero(valorTotalFactura)
            if valor is None:
                return 2

            self.valorTotalFactura = valor
            return 1
         
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
            except sqlite3.Error as ex:
                mensageInserción = [0,f'Error al insertar factura: {ex}']
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
        except sqlite3.Error as ex:
            print(f'No se pudo obtener información de las facturas: {ex}')

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
        except sqlite3.Error as ex:
            mensajeConsulta = [0,f'Problemas con la conexión a la base de datos: {ex}']

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
                mensageInserción = [1,'Factura modificada correctamente']

            except sqlite3.Error as ex:
                mensageInserción = [0,f'Error al modificar factura: {ex}']
        elif estado==0:
            mensageInserción = [0, 'No se admiten campos vacíos. Por favor valide nuevamente']
        elif estado==2:
            mensageInserción = [2,'Solo se admiten caracteres númericos en el campo "Total Factura"']

        return mensageInserción
            

