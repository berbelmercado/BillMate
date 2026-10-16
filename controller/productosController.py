import sqlite3
from model.productos import  Productos

class ProductosController:

    def __init__(self,productoId, nombreProducto):
        self.nombreProducto = nombreProducto
        self.productoId = productoId
        
    def titleDatos(self):
        #tomar la primera letra de cada palabra y convertirla a mayuscula y quita espacios a los lados del texto
         self.nombreProducto=self.nombreProducto.strip().title()
    
    def validarCamposProductos(self
                               ,nombreProducto):
        #Validamos si se envía datos en blanco
        estado=None
        if nombreProducto.isspace()==True or nombreProducto=='':
            estado=0
        else:
            estado=1
        return estado
        
    def insertarProducto(self):
        #Metodo para insertar los productos a la BD
        #validamos los campos
        self.titleDatos()
        estado=self.validarCamposProductos(self.nombreProducto)
        if estado==1:
            try:
                #Declaramos objeto
                nombreProducto = Productos(None
                                           ,self.nombreProducto)
                nombreProducto.insertarProductos()#llamamos función desde el modelo
                mensajeInsersion = [1,'Se insertó el producto correctamente']
            except sqlite3.IntegrityError:
                mensajeInsersion = [0, f'Ya existe un producto llamado "{self.nombreProducto}"']
            except sqlite3.Error as ex:
                mensajeInsersion =[0, f'No se insertó el producto: {ex}']
        else:
            mensajeInsersion=[0,'No se admiten campos vacíos']
       
        return mensajeInsersion
    
    def consultarListaProducto(self):
        #Consula productos solo con abrir la vista
        listadoProductos = []
        try:
            #Declaramos el objeto
            listaProductos = Productos(None
                                       ,None)
            
            listadoProductos=listaProductos.consultarListaProductos()#llamamos función desde el modelo
            mensajeconsulta=[1]
        except sqlite3.Error as ex:
            #Devolvemos mensaje a la vista en caso de error
            mensajeconsulta= [0
                              ,f'No fue posible consultar lista de productos: {ex}']

        return listadoProductos,mensajeconsulta
    
    def consultarProductos(self):
        #Consulta productos desde el botón de consulta

        #Declaramos variable vacía
        listadoProductos = []

        try:
            #declaramos el objeto
            listaProductos = Productos(None
                                       ,self.nombreProducto)
            
            listadoProductos=listaProductos.consultarProductos()#llamamos la función consultar desde del modelo

            mensajeconsulta=[1]
        except sqlite3.Error as ex:
            #En caso de error enviamos a la vista  mensaje
            mensajeconsulta= [0
                              ,f'No fue posible consultar productos: {ex}']

        return listadoProductos,mensajeconsulta
    

    def editarProductos(self):

        #aplitamos title a los campos
        self.titleDatos()

        #validamos los campos
        estado=self.validarCamposProductos(self.nombreProducto)
        
        if estado==1:
            try:
                #declaramos el objeto
                nombreProducto = Productos(self.productoId
                                           ,self.nombreProducto)
                nombreProducto.editarProductos()#llamamos la función editar del modelo
                mensajeInsersion = [1,'Se modificó el producto correctamente']
            except sqlite3.IntegrityError:
                mensajeInsersion = [0, f'Ya existe un producto llamado "{self.nombreProducto}"']
            except sqlite3.Error as ex:
                mensajeInsersion =[0, f'No se modificó el producto: {ex}']
                
        else:
            mensajeInsersion=[0,'No se admiten campos vacíos']
       
        return mensajeInsersion
        
