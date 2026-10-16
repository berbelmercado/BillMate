from tkinter import ttk
from PIL import Image
from customtkinter import CTkToplevel,CTkFrame,CTkLabel,CTkButton,CTkEntry,CTkScrollbar,CTkImage
from views.ventanasSecundarias import configuracionVentanasSecundarias as conSec
from views.ventanasSecundarias.configuracionVentanasSecundarias import dicConfigConsultarFactura as conFac
from views.configuracionesGenerales import dicConfiguracionGeneralColores as conColores
from views.configuracionesGenerales import dicConfiguracionGeneralFuentes as conFuentes
from views.configuracionesGenerales import dicConfig as conMaus
from controller.productosController import ProductosController
from views.messagebox import mensajesEmergentes as msbx
from views.vwImgConfig import  leerImagen


class ConsultarProductos(CTkToplevel):

    def __init__(self,master):
        super().__init__(master)
        self.master=master
        self.geometry(f"{conSec.dicConfigConsultarProducto['vpConsultarProductoWidth']}x{conSec.dicConfigConsultarProducto['vpConsultarProductoHeight']}+{conSec.dicConfigPosicion['vnConsultarProductosX']}+{conSec.dicConfigPosicion['vnConsultarProductosY']}")
        self.title("Consulta Productos")
        #Importamos la imagenes
        self.imagenBuscar=CTkImage(dark_image=Image.open(leerImagen("Consultar")),size=(28,28))
        self.imagenCancelar= CTkImage(dark_image=Image.open(leerImagen("Cancelar")),size=(28,28))
        self.imagenActualizar=CTkImage(dark_image = Image.open(leerImagen("Actualizar")),size=(28,28))
        self.imagenCargar = CTkImage(dark_image =Image.open(leerImagen("cargar")),size=(28,28))
        self.iconbitmap(leerImagen("Logo"))
        self.resizable(False,False)
        self.transient(master)
        self.lift()
        self.buscarProducto()
        self.frameModificaciones()
        self.twConsultarProducto()
    
    def btnCancelar(self):
        #Funcionalidad botón cancelar
        self.destroy()
    
    def fnModificarProducto(self):
        #Funcionalidad para modificación de producto
        #declaramos objeto
        objProducto = ProductosController(self.productoId,self.etNombreProducto.get())
        mensaje = objProducto.editarProductos()

        if mensaje[0]==1:
            self.etNombreProducto.delete(0,'end')
            msbx.mensajeInformativo(mensaje[1])
            self.twConsultarProducto()
        if mensaje[0]==0:
            msbx.mensajeError(mensaje[1])

    def fnEventoConsultarProducto(self,event):
            #evento para consultar producto cada que se ingresa una letra
            try:
                self.fnBuscarProducto()
            except:
                pass

    def fnEventoModificarProducto(self,event):
            #Evento paara modificar el producto con la tecla enter
            try:
                self.fnModificarProducto()
            except:
                pass


    def consultarProductos(self):
        #consulta Lista de productos existentes en la bd y los envía a la función twConsultarProducto
        listadoProductos = []
       #Declaramos objeto
        consultaProductos = ProductosController(None
                                               ,None)
        listadoProductos,mensaje= consultaProductos.consultarListaProducto()#llamamos función desde el controlador

        if mensaje[0]==0:
            msbx.mensajeError(mensaje[1])

        return listadoProductos


    def fnBuscarProducto(self):
         #Funcionalidad botón buscar
         productos = ProductosController(None
                                         ,self.etIngresarNombreProducto.get()) #Creamos el objeto


         listaProducto,mensaje = productos.consultarProductos() #llamamos al método consultar producto

         if mensaje[0]==1:
            #Borramos la información insertada en la tabla
            for i in self.twConsultarProductos.get_children():
                 self.twConsultarProductos.delete(i)
            
            #Insertamos la información consultada en la tabla
            for i in listaProducto:
                 self.twConsultarProductos.insert(""
                                                  ,'end'
                                                  ,text=i[0]
                                                  ,values=(i[1],)
                                                  ,tags='evenrow')
         else:
             msbx.mensajeError(mensaje[1])
    
    def buscarProducto(self):
        #Se dibujan los widgets para buscar producto
        self.fmPrincipal= CTkFrame(self
                                    ,fg_color=conColores["fg_color"]
                                    )
        self.fmPrincipal.place(x=conSec.dicConfigConsultarProducto["fmPrincipalConsultarProductoX"]
                               ,y=conSec.dicConfigConsultarProducto["fmPrincipalConsultarProductoY"]
                               )
        
        #Label ingresar nombre del producto
        self.lbIngresarNombreProducto = CTkLabel(self.fmPrincipal
                                                 ,text='Ingrese Nombre Producto'
                                                ,fg_color=conColores["bgLabels"]
                                                ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                                ,text_color=conColores["colorLetrasLabel"]
                                                ,corner_radius=8
                                                ,width=conSec.dicConfigConsultarProducto["lbIngresarNombreProductoWidth"]
                                                ,height=conSec.dicConfigConsultarProducto["lbIngresarNombreProductoHeight"]
                                                )
        self.lbIngresarNombreProducto.grid(column=0
                                           ,row=0
                                           ,padx=conSec.dicConfigConsultarProducto["padXFmModificaciones"]
                                           ,pady=conSec.dicConfigConsultarProducto["padYFmModificaciones"]
                                           )
        
        #Entry ingresar nombre del producto
        self.etIngresarNombreProducto = CTkEntry(self.fmPrincipal
                                                 ,fg_color=conColores["bgEntrys"]
                                                 #,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                                 ,text_color=conColores["colorLetrasEntry"]
                                                 ,justify='center'
                                                 ,corner_radius=8
                                                 ,width=conSec.dicConfigConsultarProducto["etIngresarNombreProductoWidth"]
                                                 ,height=conSec.dicConfigConsultarProducto["etIngresarNombreProductoHeight"]
                                                 )
        self.etIngresarNombreProducto.grid(column=0
                                            ,row=1
                                            ,padx=conSec.dicConfigConsultarProducto["padXFmModificaciones"]
                                            ,pady=conSec.dicConfigConsultarProducto["padYFmModificaciones"]
                                            )
        #Button buscar productos
        self.btBuscarProductos = CTkButton(self.fmPrincipal
                                           ,text='Buscar'
                                           ,fg_color=conColores["bgBotones"]
                                           ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                           #,text_color=conColores["ColorLetras"]
                                           ,command=self.fnBuscarProducto
                                           ,image=self.imagenBuscar
                                           ,cursor=conMaus["cursor"]
                                           ,compound=conMaus["compound"]
                                           ,width=conSec.dicConfigConsultarProducto["btBuscarProductosWidth"]
                                           ,height=conSec.dicConfigConsultarProducto["btBuscarProductosHeight"]   
                                           )
        self.btBuscarProductos.grid(column=0
                                     ,row=2
                                     ,padx=conSec.dicConfigConsultarProducto["padXFmModificaciones"]
                                     ,pady=conSec.dicConfigConsultarProducto["padYFmModificaciones"]     
                                    )
        #Boton cancelar
        self.btnCancelarConsulta=CTkButton(self.fmPrincipal
                                           ,text='Cancelar O Salir'
                                           ,fg_color=conColores["bgBotones"]
                                           ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                           #,fg=conColores["ColorLetras"]
                                           ,command=self.btnCancelar
                                           ,image=self.imagenCancelar
                                           ,cursor=conMaus["cursor"]
                                           ,compound=conMaus["compound"]
                                           ,width=conSec.dicConfigConsultarProducto["btnCancelarConsultaWidth"]
                                           ,height=conSec.dicConfigConsultarProducto["btnCancelarConsultaHeight"]
                                           )
        self.btnCancelarConsulta.grid(column=0
                                      ,row=3
                                      ,padx=conSec.dicConfigConsultarProducto["padXFmModificaciones"]
                                      ,pady=conSec.dicConfigConsultarProducto["padXFmModificaciones"]
                                     )
        
        self.etIngresarNombreProducto.bind('<Key>',self.fnEventoConsultarProducto)

  
    def frameModificaciones(self):
            #Se dibijan los widgeds para la edición de los datos del producto
            #Frame modificaciones
            self.fmFrameModificacionProducto=CTkFrame(self
                                                      ,fg_color=conColores['fg_color']
                                                      )
            self.fmFrameModificacionProducto.place(x=conSec.dicConfigConsultarProducto["fmFrameModificacionProductoX"]
                                                   ,y=conSec.dicConfigConsultarProducto["fmFrameModificacionProductoY"])
            
            #Label Nombre Producto
            self.lbNombreProducto= CTkLabel(self.fmFrameModificacionProducto
                                            ,text='Nombre Producto'
                                            ,fg_color=conColores["bgLabels"]
                                            ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                            ,text_color=conColores["colorLetrasLabel"]
                                            ,corner_radius=8
                                            ,width=conSec.dicConfigConsultarProducto["lbNombreProductoWidth"]
                                            ,height=conSec.dicConfigConsultarProducto["lbNombreProductoHigth"]
                                            )
            self.lbNombreProducto.grid(column=0
                                        ,row=0
                                        ,padx=conSec.dicConfigConsultarProducto["padXFmModificaciones"]
                                        ,pady=conSec.dicConfigConsultarProducto["padXFmModificaciones"]
                                        )
            #Entry Nombre Producto
            self.etNombreProducto=CTkEntry(self.fmFrameModificacionProducto
                                            ,fg_color=conColores["bgEntrys"]
                                            #,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                            ,text_color=conColores["colorLetrasEntry"]
                                            ,justify='center'
                                            ,corner_radius=8
                                            ,width=conSec.dicConfigConsultarProducto["etNombreProductoWidth"]
                                            ,height=conSec.dicConfigConsultarProducto["etNombreProductoHigth"]
                                            )
            self.etNombreProducto.grid(column=0 
                                       ,row=1
                                       ,padx=conSec.dicConfigConsultarProducto["padXFmModificaciones"]
                                       ,pady=conSec.dicConfigConsultarProducto["padXFmModificaciones"])
            
            #Button Modificar producto
            self.btnModificarProducto=CTkButton(self.fmFrameModificacionProducto
                                                ,text=' Actualizar Cambio'
                                                ,fg_color=conColores["bgBotones"]
                                                ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                                #,text_color=conColor["ColorLetras"]
                                                ,command=self.fnModificarProducto
                                                ,image=self.imagenActualizar
                                                ,cursor=conMaus["cursor"]
                                                ,compound=conMaus["compound"]
                                                ,width=conSec.dicConfigConsultarProducto["btGuardarCambioItemWidht"]
                                                ,height=conSec.dicConfigConsultarProducto["btGuardarCambioItemHeight"]
                                                )
            self.btnModificarProducto.grid(column=0
                                           ,row=2
                                           ,padx=conSec.dicConfigConsultarProducto["padXFmModificaciones"]
                                           ,pady=conSec.dicConfigConsultarProducto["padXFmModificaciones"]
                                           )

            self.etNombreProducto.bind('<Return>',self.fnEventoModificarProducto)

    def twConsultarProducto(self):     
       #Ejecutamos la función que trae toda la lista de productos disponibles
       listadoProductos=self.consultarProductos()
       #creación frame para treeview
       self.fmTreviewConsultarProductos= CTkFrame(self
                                                  ,fg_color=conColores["fg_color"]
                                                 )
       self.fmTreviewConsultarProductos.place(x=conSec.dicConfigConsultarProducto["fmPrincipalResultadoX"]
                                              ,y=conSec.dicConfigConsultarProducto["fmPrincipalResultadoY"]
                                              )
       
       #Label Resultado busqueda
       self.lbResultadoBusqueda = CTkLabel(self.fmTreviewConsultarProductos
                                           ,text='Resultado de Busqueda'
                                           ,fg_color=conColores["bgLabels"]
                                           ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                           ,text_color=conColores["colorLetrasLabel"]
                                           ,corner_radius=8
                                           )
       self.lbResultadoBusqueda.pack(anchor=conSec.dicConfigConsultarProducto["lbResultadoBusquedaAnchor"]
                                     ,pady=conSec.dicConfigConsultarProducto["lbResultadoBusquedaPady"])
       #creación de treview para resultados de productos buscados
       self.twConsultarProductos = ttk.Treeview(self.fmTreviewConsultarProductos
                                                ,style='Treeview'
                                                ,columns=('Nombre'
                                                         )
                                                ,height=conSec.dicConfigConsultarProducto['twConsultarProductosHeight']
                                                
                                                )
       #Configuración para las filas seleccionadas
       self.twConsultarProductos.tag_configure('evenrow'
                                                ,background=conColores["bgGeneral"]
                                                ,foreground=conColores["ColorLetras"]
                                                )
       
       # #Indicamos el titulo de las columnas
       self.twConsultarProductos.heading("#0", text='Producto Id',)
       self.twConsultarProductos.heading("#1", text='Nombre Producto',)
        
       # #configuramos las columnas
       self.twConsultarProductos.column("#0",width=90, anchor='center', )
       self.twConsultarProductos.column("#1",width=200,  anchor='center')       

       self.twConsultarProductos.pack(side='left',fill='y', expand=True)
       
       self.scrolbar = CTkScrollbar(self.fmTreviewConsultarProductos
                            ,command = self.twConsultarProductos.yview
                            ,orientation = 'vertical'
                            ,bg_color = conColores["bgLabels"]
                            ,button_color = conColores["fg_color"]
                            )
       
       self.scrolbar.pack(side='right',fill='y')
       
       #insertamos los datos a la tabla 
       for i in listadoProductos:
             self.twConsultarProductos.insert("",'end',text=i[0],values=(i[1],),tags='evenrow')
       self.twConsultarProductos.configure(yscrollcommand=self.scrolbar.set)
       
       self.twConsultarProductos.bind("<<TreeviewSelect>>",self.seleccionarProductos)#invocamos la función del evento
         

    def seleccionarProductos(self,event):
        #Función para tomar los datos seleccionados en la tabla
        try:
            #Limpiamos el entry
            self.etNombreProducto.delete(0,'end')

            #Inicializamos las variables
            self.productoId = None
            self.nombreProducto  = None

            #Selección de datos desde el la tabla 
            self.productoId = self.twConsultarProductos.item(self.twConsultarProductos.selection())['text']
            self.nombreProducto = self.twConsultarProductos.item(self.twConsultarProductos.selection())['values'][0]

            #Insertamos nuevo valor
            self.etNombreProducto.insert(0,self.nombreProducto)

        except:
            pass
