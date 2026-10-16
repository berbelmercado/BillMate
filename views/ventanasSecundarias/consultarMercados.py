from tkinter import ttk
from PIL import Image
from customtkinter import CTkToplevel,CTkFrame,CTkLabel,CTkButton,CTkEntry,CTkComboBox,CTkScrollbar,CTkImage
from views.ventanasSecundarias import configuracionVentanasSecundarias as conSec
from views.configuracionesGenerales import dicConfiguracionGeneralColores as conColores
from views.configuracionesGenerales import dicConfiguracionGeneralFuentes as conFuentes
from views.configuracionesGenerales import dicConfig as conMaus
from views.ventanasSecundarias import consultarProductos as conPro
from views.ventanasSecundarias import consultarFacturas as conFacturas
from views.ventanasSecundarias import consultarComercios as conCom
from views.ventanasSecundarias import consultarCompras as conComp
from views.frameTotal import WidgetsDatos
from views.messagebox import mensajesEmergentes as msbx
from controller import mercadosController
from views.vwImgConfig import  leerImagen
from views.frameListasTreview import avisarDatosCambiados

class ConsultarMercados(CTkToplevel):

    def __init__(self,master):
        super().__init__(master)
        self.master=master
        self.geometry(f"{conSec.dicConfigConsultarMercado["vpConsultarMercadoWidth"]}x{conSec.dicConfigConsultarMercado["vpConsultarMercadoHeight"]}+{conSec.dicConfigPosicion["vnConsultarMercadosX"]}+{conSec.dicConfigPosicion["vnConsultarMercadosY"]}")
        self._fg_color= conColores['bgGeneral']
        self.title("Consultas")
        self.imagenConsultar = CTkImage(dark_image=Image.open(leerImagen("Consultar")),size=(28,28))
        self.imagenCancelar = CTkImage(dark_image=Image.open(leerImagen("Cancelar")),size=(28,28))
        self.imagenActualizar = CTkImage(dark_image=Image.open(leerImagen("Actualizar")),size=(28,28))
        self.imagenEliminar = CTkImage(dark_image=Image.open(leerImagen("Eliminar")),size=(28,28))
        self.imagenAgregar=CTkImage(dark_image=Image.open(leerImagen("Agregar")),size=(28,28))
        self.imagenCargar = CTkImage(dark_image =Image.open(leerImagen("cargar")),size=(28,28))
        self.resizable(False,False)
        self.transient(master)
        self.lift()
        self.fmGlobal()
        self.buscarProducto()
        self.fmCargaItems()
        self.modificaciones()
        self.twConsultarProducto()
        self.definiciónVariables()

    def fmGlobal(self):
        self.frmGlobal=CTkFrame(self
                                ,fg_color=conColores['bgGeneral']
                                ,width=1270
                                ,height=610
                                )
        self.frmGlobal.place(x=0
                            ,y=0)

    def definiciónVariables(self):
        #Definimos variables para que sean reconocidas en otras funciones
        self.compraId = None
        self.idFactura = None
        self.idProducto = None
        self.comercioId = None
    
    def btnCancelar(self):
        #Funcionalidad botóon cancelar
        self.destroy()

    def fnOpcionesBusqueda(self, seleleccion):
        #Función que captura la selección del combobox
        
        #Validación de opciones
        if seleleccion == 'Nombre del Producto':
            self.opcion = 0

        elif seleleccion == 'Número de Factura':
            self.opcion = 1
            
        elif seleleccion == 'Descripción Mercado':
            self.opcion = 2
        else:
            self.opcion = 10
        
    def capturarDatos(self):
        #función que captura los datos del entry 
        #inicialización de variables
        self.vrNombreProducto = None
        self.vrNumeroFactura = None
        self.vrDescCompra = None 
        
        try:
            if self.opcion == 0:
                self.vrNombreProducto = self.etIngresoDatos.get()
            elif self.opcion == 1:
                self.vrNumeroFactura = self.etIngresoDatos.get()
            elif self.opcion == 2:
                self.vrDescCompra = self.etIngresoDatos.get()
        except:
            self.opcion = None


    def eventConsultas(self,event):
        #Evento para consultar con cada letra que se ingrese en el entry
        try:
            self.fnConsultas()
        except:
            pass
    
    def limpiarentrys(self):
        #Función para limpiar los entrys antes de mostrar un producto seleccionado

        #limpiamos entry nombre producto
        self.etNombreProducto.configure(state = 'normal')# Habilitamos el entry 
        self.etNombreProducto.delete(0,'end') #Borramos información
        self.etNombreProducto.configure(state = 'disabled')#Deshabilitamos entry 
        
        self.etCantidadProducto.delete(0,'end')
        self.etPrecioUnidadProducto.delete (0,'end')
        self.etPrecioTotalProducto.delete(0,'end')
        #Limpiamos entry factura
        self.etNumeroFactura.configure(state = 'normal')
        self.etNumeroFactura.delete(0,'end')
        self.etNumeroFactura.configure(state = 'disabled')

        #Limpiamos entry comercio
        self.etNombreComercio.configure(state = 'normal')
        self.etNombreComercio.delete(0,'end')
        self.etNombreComercio.configure(state = 'disabled')

        #Limpiamos entry Mercado
        self.etDescMercado.configure(state = 'normal')
        self.etDescMercado.delete(0,'end')
        self.etDescMercado.configure(state = 'disabled')
    


    def fnConsultas(self):
        #Función para realizar consultas a la base de datos
        self.capturarDatos() #capturamos el dato según nuestra elección
        #instanciamos la clase
        try:
            self.listaProductos, mensaje = mercadosController.consultarMercados(self.opcion, self.etIngresoDatos.get())
            
            if mensaje[0]==1:
                for i in self.twConsultarProductos.get_children():
                    self.twConsultarProductos.delete(i)
                #Insertamos la información en el treeview
                for i in self.listaProductos:
                    self.twConsultarProductos.insert(""
                                                    ,"end"
                                                    ,text=i[0]
                                                    ,values=(i[1]
                                                            ,i[2]
                                                            ,i[3]
                                                            ,i[4]
                                                            ,i[5]
                                                            ,i[6]
                                                            ,i[7]
                                                            ,i[8]
                                                            )
                                                    ,tags ='evenrow'
                                                    )
            if mensaje[0]==0:
                msbx.mensajeError(mensaje[1])

            WidgetsDatos(self,conSec.dicConfigConsultarMercado["fmDatosX"],conSec.dicConfigConsultarMercado["fmDatosY"],self.listaProductos)#Calcula el total y cantidad de productos agregados
        except:
            pass
    

    def execAgregarProductos(self):
        #Función para ingresar un producto a lavista mercado desde la vista de consulta de productos
        self.objConsultarProductos = conPro.ConsultarProductos(self)
        
        def fnfnImportarDatosProductos():

            self.idProducto = int(self.objConsultarProductos.productoId)

            self.etNombreProducto.configure(state='normal')
            self.etNombreProducto.delete(0,'end')
            self.etNombreProducto.insert (0,self.objConsultarProductos.etNombreProducto.get())
            self.etNombreProducto.configure(state='disabled')
            self.objConsultarProductos.destroy()


        #Cargar producto a vista mercado
        self.btnCargarProducto=CTkButton(self.objConsultarProductos.fmFrameModificacionProducto
                                            ,text=' Cargar Producto '
                                            ,fg_color=conColores["bgBotones"]
                                            ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                            #,text_color=conColor["ColorLetras"]
                                            ,command=fnfnImportarDatosProductos
                                            ,image=self.imagenCargar
                                            ,cursor=conMaus["cursor"]
                                            ,compound=conMaus["compound"]
                                            ,width=conSec.dicConfigConsultarProducto["btGuardarCambioItemWidht"]
                                            ,height=conSec.dicConfigConsultarProducto["btGuardarCambioItemHeight"]
                                            )
        self.btnCargarProducto.grid(column=0
                                        ,row=3
                                        ,padx=conSec.dicConfigConsultarProducto["padXFmModificaciones"]
                                        ,pady=conSec.dicConfigConsultarProducto["padXFmModificaciones"]
                                        )
        
    def execAgregarFacturas(self):
        
        #declaramos objeto que muestra la ventana de consultas
        self.objConsultarFacura = conFacturas.ConsultarFacturas(self)

        def fnImportarDatosFacturas():
            #Importamos los datos desde la vista consultar facturas
            self.idFactura =None 

            self.idFactura = int(self.objConsultarFacura.vrIdFactura)
            self.numeroFactura = self.objConsultarFacura.etModificacionesNumeroFactura.get()
            
            #seteamos el número de factura en el entry para mostrarlo
            self.etNumeroFactura.configure(state='normal')
            self.etNumeroFactura.delete(0,'end')
            self.etNumeroFactura.insert(0, self.numeroFactura)
            self.etNumeroFactura.configure(state='disabled')
            self.objConsultarFacura.destroy()#se destruye la ventana

        #Creamos botón para importación de datos
        self.btnCargarFacturas=CTkButton(self.objConsultarFacura.fmFrameModificacionFactura
                                                ,text=' Cargar A Mercado'
                                                ,fg_color=conColores["bgBotones"]
                                                ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                                ,command=fnImportarDatosFacturas
                                                ,image=self.imagenCargar
                                                ,cursor=conMaus["cursor"]
                                                ,compound=conMaus["compound"]
                                                ,width=conSec.dicConfigConsultarFactura["btnCargarFacturasWidht"]
                                                ,height=conSec.dicConfigConsultarFactura["btnCargarFacturasHeight"]
                                                )
        self.btnCargarFacturas.grid(column=0
                                        ,row=8
                                        ,padx=conSec.dicConfigConsultarFactura["padX"]
                                        ,pady=conSec.dicConfigConsultarFactura["padX"]
                                        )
        
    def execAgregarComercios(self):
        #Función para agredar comercios a la vista consultar mercados desde la vista consultar comercios
        self.objConsutarComercios = conCom.ConsultarComercios(self)

        def fnImportarDatosComercios():
            #Importamos los datos desde la vista consultar comercios

            self.comercioId = int(self.objConsutarComercios.comercioId)
            self.nombreComercio = self.objConsutarComercios.nombreComercio
            self.direccionComercio = self.objConsutarComercios.direccionComercio
            
            #seteamos el número de factura en el entry para mostrarlo
            self.etNombreComercio.configure(state='normal')
            self.etNombreComercio.delete(0,'end')
            self.etNombreComercio.insert(0, self.nombreComercio)
            self.etNombreComercio.configure(state='disabled')
            self.objConsutarComercios.destroy()#se destruye la ventana
        
        #Se crea botón agregar ela vista de consulta de comercio
        self.btnCargarFacturas=CTkButton(self.objConsutarComercios.fmFrameModificacionComercio
                                                ,text=' Cargar A Mercado'
                                                ,fg_color=conColores["bgBotones"]
                                                ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                                #,text_color=conColor["ColorLetras"]
                                                ,command=fnImportarDatosComercios
                                                ,image=self.imagenCargar
                                                ,cursor=conMaus["cursor"]
                                                ,compound=conMaus["compound"]
                                                ,width=conSec.dicConfigConsultarFactura["btnCargarFacturasWidht"]
                                                ,height=conSec.dicConfigConsultarFactura["btnCargarFacturasHeight"]
                                                )
        self.btnCargarFacturas.grid(column=0
                                    ,row=6
                                    ,padx=conSec.dicConfigConsultarFactura["padX"]
                                    ,pady=conSec.dicConfigConsultarFactura["padX"]
                                    )
    def execAgregarCompras(self):
         #Función para agredar compras a la vista consultar mercados desde la vista consultar compras
        self.objConsutarCompras = conComp.ConsultarCompras(self)

        def fnImportarDatosComercios():
            #Importamos los datos desde la vista consultar compras

            self.compraId = int(self.objConsutarCompras.compraId)
            self.descripcionCompra = self.objConsutarCompras.descripcionCompra
            
            #seteamos el número de factura en el entry para mostrarlo
            self.etDescMercado.configure(state='normal')
            self.etDescMercado.delete(0, 'end')
            self.etDescMercado.insert(0, self.descripcionCompra)
            self.etDescMercado.configure(state='disabled')
            self.objConsutarCompras.destroy()#se destruye la ventana

            
        self.btnCargarFacturas=CTkButton(self.objConsutarCompras.fmFrameModificacionCompras
                                                ,text=' Cargar A Mercado'
                                                ,fg_color=conColores["bgBotones"]
                                                ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                                #,text_color=conColor["ColorLetras"]
                                                ,command=fnImportarDatosComercios
                                                ,image=self.imagenCargar
                                                ,cursor=conMaus["cursor"]
                                                ,compound=conMaus["compound"]
                                                ,width=conSec.dicConfigConsultarFactura["btnCargarFacturasWidht"]
                                                ,height=conSec.dicConfigConsultarFactura["btnCargarFacturasHeight"]
                                                )
        self.btnCargarFacturas.grid(column=0
                                    ,row=5
                                    ,padx=conSec.dicConfigConsultarFactura["padX"]
                                    ,pady=conSec.dicConfigConsultarFactura["padX"]
                                    )

    def fnActualizarProductos(self):
        #Función para actualizar datos de productos
        for i in self.listaKeys:
        #Evaluamos los campos que van a ser actualizados para insertar los datos nuevos
            if i[0] != self.compraId and self.compraId != None:
                cambioCompraId = self.compraId
            else:
                cambioCompraId = i[0]

            if i[1] != self.idFactura and self.idFactura != None:
                cambioFacturaId = self.idFactura
            else: 
                cambioFacturaId = i[1] 

            if i[2] != self.idProducto and self.idProducto != None:
                cambioProductoId = self.idProducto
            else:
                cambioProductoId = i[2]

            if i[3]!=self.comercioId and self.comercioId != None:
                cambioComercioId = self.comercioId
            else:
                cambioComercioId = i[3]
            
        mensaje = mercadosController.actualizarMercado(self.vrMercadoIdSelect
                                                       ,cambioCompraId
                                                       ,cambioFacturaId
                                                       ,cambioProductoId
                                                       ,cambioComercioId
                                                       ,self.etCantidadProducto.get()
                                                       ,self.etPrecioUnidadProducto.get()
                                                       ,self.etPrecioTotalProducto.get())
        
        if mensaje[0]==1:

            self.limpiarentrys()
            self.fnConsultas()
            avisarDatosCambiados(self)
        if mensaje[0]==0:
            msbx.mensajeError(mensaje[1])

    def fnEliminarProductos(self):
        #Función para eliminar los productos que seleccionemos en el entry
        mensaje = mercadosController.eliminarMercado(self.vrMercadoIdSelect)

        if mensaje[0]==1:
            msbx.mensajeInformativo(mensaje[1])
            self.limpiarentrys()
            self.fnConsultas()
            #La pantalla de inicio vuelve a leer la última compra
            avisarDatosCambiados(self)
        if mensaje[0]==0:
            msbx.mensajeError(mensaje[1])


    
    def fmCargaItems(self):
        #Se crean los widgeds para cargar los diferentes datos desde las vistas de consultas
        self.frameCargaItems = CTkFrame(self
                                        ,fg_color= conColores['fg_color']
                                        )
        self.frameCargaItems.place(x = 5
                                   ,y = 5)
        
        #Boton cargar productos
        self.btnCargaProductos = CTkButton(self.frameCargaItems
                                           ,text = 'Carga Producto  '
                                           ,fg_color= conColores['bgBotones']
                                           ,font = (conFuentes['Fuente'],conFuentes['tamano'])
                                           ,command=self.execAgregarProductos
                                           ,image=self.imagenAgregar
                                           ,cursor=conMaus["cursor"]
                                           ,compound=conMaus["compound"]
                                           )
        self.btnCargaProductos.grid(column = 0
                                    ,row = 0
                                    ,padx = conSec.dicConfigConsultarMercado['padXFmModificaciones']
                                    ,pady = conSec.dicConfigConsultarMercado['padyFmModificaciones']
                                    )
        
        #Boton cargar facturas
        self.btnCargaFacturas = CTkButton(self.frameCargaItems
                                           ,text = 'Cargar Facturas  '
                                           ,fg_color= conColores['bgBotones']
                                           ,font = (conFuentes['Fuente'],conFuentes['tamano'])
                                           ,command=self.execAgregarFacturas
                                           ,image=self.imagenAgregar
                                           ,cursor=conMaus["cursor"]
                                           ,compound=conMaus["compound"]
                                           )
        self.btnCargaFacturas.grid(column = 0
                                    ,row = 1
                                    ,padx = conSec.dicConfigConsultarMercado['padXFmModificaciones']
                                    ,pady = conSec.dicConfigConsultarMercado['padyFmModificaciones']
                                    )
        #Boton carga comercios
        self.btnCargaComercios = CTkButton(self.frameCargaItems
                                           ,text = 'Carga Comercios'
                                           ,fg_color= conColores['bgBotones']
                                           ,font = (conFuentes['Fuente'],conFuentes['tamano'])
                                           ,command=self.execAgregarComercios
                                           ,image=self.imagenAgregar
                                           ,cursor=conMaus["cursor"]
                                           ,compound=conMaus["compound"]
                                           )
        self.btnCargaComercios.grid(column = 0
                                    ,row = 2
                                    ,padx = conSec.dicConfigConsultarMercado['padXFmModificaciones']
                                    ,pady = conSec.dicConfigConsultarMercado['padyFmModificaciones']
                                    )
        #Boton cargar compras
        self.btnCargaProductos = CTkButton(self.frameCargaItems
                                           ,text = 'Carga Compras   '
                                           ,fg_color= conColores['bgBotones']
                                           ,font = (conFuentes['Fuente'],conFuentes['tamano'])
                                           ,command=self.execAgregarCompras
                                           ,image=self.imagenAgregar
                                           ,cursor=conMaus["cursor"]
                                           ,compound=conMaus["compound"]
                                           )
        self.btnCargaProductos.grid(column = 0
                                    ,row = 3
                                    ,padx = conSec.dicConfigConsultarMercado['padXFmModificaciones']
                                    ,pady = conSec.dicConfigConsultarMercado['padyFmModificaciones']
                                    )
    
    def buscarProducto(self):
        #se crean los widgets para realizar las busquedas
        self.fmPrincipal= CTkFrame(self
                                ,fg_color=conColores["fg_color"]
                                ,width=conSec.dicConfigConsultarMercado["fmPrincipalConsultarMercadoWidht"]
                                ,height=conSec.dicConfigConsultarMercado["fmPrincipalConsultarMercadoHeight"]
                                )
        self.fmPrincipal.pack(anchor='center',pady=5)
   
        #Combo box ingresar nombre del producto
        self.cboxIngresarDatoBusqueda = CTkComboBox(self.fmPrincipal
                                                    ,fg_color=conColores["bgLabels"]
                                                    ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                                    ,text_color=conColores["colorLetrasLabel"]
                                                    ,corner_radius=8
                                                    ,width=conSec.dicConfigConsultarMercado["cboxIngresarDatoBusquedaWidth"]
                                                    ,height=conSec.dicConfigConsultarMercado["cboxIngresarDatoBusquedaHeight"]
                                                    ,values=["Nombre del Producto"
                                                           ,"Número de Factura"
                                                           ,"Descripción Mercado"]
                                                    ,state='readonly'
                                                    ,command= self.fnOpcionesBusqueda
                                                    )   
        self.cboxIngresarDatoBusqueda.place(x=conSec.dicConfigConsultarMercado["cboxIngresarDatoBusquedaX"]
                                            ,y=conSec.dicConfigConsultarMercado["cboxIngresarDatoBusquedaY"]
                                            )
        self.cboxIngresarDatoBusqueda.set('Escoja Una Opción')
       
        
        #Entry ingresar nombre del producto
        self.etIngresoDatos = CTkEntry(self.fmPrincipal
                                                 ,fg_color=conColores["bgEntrys"]
                                                 #,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                                 ,text_color=conColores["colorLetrasEntry"]
                                                 ,justify='center'
                                                 ,corner_radius=8
                                                 ,width=conSec.dicConfigConsultarMercado["etIngresoDatosWidth"]
                                                 ,height=conSec.dicConfigConsultarMercado["etIngresoDatosHeight"]
                                                 )
        self.etIngresoDatos.place(x=conSec.dicConfigConsultarMercado["etIngresoDatosX"]
                                            ,y=conSec.dicConfigConsultarMercado["etIngresoDatosY"]
                                            )
        
        #Creamos evento para que se ejecute la busqueda cada que ingresamos una letra

        self.etIngresoDatos.bind('<Key>',self.eventConsultas)
        
        
        #Button buscar productos
        self.btBuscarProductos = CTkButton(self.fmPrincipal
                                           ,text='Buscar'
                                           ,fg_color=conColores["bgBotones"]
                                           ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                           #,text_color=conColores["ColorLetras"]
                                           ,command=self.fnConsultas
                                           ,image=self.imagenConsultar
                                           ,cursor=conMaus["cursor"]
                                           ,compound=conMaus["compound"]
                                           ,width=conSec.dicConfigConsultarMercado["btBuscarMercadosWidth"]
                                           ,height=conSec.dicConfigConsultarMercado["btBuscarMercadosHeight"]   
                                           )
        self.btBuscarProductos.place(x=conSec.dicConfigConsultarMercado["btBuscarMercadosX"]
                                     ,y=conSec.dicConfigConsultarMercado["btBuscarMercadosY"]          
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
                                           ,width=conSec.dicConfigConsultarMercado["btnCancelarConsultaWidth"]
                                           ,height=conSec.dicConfigConsultarMercado["btnCancelarConsultaHeight"]
                                           )
        self.btnCancelarConsulta.place(x=conSec.dicConfigConsultarMercado["btnCancelarConsultaX"]
                                     ,y=conSec.dicConfigConsultarMercado["btnCancelarConsultaY"]
                                     )
        
    def modificaciones(self):
        #segundo frame en la ventana
        self.fmModificaciones=CTkFrame(self
                                       ,fg_color=conColores["fg_color"])
        self.fmModificaciones.place(x=190
                                    ,y=70)

        #label Nombre Producto
        self.lbNombreProducto=CTkLabel(self.fmModificaciones
                                       ,text='Nombre Producto'
                                       ,fg_color=conColores["bgLabels"]
                                       ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                       ,text_color=conColores["colorLetrasLabel"]
                                       ,corner_radius=8
                                       ,width=conSec.dicConfigConsultarMercado["lbNombreProductoWidth"]
                                       ,height=conSec.dicConfigConsultarMercado["lbNombreProductoHeight"]
                                       )
        self.lbNombreProducto.grid(column=0
                                   ,row=0
                                   ,padx=conSec.dicConfigConsultarMercado["padXFmModificaciones"]
                                   ,pady=conSec.dicConfigConsultarMercado["padyFmModificaciones"]
                                   )

        #label Cantidad
        self.lbCantidadProducto=CTkLabel(self.fmModificaciones
                                       ,text='Cantidad'
                                       ,fg_color=conColores["bgLabels"]
                                       ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                       ,text_color=conColores["colorLetrasLabel"]
                                       ,corner_radius=8
                                       ,width=conSec.dicConfigConsultarMercado["lbCantidadProductoWidth"]
                                       ,height=conSec.dicConfigConsultarMercado["lbCantidadProductoHeight"]
                                       )
        self.lbCantidadProducto.grid(column=1
                                     ,row=0
                                     ,padx=conSec.dicConfigConsultarMercado["padXFmModificaciones"]
                                     ,pady=conSec.dicConfigConsultarMercado["padyFmModificaciones"]
                                     )

        #label precio unidad
        self.lbPrecioUnidadProducto=CTkLabel(self.fmModificaciones
                                       ,text='Precio Unidad'
                                       ,fg_color=conColores["bgLabels"]
                                       ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                       ,text_color=conColores["colorLetrasLabel"]
                                       ,corner_radius=8
                                       ,width=conSec.dicConfigConsultarMercado["lbPrecioUnidadProductoWidth"]
                                       ,height=conSec.dicConfigConsultarMercado["lbPrecioUnidadProductoHeight"]
                                       )
        self.lbPrecioUnidadProducto.grid(column=2
                                         ,row=0
                                         ,padx=conSec.dicConfigConsultarMercado["padXFmModificaciones"]
                                         ,pady=conSec.dicConfigConsultarMercado["padyFmModificaciones"]
                                        )

        #label precio total
        self.lbPrecioTotalProducto=CTkLabel(self.fmModificaciones
                                       ,text='Precio Total'
                                       ,fg_color=conColores["bgLabels"]
                                       ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                       ,text_color=conColores["colorLetrasLabel"]
                                       ,corner_radius=8
                                       ,width=conSec.dicConfigConsultarMercado["lbPrecioTotalProductoWidth"]
                                       ,height=conSec.dicConfigConsultarMercado["lbPrecioTotalProductoHeight"]
                                       )
        self.lbPrecioTotalProducto.grid(column=3
                                        ,row=0
                                        ,padx=conSec.dicConfigConsultarMercado["padXFmModificaciones"]
                                        ,pady=conSec.dicConfigConsultarMercado["padyFmModificaciones"]
                                         )

        #label Número factura
        self.lbNumeroFactura=CTkLabel(self.fmModificaciones
                                       ,text='N° Factura'
                                       ,fg_color=conColores["bgLabels"]
                                       ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                       ,text_color=conColores["colorLetrasLabel"]
                                       ,corner_radius=8
                                       ,width=conSec.dicConfigConsultarMercado["lbNumeroFacturaWidth"]
                                       ,height=conSec.dicConfigConsultarMercado["lbNumeroFacturaHeight"]
                                       )
        self.lbNumeroFactura.grid(column=4
                                  ,row=0
                                  ,padx=conSec.dicConfigConsultarMercado["padXFmModificaciones"]
                                  ,pady=conSec.dicConfigConsultarMercado["padyFmModificaciones"]
                                  )


        #label Nombre comercio
        self.lbNombreComercio=CTkLabel(self.fmModificaciones
                                       ,text='Nombre Comercio'
                                       ,fg_color=conColores["bgLabels"]
                                       ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                       ,text_color=conColores["colorLetrasLabel"]
                                       ,corner_radius=8
                                       ,width=conSec.dicConfigConsultarMercado["lbNombreComercioWidth"]
                                       ,height=conSec.dicConfigConsultarMercado["lbNombreComercioHeight"]
                                       )
        self.lbNombreComercio.grid(column=6
                                   ,row=0
                                   ,padx=conSec.dicConfigConsultarMercado["padXFmModificaciones"]
                                   ,pady=conSec.dicConfigConsultarMercado["padyFmModificaciones"]
                                   )

        #label Descripcion Mercado
        self.lbDescMercado=CTkLabel(self.fmModificaciones
                                       ,text='Desc. Mercado'
                                       ,fg_color=conColores["bgLabels"]
                                       ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                       ,text_color=conColores["colorLetrasLabel"]
                                       ,corner_radius=8
                                       ,width=conSec.dicConfigConsultarMercado["lbDescMercadoWidth"]
                                       ,height=conSec.dicConfigConsultarMercado["lbDescMercadoHeight"]
                                       )
        self.lbDescMercado.grid(column=7
                              ,row=0
                              ,padx=conSec.dicConfigConsultarMercado["padXFmModificaciones"]
                              ,pady=conSec.dicConfigConsultarMercado["padyFmModificaciones"]
                              )
  
        #Entry Nombre Producto
        self.etNombreProducto= CTkEntry(self.fmModificaciones
                                        ,fg_color=conColores["bgEntrys"]
                                        ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                        ,text_color=conColores["colorLetrasLabel"]
                                        ,corner_radius=8
                                        ,justify='center'
                                        ,width=conSec.dicConfigConsultarMercado["etNombreProductoWidth"]
                                        ,height=conSec.dicConfigConsultarMercado["etNombreProductoHeight"]
                                        ,state='disabled'
                                        )
        self.etNombreProducto.grid(column=0
                                   ,row=1
                                   ,pady=7
                                   ,padx=7
                                   )
        #entry Cantidad
        self.etCantidadProducto= CTkEntry(self.fmModificaciones
                                        ,fg_color=conColores["bgEntrys"]
                                        ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                        ,text_color=conColores["colorLetrasLabel"]
                                        ,corner_radius=8
                                        ,justify='center'
                                        ,width=conSec.dicConfigConsultarMercado["etCantidadProductoWidth"]
                                        ,height=conSec.dicConfigConsultarMercado["etCantidadProductoHeight"]
                                        )
        self.etCantidadProducto.grid(column=1
                                   ,row=1
                                   ,pady=6
                                   ,padx=7
                                   )
        
        # #entry precio unidad
        self.etPrecioUnidadProducto= CTkEntry(self.fmModificaciones
                                        ,fg_color=conColores["bgEntrys"]
                                        ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                        ,text_color=conColores["colorLetrasLabel"]
                                        ,corner_radius=8
                                        ,justify='center'
                                        ,width=conSec.dicConfigConsultarMercado["etPrecioUnidadProductoWidth"]
                                       ,height=conSec.dicConfigConsultarMercado["etPrecioUnidadProductoHeight"]
                                        )
        self.etPrecioUnidadProducto.grid(column=2
                                   ,row=1
                                   ,padx=conSec.dicConfigConsultarMercado["padXFmModificaciones"]
                                   ,pady=conSec.dicConfigConsultarMercado["padyFmModificaciones"]
                                   )

        # #Entry precio Total
        self.etPrecioTotalProducto= CTkEntry(self.fmModificaciones
                                        ,fg_color=conColores["bgEntrys"]
                                        ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                        ,text_color=conColores["colorLetrasLabel"]
                                        ,corner_radius=8
                                        ,justify='center'
                                        ,width=conSec.dicConfigConsultarMercado["lbPrecioUnidadProductoWidth"]
                                        ,height=conSec.dicConfigConsultarMercado["lbPrecioUnidadProductoHeight"]
                                        )
        self.etPrecioTotalProducto.grid(column=3
                                   ,row=1
                                   ,padx=conSec.dicConfigConsultarMercado["padXFmModificaciones"]
                                   ,pady=conSec.dicConfigConsultarMercado["padyFmModificaciones"]
                                   )
        
        #Entry Numero factura
        self.etNumeroFactura= CTkEntry(self.fmModificaciones
                                        ,fg_color=conColores["bgEntrys"]
                                        ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                        ,text_color=conColores["colorLetrasLabel"]
                                        ,corner_radius=8
                                        ,justify='center'
                                        ,width=conSec.dicConfigConsultarMercado["etNumeroFacturaWidth"]
                                        ,height=conSec.dicConfigConsultarMercado["etNumeroFacturaHeight"]
                                        ,state='disabled'
                                        )
        self.etNumeroFactura.grid(column=4
                                   ,row=1
                                   ,padx=conSec.dicConfigConsultarMercado["padXFmModificaciones"]
                                   ,pady=conSec.dicConfigConsultarMercado["padyFmModificaciones"]
                                   )

        #Entry Nombre Comercio
        self.etNombreComercio= CTkEntry(self.fmModificaciones
                                        ,fg_color=conColores["bgEntrys"]
                                        ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                        ,text_color=conColores["colorLetrasLabel"]
                                        ,corner_radius=8
                                        ,justify='center'
                                        ,width=conSec.dicConfigConsultarMercado["etNombreComercioWidth"]
                                        ,height=conSec.dicConfigConsultarMercado["etNombreComercioHeight"]
                                        ,state='disabled'
                                        )
        self.etNombreComercio.grid(column=6
                                   ,row=1
                                   ,padx=conSec.dicConfigConsultarMercado["padXFmModificaciones"]
                                   ,pady=conSec.dicConfigConsultarMercado["padyFmModificaciones"]
                                   )
        #Entry descripcion mercado
        self.etDescMercado= CTkEntry(self.fmModificaciones
                                        ,fg_color=conColores["bgEntrys"]
                                        ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                        ,text_color=conColores["colorLetrasLabel"]
                                        ,corner_radius=8
                                        ,justify='center'
                                        ,width=conSec.dicConfigConsultarMercado["etDescMercadoWidth"]
                                        ,height=conSec.dicConfigConsultarMercado["etDescMercadoHeight"]
                                        ,state='disabled'
                                        )
        self.etDescMercado.grid(column=7
                                   ,row=1
                                   ,padx=conSec.dicConfigConsultarMercado["padXFmModificaciones"]
                                   ,pady=conSec.dicConfigConsultarMercado["padyFmModificaciones"]
                                   )

        self.btnActualizarDatosItem=CTkButton(self.fmModificaciones
                                            ,text=' Actualizar Cambio'
                                            ,fg_color=conColores["bgBotones"]
                                            ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                            #,text_color=conColor["ColorLetras"]
                                            ,command=self.fnActualizarProductos
                                            ,image=self.imagenActualizar
                                            ,cursor=conMaus["cursor"]
                                            ,compound=conMaus["compound"]
                                            ,width=conSec.dicConfigConsultarMercado["btnActualizarDatosItemWidth"]
                                            ,height=conSec.dicConfigConsultarMercado["btnActualizarDatosItemHeight"]
                                            )
        self.btnActualizarDatosItem.grid(column=0
                                       ,row=2
                                       ,padx=conSec.dicConfigConsultarMercado["padXFmModificaciones"]
                                       ,pady=conSec.dicConfigConsultarMercado["padyFmModificaciones"]
                                        )
        self.btnEliminarProductos= CTkButton(self.fmModificaciones
                                            ,text=' Eliminar Producto'
                                            #,bg=conColor["bgBotones"]
                                            ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                            #,fg=conColor["ColorLetras"]
                                            ,command= self.fnEliminarProductos
                                            ,image=self.imagenEliminar
                                            ,cursor=conMaus["cursor"]
                                            ,compound=conMaus["compound"]
                                            ,width=conSec.dicConfigConsultarMercado["btnEliminarProductosWidth"]
                                            ,height=conSec.dicConfigConsultarMercado["btnEliminarProductosHeight"]
                                            )
        self.btnEliminarProductos.place(x=conSec.dicConfigConsultarMercado["btnEliminarProductosX"]
                                        ,y=conSec.dicConfigConsultarMercado["btnEliminarProductosY"]
                                       )
   

    def twConsultarProducto(self):
       #creación frame para treeview
       self.fmTreviewConsultarProductos= CTkFrame(self 
                                                  ,fg_color=conColores["fg_color"]
                                                  ,corner_radius=8
                                                  #,width=conSec.dicConfigConsultarMercado["fmTreviewConsultarMercadosWidth"]
                                                  #,height=conSec.dicConfigConsultarMercado["fmTreviewConsultarMercadosHeight"]
                                                 )
       self.fmTreviewConsultarProductos.place(x = 130,y = 210)
                                        
       self.lbResultadoBusqueda = CTkLabel(self.fmTreviewConsultarProductos
                                           ,text='Resultado de Busqueda'
                                           ,fg_color=conColores["bgLabels"]
                                           ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                           ,text_color=conColores["colorLetrasLabel"]
                                           ,corner_radius=8
                                           )
       self.lbResultadoBusqueda.pack(anchor=conSec.dicConfigConsultarMercado["lbResultadoBusquedaAnchor"]
                                     ,pady=conSec.dicConfigConsultarMercado["lbResultadoBusquedaPady"])
       #creación de treview para resultados de productos buscados
       self.twConsultarProductos = ttk.Treeview(self.fmTreviewConsultarProductos
                                                ,style='Treeview'
                                                ,columns=('Producto'
                                                         ,'cantidad'
                                                         ,'precioUnidad'
                                                         ,'precioTotal'
                                                         ,'numeroFactura'
                                                         ,'fechaFactura'
                                                         ,'comercio'
                                                         ,'descMercado'                                                         
                                                        )
                                                )
       #Configuración para las filas seleccionadas
       self.twConsultarProductos.tag_configure('evenrow'
                                                ,background=conColores["bgGeneral"]
                                                ,foreground=conColores["ColorLetras"]
                                                )
       
       # #Indicamos el titulo de las columnas
       self.twConsultarProductos.heading("#0", text='Id',)
       self.twConsultarProductos.heading("#1", text='Producto',)
       self.twConsultarProductos.heading("#2", text='Cantidad',)
       self.twConsultarProductos.heading("#3", text='Precio Unidad',) 
       self.twConsultarProductos.heading("#4", text='Precio Total',)
       self.twConsultarProductos.heading("#5", text='Numero de Factura',)
       self.twConsultarProductos.heading("#6", text='Fecha Factura',)
       self.twConsultarProductos.heading("#7", text='Comercio',)
       self.twConsultarProductos.heading("#8", text='Desc. Mercado',)
       
        
       # #configuramos las columnas
       self.twConsultarProductos.column("#0",width=50, anchor='center',)
       self.twConsultarProductos.column("#1",width=160, anchor='center',)
       self.twConsultarProductos.column("#2",width=60,  anchor='center')
       self.twConsultarProductos.column("#3",width=90, anchor='center')
       self.twConsultarProductos.column("#4",width=85, anchor='center')
       self.twConsultarProductos.column("#5",width=120, anchor='center')
       self.twConsultarProductos.column("#6",width=100, anchor='center')
       self.twConsultarProductos.column("#7",width=160, anchor='center')
       self.twConsultarProductos.column("#8",width=100, anchor='center')
       
       self.twConsultarProductos.pack(side='left',fill='y', expand=True)

       self.scrollBarr=CTkScrollbar(self.fmTreviewConsultarProductos
                #,hover=True
                ,command=self.twConsultarProductos.yview
                ,orientation='vertical'
                ,bg_color=conColores["bgLabels"]
                ,button_color=conColores["fg_color"]
                )
       self.scrollBarr.pack(side='right', fill="y")

       self.twConsultarProductos.configure(yscrollcommand=self.scrollBarr.set)

       #Evento para selección de filas en treview
       self.twConsultarProductos.bind('<<TreeviewSelect>>',self.seleccionarProductos)

    def consultarLaves(self, mercadoId):
        #Función que sonsulta las llaves para permitir la acutualización de los productos

        self.listaKeys, mensaje = mercadosController.consultarLlavesMercado(mercadoId)
        if mensaje[0]==0:
            msbx.mensajeError(mensaje[1])


    def seleccionarProductos(self,event):
        try:
            #Limpiamos el entry
            self.limpiarentrys()

            #Inicializamos las variables
            self.vrMercadoIdSelect = None
            self.vrNombreProductoSelect = None
            self.vrCantidadSelect = None
            self.vrPrecioUnidadSelect = None
            self.vrPrecioTotalSelect = None
            self.vrNumeroFacturaSelect = None
            self.vrNombreComercioSelect = None
            self.vrDescMercadoSelect = None
            
            #Capturamos los datos de cada columna
            self.vrMercadoIdSelect = self.twConsultarProductos.item(self.twConsultarProductos.selection())['text']
            self.vrNombreProductoSelect = self.twConsultarProductos.item(self.twConsultarProductos.selection())['values'][0]
            self.vrCantidadSelect = self.twConsultarProductos.item(self.twConsultarProductos.selection())['values'][1]
            self.vrPrecioUnidadSelect = self.twConsultarProductos.item(self.twConsultarProductos.selection())['values'][2]
            self.vrPrecioTotalSelect = self.twConsultarProductos.item(self.twConsultarProductos.selection())['values'][3]
            self.vrNumeroFactura = self.twConsultarProductos.item(self.twConsultarProductos.selection())['values'][4]
            self.vrNombreComercioSelect = self.twConsultarProductos.item(self.twConsultarProductos.selection())['values'][6]
            self.vrDescMercadoSelect = self.twConsultarProductos.item(self.twConsultarProductos.selection())['values'][7]

            #Consultamos las keys
            self.consultarLaves(int(self.vrMercadoIdSelect))

            #Insertamos nombre de produco al entry
            self.etNombreProducto.configure(state = 'normal')
            self.etNombreProducto.insert(0,self.vrNombreProductoSelect)
            self.etNombreProducto.configure(state = 'disabled')

            #insertamos cantidad a entry
            self.etCantidadProducto.insert(0,self.vrCantidadSelect)
            self.etPrecioUnidadProducto.insert(0,self.vrPrecioUnidadSelect)#Precio unidad
            self.etPrecioTotalProducto.insert(0, self.vrPrecioTotalSelect) #Precio unidad
            
            #Insertamos numero de factura en entry
            self.etNumeroFactura.configure(state = 'normal')
            self.etNumeroFactura.insert(0,self.vrNumeroFactura)
            self.etNumeroFactura.configure(state = 'disabled')

            #Insertamos nombre comercio a entry
            self.etNombreComercio.configure(state = 'normal')
            self.etNombreComercio.insert(0,self.vrNombreComercioSelect)
            self.etNombreComercio.configure(state='disabled')

            #Insertamos descripción compra en entry
            self.etDescMercado.configure(state = 'normal')
            self.etDescMercado.insert(0,self.vrDescMercadoSelect)
            self.etDescMercado.configure(state = 'disabled')

        except:
            pass
            
            
            