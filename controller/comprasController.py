import sqlite3
from model.compras import Compras

class ComprasController():
    def __init__(self,
                 idCompra
                 ,describcionCompra
                 ,fechaCreacionCompra):
        
        self.idCompra = idCompra
        self.describcionCompra = describcionCompra
        self.fechaCreacionCompra = fechaCreacionCompra
        

    def formatoDatos(self):
        #Formateamos la describción
        self.describcionCompra=self.describcionCompra.strip().title()

    def validarDatosCompras(self):
        #Validamos la describción

        self.formatoDatos() #Formateamos datos
        
        control =None  #Inicializamos variable de control

        if self.describcionCompra =='' or self.describcionCompra.isspace()==True : 
            control=0
        else:
            control=1

        return control
    
    def insertarCompras(self):
        #Función para registrar compras
        mensaje = [] #Inicializamos variable mensaje

        #Objenmos resultado de la evaluación
        estado = self.validarDatosCompras()

        if estado==1:
            try:
                objInsertarCompras= Compras(None
                                            ,self.describcionCompra
                                            ,self.fechaCreacionCompra)
                objInsertarCompras.insertarCompras()
                mensaje=[1,'Se insertó correctamente la compra']
            except sqlite3.Error as ex:
                mensaje=[0,f'Error al insertar la compra: {ex}']
        if estado==0:
            mensaje=[0,'No se permite enviar la describción en blanco']
        
        return mensaje
    
    def consultarComprasRegistradasController(self):
        listadoComprasRegistradas = []

        try:
            #Intanciamos clase Compras desde el modelo
            objComprasRegistradas = Compras(None
                                            ,None
                                            ,None)
            #Ejecutamos la consulta select y guardamos los registros en una lista
            listadoComprasRegistradas = objComprasRegistradas.buscarComprasRegistradas()

        except sqlite3.Error as ex:
            print(f'Error al consultar compras registradas: {ex}')

        return listadoComprasRegistradas
    
    def consultarCompra(self):
        listadoCompra = []#Inicializamos variable 
        mensaje = []

        try:
            #Instanciamos la clase Compras
            objConsultarCompra = Compras(None
                                         ,self.describcionCompra
                                         ,None)
            
            listadoCompra = objConsultarCompra.consultarCompras() #Ejecutamos la consultas 

            mensaje=[1]
        except sqlite3.Error as ex:
            mensaje=[0,f'Error al consultar la compra: {ex}']

        return listadoCompra,mensaje
    
    def modificarCompra(self):

        self.formatoDatos()
        mensaje= []

        try:
            #Instanciamos la clase
            objModificarCompra = Compras(self.idCompra
                                         ,self.describcionCompra
                                         ,None)
            objModificarCompra.modificarCompras()

            mensaje = [1,'Se modificó la compra corectamente']

        except sqlite3.Error as ex:
            mensaje=[0,f'Error al modificar la compra: {ex}']

        return mensaje