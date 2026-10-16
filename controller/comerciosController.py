import sqlite3
from model.comercios import Comercios

class ComerciosController:
    #constructor
    def __init__(self
                 ,comercioId
                 ,nombreComercio
                 ,direccionComercio):
        
        self.comercioId = comercioId
        self.nombreComercio = nombreComercio
        self.direccionComercio = direccionComercio

    def titleDatos(self,):
        #Trasforma el texto poniendo la primera letra de cada palabra en mayusculas y elimina los espacios a los lados del texto
        self.nombreComercio = self.nombreComercio.strip().title()
        self.direccionComercio = self.direccionComercio.strip().title()

    def validarCamposComercio(self
                              ,nombreComercio
                              ,direccionComercio):
        
        #validamos los campos para no aceptar campos en blanco o sólo espacios
        if nombreComercio.isspace()==True or nombreComercio=='' or direccionComercio.isspace()==True or direccionComercio=='' :
            estado=0
        else:
            estado=1
        
        return estado

    def insertarComercios(self):
        #Método para insertar los comercios a la BD
        self.titleDatos()
        estado=self.validarCamposComercio(self.nombreComercio
                                         ,self.direccionComercio)

        if estado==1:
            try:
                comercio = Comercios(None
                                     ,self.nombreComercio
                                     ,self.direccionComercio)
                comercio.insertarComercios()
                messagebox = [1,
                              'Se insertó correctamente el comercio']
            except sqlite3.Error as ex:
                messagebox = [0,
                              f'No se pudo insertar el comercio: {ex}']
        if estado==0:
            messagebox = [0, 
                          'No se permiten campos vacíos... ponga bien esa mondá >.<']
        
        return messagebox
    
    def consultarListaComercios(self):
        #Se consultan todos los comercios registrados
        listaComercio =[]

        try:
            listadoComercio = Comercios(None
                                        ,None
                                        ,None)
            listaComercio = listadoComercio.consultarComercios()
        except sqlite3.Error as ex:
            print(f'Error al consultar comercios en la base de datos: {ex}')
        
        return listaComercio
    
    def consultarComerciosController(self):

        listaComrercio = []

        try:
            #Declaramos un objeto
            objComercios = Comercios(None
                                     ,self.nombreComercio
                                     ,None
                                     )
            #instanciamos la clase
            listaComrercio = objComercios.consultarComercioModel()
            messagebox = [1,'']
        except sqlite3.Error as ex:
            messagebox =[0,f"No se pudo consultar los comercios: {ex}"]
        return listaComrercio, messagebox
    
    def modificarComerciosController(self):
        
        self.titleDatos()

        estado=self.validarCamposComercio(self.nombreComercio
                                         ,self.direccionComercio)

        if estado==1:
            try:
                #declaramos el objeto
                comercio = Comercios(self.comercioId
                                    ,self.nombreComercio
                                    ,self.direccionComercio)
                comercio.modificarComerciosModel()
                messagebox = [1,
                              'Se actualizó el comercio']
            except sqlite3.Error as ex:
                messagebox = [0,
                              f'No se pudo actualizar el comercio: {ex}']
        if estado==0:
            messagebox = [0, 
                          'No se permiten campos vacíos... ponga bien esa mondá >.<']
        
        return messagebox