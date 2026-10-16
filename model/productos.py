#importamos la clase de conexión 
from model.conexionDb import ConexionDb as con


class Productos:
    #Constructor
    def __init__(self,productoId,nombreProducto):
        self.productoId = productoId
        self.nombreProducto = nombreProducto
        

    def insertarProductos(self):
            #Insertamos nuevo poducto
            conexion=con()
            sql = """INSERT INTO productos VALUES (NULL, ?)
                """
            conexion.cursor.execute(sql, (self.nombreProducto,))
            conexion.desconectar()
            estatus=0


    def consultarListaProductos(self):
        #Se crea conexion
        conexion=con()

        listaProductos = []
        
        #Consulta sql
        sql = f"""SELECT * FROM productos
               """
        conexion.cursor.execute(sql) #Ejecutamos consulta
        listaProductos = conexion.cursor.fetchall() #listamos infomación
        conexion.desconectar() #Cerramos conexión

        return listaProductos
    
    def consultarProductos(self):
         #Abrimos conexión
         conexion = con()

         producto =[]
        #Sentencia sql
         sql = """ SELECT * FROM productos WHERE nombreProducto LIKE ?
                 """
         conexion.cursor.execute(sql, (f'%{self.nombreProducto}%',))#Ejecutamos consulta
         producto = conexion.cursor.fetchall()#Listamos información
         conexion.desconectar()#Cerramos conexión

         return producto
    
    def editarProductos(self):
         #actualizamos un producto
         conexion = con()
         
         sql =  """ UPDATE productos
                  SET nombreProducto = ?
                  WHERE productoId = ?
                """
         conexion.cursor.execute(sql, (self.nombreProducto, self.productoId))
         conexion.desconectar()
         
        


