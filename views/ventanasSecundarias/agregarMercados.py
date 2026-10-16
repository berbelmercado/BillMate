"""Modulo para crear la ventana de agregar mercados"""
from tkinter import ttk,IntVar
from PIL import Image
from customtkinter import CTkToplevel,CTkFrame,CTkButton,CTkLabel,CTkEntry,CTkCheckBox,CTkImage,CTkScrollbar
from views.ventanasSecundarias import configuracionVentanasSecundarias as conSec
from views.ventanasSecundarias.configuracionVentanasSecundarias import dicConfigConsultarFactura as conFactu
from views.configuracionesGenerales import dicConfiguracionGeneralColores as conColor
from views.configuracionesGenerales import dicConfiguracionGeneralFuentes as conFuente
from views.configuracionesGenerales import dicConfig as conMaus
from views.ventanasSecundarias import consultarProductos as conPro
from views.ventanasSecundarias import consultarFacturas as conFacturas
from views.ventanasSecundarias import consultarComercios as conCom
from views.ventanasSecundarias import consultarCompras as conComp
from views.frameTotal import WidgetsDatos
from controller.mercadoTempController import MercadoTempController
from controller.mercadoTempController import fnCargarCompraController
from controller.validaciones import convertirNumero, formatearNumero
from views.messagebox import mensajesEmergentes as mss
from views.vwImgConfig import leerImagen
from views.frameListasTreview import TreviewUltimoMercado

class AgregarMercados(CTkToplevel):
    """
    Clase para crear la ventana de agregar mercados
    Esta clase hereda de CTkToplevel y se encarga de crear la ventana
    """
    #Crea la ventana secundaria donde se ingresarán los mercados
    def __init__(self,master):
        super().__init__(master)
        self.master=master
        self.geometry(f"{conSec.dicConfigAgregarMercado["vpWidth"]}x{conSec.dicConfigAgregarMercado["vpHeight"]}+{conSec.dicConfigPosicion["vnagregarMercadoX"]}+{conSec.dicConfigPosicion["vnagregarMercadoY"]}")
        self.imagenGuardar=CTkImage(dark_image=Image.open(leerImagen("Guardar")),size=(28,28))
        self.imagenCancelar=CTkImage(dark_image=Image.open(leerImagen("Cancelar")),size=(28,28))
        self.imagenAgregar=CTkImage(dark_image=Image.open(leerImagen("Agregar")),size=(28,28))
        self.imagenEliminar=CTkImage(dark_image=Image.open(leerImagen("Eliminar")),size=(28,28))
        self.imagenActualizar=CTkImage(dark_image=Image.open(leerImagen("Actualizar")),size=(28,28))
        self.imagenLimpiar=CTkImage(dark_image=Image.open(leerImagen("Limpiar")),size=(28,28))
        self.imagenCargar = CTkImage(dark_image =Image.open(leerImagen("cargar")),size=(28,28))
        self.title("Agregar Mercados")
        self.resizable(False,False)
        self.transient(master)
        self.lift()
        self.crearWidget()
        self.productosAgregados()
        self.definiciónVariables()
        self.obj_frame_total = WidgetsDatos(self.FramePrincipal,conSec.dicConfigAgregarMercado["fmDatosX"],conSec.dicConfigAgregarMercado["fmDatosY"],self.listaProductos)#Calcula el total y cantidad de productos agregados

    def definiciónVariables(self):
        self.compraId = None
        self.idFactura = None
        self.idProducto = None
        self.comercioId = None

    def fnLimpiar(self):
        entrys = [
            self.etCantidadProducto
            ,self.etPrecioUnidad
            ,self.etPrecioTotal
        ]

        entrysNoDelete = [
            self.etNombreProducto
            ,self.etNumeroFactura
            ,self.etNombreComercio
            ,self.etDescribcionMercado
        ]

        for i in entrys:
            i.delete(0,'end')
            if i==self.etCantidadProducto:
                i.insert(0,'1')
           
        for y in entrysNoDelete:

            if self.varFijarFactura.get()==0 and self.varFijarCompra.get()==0 and self.varFijarComercio.get()==0:
                y.configure(state='normal')
                y.delete(0,'end')
                y.configure(state='disabled')
            if self.varFijarFactura.get()==1 and self.varFijarCompra.get()==0 and self.varFijarComercio.get()==0:
                if y==self.etNumeroFactura:
                    pass
                else:
                    y.configure(state='normal')
                    y.delete(0,'end')
                    y.configure(state='disabled')

            if self.varFijarFactura.get()==0 and self.varFijarCompra.get()==1 and self.varFijarComercio.get()==0:
                if y==self.etDescribcionMercado:
                    pass
                else:
                    y.configure(state='normal')
                    y.delete(0,'end')
                    y.configure(state='disabled')
            
            if self.varFijarFactura.get()==0 and self.varFijarCompra.get()==0 and self.varFijarComercio.get()==1:
                if y==self.etNombreComercio:
                    pass
                else:
                    y.configure(state='normal')
                    y.delete(0,'end')
                    y.configure(state='disabled')

    def execEditarProductos(self):
        #Funcionalidad para el botón actualizar cambio
        for i in self.listaLlaves:
        #Evaluamos los campos que van a ser actualizados
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
        
        objEditarProductos = MercadoTempController(self.vrIdeMercadoTemp
                                                   ,cambioCompraId
                                                   ,cambioFacturaId
                                                   ,cambioProductoId
                                                   ,cambioComercioId
                                                   ,self.etCantidadProducto.get()
                                                   ,self.etPrecioUnidad.get()
                                                   ,self.etPrecioTotal.get() 
                                                   )

        mensaje = objEditarProductos.actualizarProductosController()
        
        if mensaje[0]==1:
            #Modificamos los checks buttons para que se limpien todos los campos 
            self.obj_frame_total.destruirFrameTotal()
            self.cbFijarFactura.deselect()
            self.cbFijarCompra.deselect()
            self.cbNFijarComercio.deselect()
            self.fnLimpiar()
            self.productosAgregados()
            self.obj_frame_total = WidgetsDatos(self.FramePrincipal,conSec.dicConfigAgregarMercado["fmDatosX"],conSec.dicConfigAgregarMercado["fmDatosY"],self.listaProductos)#Calcula el total y cantidad de productos agregados
        
        if mensaje[0]==0:
            mss.mensajeError(mensaje[1])


    def execAgregarProductos(self):
        self.objConsultarProductos = conPro.ConsultarProductos(self)
        self.objConsultarProductos.grab_set()  # Da el foco a la ventana

        def fnfnImportarDatosProductos():
            self.idProducto = int(self.objConsultarProductos.productoId)

            self.etNombreProducto.configure(state='normal')
            self.etNombreProducto.delete(0,'end')
            self.etNombreProducto.insert (0,self.objConsultarProductos.etNombreProducto.get())
            self.etNombreProducto.configure(state='disabled')
            # self.grab_set()
            # self.focus()
            self.objConsultarProductos.destroy()


        #Cargar producto a vista mercado
        self.btnCargarProducto=CTkButton(self.objConsultarProductos.fmFrameModificacionProducto
                                            ,text=' Cargar Producto '
                                            ,fg_color=conColor["bgBotones"]
                                            ,font=(conFuente["Fuente"],conFuente["tamano"])
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
        WidgetsDatos(self.FramePrincipal,conSec.dicConfigAgregarMercado["fmDatosX"],conSec.dicConfigAgregarMercado["fmDatosY"],self.listaProductos)

    def execAgregarFacturas(self):
        
        #declaramos objeto que muestra la ventana de consultas
        self.objConsultarFacura = conFacturas.ConsultarFacturas(self)
        self.objConsultarFacura.grab_set()

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
            self.focus()
            self.objConsultarFacura.destroy()#se destruye la ventana

        #Creamos botón para importación de datos
        self.btnCargarFacturas=CTkButton(self.objConsultarFacura.fmFrameModificacionFactura
                                                ,text=' Cargar A Mercado'
                                                ,fg_color=conColor["bgBotones"]
                                                ,font=(conFuente["Fuente"],conFuente["tamano"])
                                                #,text_color=conColor["ColorLetras"]
                                                ,command=fnImportarDatosFacturas
                                                ,image=self.imagenCargar
                                                ,cursor=conMaus["cursor"]
                                                ,compound=conMaus["compound"]
                                                ,width=conFactu["btnCargarFacturasWidht"]
                                                ,height=conFactu["btnCargarFacturasHeight"]
                                                )
        self.btnCargarFacturas.grid(column=0
                                        ,row=8
                                        ,padx=conFactu["padX"]
                                        ,pady=conFactu["padX"]
                                        )



    def execAgregarComercios(self):
        self.objConsutarComercios = conCom.ConsultarComercios(self)
        self.objConsutarComercios.grab_set()

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
            self.focus()
            self.objConsutarComercios.destroy()#se destruye la ventana

        self.btnCargarFacturas=CTkButton(self.objConsutarComercios.fmFrameModificacionComercio
                                                ,text=' Cargar A Mercado'
                                                ,fg_color=conColor["bgBotones"]
                                                ,font=(conFuente["Fuente"],conFuente["tamano"])
                                                #,text_color=conColor["ColorLetras"]
                                                ,command=fnImportarDatosComercios
                                                ,image=self.imagenCargar
                                                ,cursor=conMaus["cursor"]
                                                ,compound=conMaus["compound"]
                                                ,width=conFactu["btnCargarFacturasWidht"]
                                                ,height=conFactu["btnCargarFacturasHeight"]
                                                )
        self.btnCargarFacturas.grid(column=0
                                    ,row=6
                                    ,padx=conFactu["padX"]
                                    ,pady=conFactu["padX"]
                                    )
        
    def execAgregarCompras(self):
       
        self.objConsutarCompras = conComp.ConsultarCompras(self)
        self.objConsutarCompras.grab_set()

        def fnImportarDatosComercios():
            #Importamos los datos desde la vista consultar compras

            self.compraId = int(self.objConsutarCompras.compraId)
            self.describcionCompra = self.objConsutarCompras.describcionCompra
            
            #seteamos el número de factura en el entry para mostrarlo
            self.etDescribcionMercado.configure(state='normal')
            self.etDescribcionMercado.delete(0, 'end')
            self.etDescribcionMercado.insert(0, self.describcionCompra)
            self.etDescribcionMercado.configure(state='disabled')
            # self.grab_set()
            # self.focus()
            self.objConsutarCompras.destroy()#se destruye la ventana

        self.btnCargarFacturas=CTkButton(self.objConsutarCompras.fmFrameModificacionCompras
                                                ,text=' Cargar A Mercado'
                                                ,fg_color=conColor["bgBotones"]
                                                ,font=(conFuente["Fuente"],conFuente["tamano"])
                                                #,text_color=conColor["ColorLetras"]
                                                ,command=fnImportarDatosComercios
                                                ,image=self.imagenCargar
                                                ,cursor=conMaus["cursor"]
                                                ,compound=conMaus["compound"]
                                                ,width=conFactu["btnCargarFacturasWidht"]
                                                ,height=conFactu["btnCargarFacturasHeight"]
                                                )
        self.btnCargarFacturas.grid(column=0
                                    ,row=5
                                    ,padx=conFactu["padX"]
                                    ,pady=conFactu["padX"]
                                    )


    def execInsertarProductos(self):
        #Agrega la compra a tabla mercado temporal
        
        mensaje= []
        #print(f"compra {self.compraId} \n Factura {self.idFactura} \n producto {self.idProducto} \n comercio {self.comercioId}")
        objInsertarProducto = MercadoTempController(None
                                                    ,self.compraId
                                                    ,self.idFactura
                                                    ,self.idProducto
                                                    ,self.comercioId
                                                    ,self.etCantidadProducto.get()
                                                    ,self.etPrecioUnidad.get()
                                                    ,self.etPrecioTotal.get()
                                                    )
        mensaje = objInsertarProducto.insertarMercadosTempController()

        if mensaje[0]==1:
            self.obj_frame_total.destruirFrameTotal()
            self.fnLimpiar()
            self.productosAgregados()
            self.obj_frame_total = WidgetsDatos(self.FramePrincipal,conSec.dicConfigAgregarMercado["fmDatosX"],conSec.dicConfigAgregarMercado["fmDatosY"],self.listaProductos)#Calcula el total y cantidad de productos agregados
            self.lift()
        if mensaje[0]==0:
            mss.mensajeError(mensaje[1])
    
    def eliminarProductosTbTemporal(self):
        #Elimina los productos de la tabla temporal
        objEliminarProductosTemp = MercadoTempController(self.vrIdeMercadoTemp
                                                        ,None
                                                        ,None
                                                        ,None
                                                        ,None
                                                        ,None
                                                        ,None
                                                        ,None
                                                        )
        
        mensaje = objEliminarProductosTemp.eliminarProductosTempController()


        if mensaje[0] == 0:
            mss.mensajeError(mensaje[1])
        if mensaje[0] == 1:
            self.obj_frame_total.destruirFrameTotal()
            self.fnLimpiar()
            self.productosAgregados()
            self.obj_frame_total = WidgetsDatos(self.FramePrincipal,conSec.dicConfigAgregarMercado["fmDatosX"],conSec.dicConfigAgregarMercado["fmDatosY"],self.listaProductos)#Calcula el total y cantidad de productos agregados


    def execCargarCompra(self):
        #Cargamos el consolidado de la compra en la tabla mercados
        estado = fnCargarCompraController()
        if estado[0] ==1:
            mss.mensajeInformativo(estado[1])
            self.obj_frame_total.destruirFrameTotal()
            self.fnLimpiar
            self.productosAgregados()

            #Actualizamos frame ultimo mercado en la ventana principal
            objActualizarUltimoMercado = TreviewUltimoMercado(self.master)
            objActualizarUltimoMercado.destroy()
            self.obj_frame_total = WidgetsDatos(self.FramePrincipal,conSec.dicConfigAgregarMercado["fmDatosX"],conSec.dicConfigAgregarMercado["fmDatosY"],self.listaProductos)#Calcula el total y cantidad de productos agregados
            TreviewUltimoMercado(self.master)

        if estado[0] == 0:
            mss.mensajeError(estado[1])

    def crearWidget(self):

        #Frame principal
        self.FramePrincipal = CTkFrame(self
                                       ,fg_color=conColor["bgGeneral"]
                                       ,width=1343
                                       ,height=588)
        self.FramePrincipal.place(x=0
                                  ,y=0)

        #Frame 
        self.fmMenu=CTkFrame(self.FramePrincipal
                             ,fg_color=conColor["fg_color"]
                             ,width=conSec.dicConfigAgregarMercado["fmWidht"]
                             ,height=conSec.dicConfigAgregarMercado["fmHeight"])
        self.fmMenu.place(x=conSec.dicConfigAgregarMercado["fmX"]
                         ,y=conSec.dicConfigAgregarMercado["fmY"]
                         )
        #Boton agregar producto
        self.btnAgregarProducto=CTkButton(self.fmMenu
                                          ,text='  Agregar Productos '
                                           ,fg_color=conColor["bgBotones"]
                                           ,font=(conFuente["Fuente"],conFuente["tamano"])
                                           ,command=self.execAgregarProductos
                                           ,image=self.imagenAgregar
                                           ,cursor=conMaus["cursor"]
                                           ,compound=conMaus["compound"]
                                           ,width=conSec.dicConfigAgregarMercado["btnAgregarProductosWidth"]
                                          ,height=conSec.dicConfigAgregarMercado["btnAgregarProductosHeight"])
        self.btnAgregarProducto.place(x=conSec.dicConfigAgregarMercado["btnAgregarProductosX"]
                                      ,y=conSec.dicConfigAgregarMercado["btnAgregarProductosY"]
                                      )
        #Boton agregar facturas
        self.btnAgregarFacturas=CTkButton(self.fmMenu
                                          ,text='    Agregar Facturas '
                                          ,fg_color=conColor["bgBotones"]
                                          ,font=(conFuente["Fuente"],conFuente["tamano"])
                                          #,te=conColor["ColorLetras"]
                                           #,command=self.insertarFechaEntry
                                          ,image=self.imagenAgregar
                                          ,cursor=conMaus["cursor"]
                                          ,compound=conMaus["compound"]
                                          ,command=self.execAgregarFacturas
                                          ,width=conSec.dicConfigAgregarMercado["btnAgregarFacturasWidth"]
                                          ,height=conSec.dicConfigAgregarMercado["btnAgregarFacturasHeight"])
        self.btnAgregarFacturas.place(x=conSec.dicConfigAgregarMercado["btnAgregarFacturasX"]
                                      ,y=conSec.dicConfigAgregarMercado["btnAgregarFacturasY"]
                                     )
        
        #Boton agregar comercios
        self.btnAgregarProducto=CTkButton(self.fmMenu
                                          ,text=' Agregar Comercios '
                                          ,fg_color=conColor["bgBotones"]
                                          ,font=(conFuente["Fuente"],conFuente["tamano"])
                                          #,fg=conColor["ColorLetras"]
                                          ,command=self.execAgregarComercios
                                          ,image=self.imagenAgregar
                                          ,cursor=conMaus["cursor"]
                                          ,compound=conMaus["compound"]
                                          ,width=conSec.dicConfigAgregarMercado["btnAgregarComerciosWidth"]
                                          ,height=conSec.dicConfigAgregarMercado["btnAgregarComerciossHeight"]
                                          )
        self.btnAgregarProducto.place(x=conSec.dicConfigAgregarMercado["btnAgregarComerciosX"]
                                      ,y=conSec.dicConfigAgregarMercado["btnAgregarComerciosY"]
                                     )
        #Botón agregar compras
        self.btnAgregarCompra = CTkButton(self.fmMenu
                                          ,text=' Agregar Compras   '
                                          ,fg_color=conColor["bgBotones"]
                                          ,font=(conFuente["Fuente"],conFuente["tamano"])
                                          #,fg=conColor["ColorLetras"]
                                          ,command=self.execAgregarCompras
                                          ,image=self.imagenAgregar
                                          ,cursor=conMaus["cursor"]
                                          ,compound=conMaus["compound"]
                                          ,width=conSec.dicConfigAgregarMercado["btnAgregarCompraWidth"]
                                          ,height=conSec.dicConfigAgregarMercado["btnAgregarCompraHeight"]
                                          )
        self.btnAgregarCompra.place(x=conSec.dicConfigAgregarMercado["btnAgregarCompraX"]
                                      ,y=conSec.dicConfigAgregarMercado["btnAgregarCompraY"]
                                      )
        

        #Frame Formulario
        self.fmFormulario=CTkFrame(self.FramePrincipal
                                ,fg_color=conColor['fg_color']
                                ,width=conSec.dicConfigAgregarMercado["fmFormularioWidht"]
                                ,height=conSec.dicConfigAgregarMercado["fmFormularioHeight"]
                                )
        self.fmFormulario.place(x=conSec.dicConfigAgregarMercado["fmFormularioX"]
                                ,y=conSec.dicConfigAgregarMercado["fmFormularioY"]
                                )
        #Label Nombre Producto
        self.lbNombreProducto= CTkLabel(self.fmFormulario
                                        ,text='Nombre del Producto'
                                        ,fg_color=conColor["bgLabels"]
                                        ,font=(conFuente["Fuente"],conFuente["tamano"])
                                        ,text_color=conColor["colorLetrasLabel"]
                                        ,width=conSec.dicConfigAgregarMercado["lbNombreProductoWidht"]
                                        ,height=conSec.dicConfigAgregarMercado["lbNombreProductoHeight"]
                                        ,corner_radius=8
                                        )
        self.lbNombreProducto.place(x=conSec.dicConfigAgregarMercado["lbNombreProductoX"]
                                    ,y=conSec.dicConfigAgregarMercado["lbNombreProductoY"]
                                    )
        #Entry Nombre Producto
        self.etNombreProducto= CTkEntry(self.fmFormulario
                                        ,fg_color=conColor["bgEntrys"]
                                        ,font=(conFuente["Fuente"],conFuente["tamano"])
                                        ,text_color=conColor["colorLetrasEntry"]
                                        ,justify='center'
                                        ,state="disabled"
                                        #,=conColor["bgEntrys"]                                    
                                        ,width=conSec.dicConfigAgregarMercado["etNombreProductoWidht"]
                                        ,height=conSec.dicConfigAgregarMercado["etNombreProductoHeight"]
                                        ,corner_radius=8
                                    )
        self.etNombreProducto.place(x=conSec.dicConfigAgregarMercado["etNombreProductoX"]
                                    ,y=conSec.dicConfigAgregarMercado["etNombreProductoY"]
                                    )
        #Label Cantidad Producto
        self.lbCantidadProducto= CTkLabel(self.fmFormulario
                                      ,text='Cantidad'
                                      ,fg_color=conColor["bgLabels"]
                                      ,font=(conFuente["Fuente"],conFuente["tamano"])
                                      ,text_color=conColor["colorLetrasLabel"]
                                      ,width=conSec.dicConfigAgregarMercado["lbCantidadWidht"]
                                      ,height=conSec.dicConfigAgregarMercado["lbCantidadHeight"]
                                      ,corner_radius=8
                                      )
        self.lbCantidadProducto.place(x=conSec.dicConfigAgregarMercado["lbCantidadX"]
                                    ,y=conSec.dicConfigAgregarMercado["lbCantidadY"]
                                    )
        #Entry Cantidad Producto
        self.etCantidadProducto= CTkEntry(self.fmFormulario
                                       ,fg_color=conColor["bgEntrys"]
                                       ,font=(conFuente["Fuente"],conFuente["tamano"])
                                       ,text_color=conColor["colorLetrasEntry"]
                                       ,justify='center'
                                       ,corner_radius=8
                                       ,width=conSec.dicConfigAgregarMercado["etCantidadWidht"]
                                       ,height=conSec.dicConfigAgregarMercado["etCantidadHeight"]
                                       )
        self.etCantidadProducto.place(x=conSec.dicConfigAgregarMercado["etCantidadX"]
                                    ,y=conSec.dicConfigAgregarMercado["etCantidadY"]
                                    )
        self.etCantidadProducto.insert(0,'1')
        #Label Precio Unidad
        self.lbPrecioUnidad= CTkLabel(self.fmFormulario
                                      ,text='Precio Unidad'
                                      ,fg_color=conColor["bgLabels"]
                                      ,font=(conFuente["Fuente"],conFuente["tamano"])
                                      ,text_color=conColor["colorLetrasLabel"]
                                      ,corner_radius=8
                                      ,width=conSec.dicConfigAgregarMercado["lbPrecioUnidadWidht"]
                                      ,height=conSec.dicConfigAgregarMercado["lbPrecioUnidadHeight"]
                                      )
        self.lbPrecioUnidad.place(x=conSec.dicConfigAgregarMercado["lbPrecioUnidadX"]
                                  ,y=conSec.dicConfigAgregarMercado["lbPrecioUnidadY"]
                                  )
        #Entry Precio Unidad
        self.etPrecioUnidad= CTkEntry(self.fmFormulario
                                      ,fg_color=conColor["bgEntrys"]
                                      ,font=(conFuente["Fuente"],conFuente["tamano"])
                                      ,text_color=conColor["colorLetrasEntry"] 
                                      ,justify="center"
                                      ,corner_radius=8
                                      ,width=conSec.dicConfigAgregarMercado["etPrecioUnidadWidht"]
                                      ,height=conSec.dicConfigAgregarMercado["etPrecioUnidadHeight"]
                                      )
        self.etPrecioUnidad.place(x=conSec.dicConfigAgregarMercado["etPrecioUnidadX"]
                                  ,y=conSec.dicConfigAgregarMercado["etPrecioUnidadY"]
                                  )
        
        #Label Precio Total
        self.lbPrecioTotal= CTkLabel(self.fmFormulario
                                     ,text='Precio Total'
                                     ,fg_color=conColor["bgLabels"]
                                     ,font=(conFuente["Fuente"],conFuente["tamano"])
                                     ,text_color=conColor["colorLetrasLabel"]
                                     ,corner_radius=8
                                     ,width=conSec.dicConfigAgregarMercado["lbPrecioTotalWidht"]
                                     ,height=conSec.dicConfigAgregarMercado["lbPrecioTotalHeight"]
                                     )
        self.lbPrecioTotal.place(x=conSec.dicConfigAgregarMercado["lbPrecioTotalX"]
                                 ,y=conSec.dicConfigAgregarMercado["lbPrecioTotalY"]
                                )
        #Entry Precio Total
        self.etPrecioTotal= CTkEntry(self.fmFormulario
                                     ,fg_color=conColor["bgEntrys"]
                                    ,font=(conFuente["Fuente"],conFuente["tamano"])
                                    ,text_color=conColor["colorLetrasEntry"]
                                    ,justify='center'
                                    ,corner_radius=8
                                    ,width=conSec.dicConfigAgregarMercado["etPrecioTotalWidht"]
                                    ,height=conSec.dicConfigAgregarMercado["etPrecioTotalHeight"]
                                    )
        self.etPrecioTotal.place(x=conSec.dicConfigAgregarMercado["etPrecioTotalX"]
                                ,y=conSec.dicConfigAgregarMercado["etPrecioTotalY"]
                                )
        #Entry Precio Unidad
        self.etPrecioUnidad= CTkEntry(self.fmFormulario
                                      ,fg_color=conColor["bgEntrys"]
                                      ,font=(conFuente["Fuente"],conFuente["tamano"])
                                      ,text_color=conColor["colorLetrasEntry"]
                                      ,width=conSec.dicConfigAgregarMercado["etPrecioUnidadWidht"]
                                      ,height=conSec.dicConfigAgregarMercado["etPrecioUnidadHeight"]
                                      ,corner_radius=8
                                    )
        self.etPrecioUnidad.place(x=conSec.dicConfigAgregarMercado["etPrecioUnidadX"]
                                    ,y=conSec.dicConfigAgregarMercado["etPrecioUnidadY"]
                                    )
        
        #Label numero factura
        self.lbNumeroFactura= CTkLabel(self.fmFormulario
                                     ,text='Numero de Factura'
                                     ,fg_color=conColor["bgLabels"]
                                     ,font=(conFuente["Fuente"],conFuente["tamano"])
                                     ,text_color=conColor["colorLetrasLabel"]
                                     ,corner_radius=8
                                     ,width=conSec.dicConfigAgregarMercado["lbNumeroFacturaWidht"]
                                     ,height=conSec.dicConfigAgregarMercado["lbNumeroFacturaHeight"]
                                     )
        self.lbNumeroFactura.place(x=conSec.dicConfigAgregarMercado["lbNumeroFacturalX"]
                                 ,y=conSec.dicConfigAgregarMercado["lbNumeroFacturaY"]
                                  )
        #Entry numero factura
        self.etNumeroFactura= CTkEntry(self.fmFormulario
                                  ,fg_color=conColor["bgEntrys"]
                                  ,font=(conFuente["Fuente"],conFuente["tamano"])
                                  ,text_color=conColor["colorLetrasEntry"]
                                  ,state="disabled"
                                  ,width=conSec.dicConfigAgregarMercado["etNumeroFacturaWidht"]
                                  ,height=conSec.dicConfigAgregarMercado["etNumeroFacturaHeight"]
                                  )
        self.etNumeroFactura.place(x=conSec.dicConfigAgregarMercado["etNumeroFacturaX"]
                                 ,y=conSec.dicConfigAgregarMercado["etNumeroFacturaY"]
                                 )
        
        self.varFijarFactura= IntVar()
        #Checbutton fijar factura
        self.cbFijarFactura = CTkCheckBox(self.fmFormulario
                                          ,text='Fijar Factura'
                                          ,fg_color=conColor["bgEntrys"]
                                          ,font=(conFuente["Fuente"],conFuente["tamano"])
                                          ,text_color=conColor["ColorLetras"]
                                          ,onvalue=1
                                          ,offvalue=0
                                          ,variable=self.varFijarFactura
                                          )
        self.cbFijarFactura.place(x=conSec.dicConfigAgregarMercado["cbNFijarFacturaX"]
                                 ,y=conSec.dicConfigAgregarMercado["cbNFijarFacturaY"]
                                 )
        
        self.varFijarCompra= IntVar()
        #Checbutton fijar Compra
        self.cbFijarCompra = CTkCheckBox(self.fmFormulario
                                          ,text='Fijar Compra'
                                          ,fg_color=conColor["bgEntrys"]
                                          ,font=(conFuente["Fuente"],conFuente["tamano"])
                                          ,text_color=conColor["ColorLetras"]
                                          ,onvalue=1
                                          ,offvalue=0
                                          ,variable=self.varFijarCompra
                                          )
        self.cbFijarCompra.place(x=conSec.dicConfigAgregarMercado["cbFijarCompraX"]
                                 ,y=conSec.dicConfigAgregarMercado["cbFijarCompraY"]
                                 )
        #Label comercio
        self.lbNombreComercio= CTkLabel(self.fmFormulario
                                     ,text='Comercio'
                                     ,fg_color=conColor["bgLabels"]
                                     ,font=(conFuente["Fuente"],conFuente["tamano"])
                                     ,text_color=conColor["colorLetrasLabel"]
                                     ,width=conSec.dicConfigAgregarMercado["lbComercioWidht"]
                                     ,height=conSec.dicConfigAgregarMercado["lbComercioHeight"]
                                     ,corner_radius=8
                                     )
        self.lbNombreComercio.place(x=conSec.dicConfigAgregarMercado["lbComercioX"]
                                 ,y=conSec.dicConfigAgregarMercado["lbComercioY"]
                                  )
        
        #Entry comercio
        self.etNombreComercio= CTkEntry(self.fmFormulario
                                     ,fg_color=conColor["bgEntrys"]
                                     ,font=(conFuente["Fuente"],conFuente["tamano"])
                                     ,text_color=conColor["colorLetrasEntry"]
                                     ,state="disabled"
                                     ,width=conSec.dicConfigAgregarMercado["etComercioWidht"]
                                     ,height=conSec.dicConfigAgregarMercado["etComercioHeight"]
                                     ,corner_radius=8
                                     )
        self.etNombreComercio.place(x=conSec.dicConfigAgregarMercado["etComercioX"]
                                    ,y=conSec.dicConfigAgregarMercado["etComercioY"]
                                    )
        #label descibcion mercado
        self.lbDescribcionMercado=CTkLabel(self.fmFormulario
                                           ,text='Desc. Mercado'
                                           ,fg_color=conColor["bgLabels"]
                                           ,font=(conFuente["Fuente"],conFuente["tamano"])
                                           ,text_color=conColor["colorLetrasLabel"]
                                           ,corner_radius=8
                                           ,justify="center"
                                           ,width=conSec.dicConfigAgregarMercado["lbDescribcionMercadoWidht"]
                                           ,height=conSec.dicConfigAgregarMercado["lbDescribcionMercadoHeight"]
                                           )
        self.lbDescribcionMercado.place(x=conSec.dicConfigAgregarMercado["lbDescribcionMercadoX"]
                                        ,y=conSec.dicConfigAgregarMercado["lbDescribcionMercadoY"])
        #Entry describcion mercado
        self.etDescribcionMercado=CTkEntry(self.fmFormulario
                                           ,fg_color=conColor["bgEntrys"]
                                           ,font=(conFuente["Fuente"],conFuente["tamano"])
                                           ,text_color=conColor["colorLetrasEntry"]
                                           ,justify="center"
                                           ,corner_radius=8
                                           ,width=conSec.dicConfigAgregarMercado["etDescribcionMercadoWidht"]
                                           ,height=conSec.dicConfigAgregarMercado["etDescribcionMercadoHeight"]
                                           )
        self.etDescribcionMercado.place(x=conSec.dicConfigAgregarMercado["etDescribcionMercadoX"]
                                        ,y=conSec.dicConfigAgregarMercado["etDescribcionMercadoY"])
        
        #Checbutton Fijar Comercio
        self.varFijarComercio = IntVar()
        
        self.cbNFijarComercio = CTkCheckBox(self.fmFormulario
                                          ,text='Fijar Comercio'
                                          ,fg_color=conColor["bgEntrys"]
                                          ,font=(conFuente["Fuente"],conFuente["tamano"])
                                          ,text_color=conColor["ColorLetras"]
                                          ,onvalue=1
                                          ,offvalue=0
                                          ,variable=self.varFijarComercio
                                          )
        self.cbNFijarComercio.place(x=conSec.dicConfigAgregarMercado["cbNFijarComercioX"]
                                 ,y=conSec.dicConfigAgregarMercado["cbNFijarComercioY"]
                                 )
        
        #Boton Agregar 
        self.btnAgregarItem=CTkButton(self.fmFormulario
                                      ,text='  Agregar'
                                      ,fg_color=conColor["bgBotones"]
                                      ,font=(conFuente["Fuente"],conFuente["tamano"])
                                      #,text_color=conColor["ColorLetras"]
                                      #,command=self.insertarFechaEntry
                                      ,image=self.imagenAgregar
                                      ,cursor=conMaus["cursor"]
                                      ,compound=conMaus["compound"]
                                      ,command=self.execInsertarProductos
                                      ,width=conSec.dicConfigAgregarMercado["btAgregarItemWidht"]
                                      ,height=conSec.dicConfigAgregarMercado["btAgregarItemHeight"]
                                      )
        self.btnAgregarItem.place(x=conSec.dicConfigAgregarMercado["btAgregarItemX"]
                                      ,y=conSec.dicConfigAgregarMercado["btAgregarItemY"]
                                      )
        #Boton Guardar Cambio
        self.btnAgregarCambioItem=CTkButton(self.fmFormulario
                                            ,text=' Actualizar Cambio'
                                            ,fg_color=conColor["bgBotones"]
                                            ,font=(conFuente["Fuente"],conFuente["tamano"])
                                            #,text_color=conColor["ColorLetras"]
                                            ,command=self.execEditarProductos
                                            ,image=self.imagenActualizar
                                            ,cursor=conMaus["cursor"]
                                            ,compound=conMaus["compound"]
                                            ,width=conSec.dicConfigAgregarMercado["btGuardarCambioItemWidht"]
                                            ,height=conSec.dicConfigAgregarMercado["btGuardarCambioItemHeight"]
                                            )
        self.btnAgregarCambioItem.place(x=conSec.dicConfigAgregarMercado["btGuardarCambioItemX"]
                                       ,y=conSec.dicConfigAgregarMercado["btGuardarCambioItemY"]
                                       )
        
        self.btnLimpiarEntrys=CTkButton(self.fmFormulario
                                        ,text=' Limpiar'
                                        ,fg_color=conColor["bgBotones"]
                                        ,font=(conFuente["Fuente"],conFuente["tamano"])
                                        #,text_color=conColor["ColorLetras"]
                                        ,command=self.fnLimpiar
                                        ,image=self.imagenLimpiar
                                        ,cursor=conMaus["cursor"]
                                        ,compound=conMaus["compound"]
                                        ,width=conSec.dicConfigAgregarMercado["btLimpiarEntrysWidht"]
                                        ,height=conSec.dicConfigAgregarMercado["btLimpiarEntrysHeight"]
                                        )
        self.btnLimpiarEntrys.place(x=conSec.dicConfigAgregarMercado["btLimpiarEntrysX"]
                                    ,y=conSec.dicConfigAgregarMercado["btLimpiarEntrysY"]
                                    )
        
        self.btLEliminarProducto= CTkButton(self.fmFormulario
                                            ,text=' Eliminar Producto'
                                            #,bg=conColor["bgBotones"]
                                            ,font=(conFuente["Fuente"],conFuente["tamano"])
                                            #,fg=conColor["ColorLetras"]
                                            ,command=self.eliminarProductosTbTemporal
                                            ,image=self.imagenEliminar
                                            ,cursor=conMaus["cursor"]
                                            ,compound=conMaus["compound"]
                                            ,width=conSec.dicConfigAgregarMercado["btEliminarProductoWidht"]
                                            ,height=conSec.dicConfigAgregarMercado["btEliminarProductoHeight"]
                                            )
        self.btLEliminarProducto.place(x=conSec.dicConfigAgregarMercado["btEliminarProductoX"]
                                      ,y=conSec.dicConfigAgregarMercado["btEliminarProductoY"]
                                      )
        
        #Boton cargar compra
        self.btnCargarCompra=CTkButton(self.fmFormulario
                                          ,text='  Cargar Compra '
                                           ,fg_color=conColor["bgBotones"]
                                           ,font=(conFuente["Fuente"],conFuente["tamano"])
                                           ,command=self.execCargarCompra
                                           ,image=self.imagenGuardar
                                           ,cursor=conMaus["cursor"]
                                           ,compound=conMaus["compound"]
                                           ,width=conSec.dicConfigAgregarMercado["btnCargarCompraWidth"]
                                          ,height=conSec.dicConfigAgregarMercado["btnCargarCompraHeight"])
        self.btnCargarCompra.place(x=conSec.dicConfigAgregarMercado["btnCargarCompraX"]
                                   ,y=conSec.dicConfigAgregarMercado["btnCargarCompraY"]
                                   )
        
        self.etPrecioUnidad.bind('<Return>',self.cantidad)
#=============================================================================================================================
    def productosAgregados(self):

        mensaje = []
        self.listaProductos = []

        #Creamos objeto para traer los productos que se van agregando
        objConsultarProductosAgregados = MercadoTempController(None
                                                               ,None
                                                               ,None
                                                               ,None
                                                               ,None
                                                               ,None
                                                               ,None
                                                               ,None
                                                               )
        self.listaProductos, mensaje = objConsultarProductosAgregados.consultarMercadoTempController()

        if mensaje[0]==0:
            mss.mensajeError(mensaje[1])

        self.fmListado = CTkFrame(self.FramePrincipal
                                  ,fg_color=conColor['fg_color']
                                  ,width=conSec.dicConfigAgregarMercado["fmListaWidht"]
                                  ,height=conSec.dicConfigAgregarMercado["fmListaHeight"])
        self.fmListado.place(x=conSec.dicConfigAgregarMercado["fmListax"]
                                ,y=conSec.dicConfigAgregarMercado["fmListay"]
                                
                                )

        self.lbListadoItems= CTkLabel(self.fmListado
                                      ,text='Productos Agregados'
                                      ,fg_color=conColor["bgLabels"]
                                      ,font=(conFuente["Fuente"],conFuente["tamano"])
                                      ,text_color=conColor["colorLetrasLabel"]
                                      ,corner_radius=8
                                      )
        self.lbListadoItems.pack(pady=conSec.dicConfigAgregarMercado["lbListadoPady"])

         #Treeview Items agregados
        self.tvListaItem = ttk.Treeview(self.fmListado
                                        ,columns=(
                                                'mercadoId'
                                                ,'Cantidad'
                                                ,'PrecioUnidad'
                                                ,'PrecioTotal'
                                                ,'NumeroDeFactura'
                                                ,'Comercio'
                                                ,'describcionCompra'
                                        ))
        #Cambia el estilo para las columnas insertadas
        self.tvListaItem.tag_configure('evenrow',background=conColor["bgGeneral"],foreground=conColor["ColorLetras"])
        
        # #Indicamos el titulo de las columnas
        self.tvListaItem.heading("#0", text='Mercado Id',)
        self.tvListaItem.heading("#1", text='Producto',)
        self.tvListaItem.heading("#2", text='Cantidad',)
        self.tvListaItem.heading("#3", text='Precio Unidad',) 
        self.tvListaItem.heading("#4", text='Precio Total',)
        self.tvListaItem.heading("#5", text='Numero de Factura',)
        self.tvListaItem.heading("#6", text='Comercio',)
        self.tvListaItem.heading("#7", text='Describcion Compra',)
        
        # #configuramos las columnas
        self.tvListaItem.column("#0",width=80, anchor='center',)
        self.tvListaItem.column("#1",width=160, anchor='center',)
        self.tvListaItem.column("#2",width=60,  anchor='center')
        self.tvListaItem.column("#3",width=120, anchor='center')
        self.tvListaItem.column("#4",width=120, anchor='center')
        self.tvListaItem.column("#5",width=120, anchor='center')
        self.tvListaItem.column("#6",width=190, anchor='center')
        self.tvListaItem.column("#7",width=190, anchor='center')

        #Insertamos la información en la tabla
        for i in self.listaProductos:
            self.tvListaItem.insert("",'end'
                                    ,text=i[0]
                                    ,values=(i[1]
                                             ,i[2]
                                             ,i[3]
                                             ,i[4]
                                             ,i[5]
                                             ,i[6]
                                             ,i[7]
                                             )
                                    ,tags='evenrow')
            
        self.tvListaItem.pack(side='left',fill='y', expand=True)

        #Insertamos Scroll bar
        self.scrollBar = CTkScrollbar(self.fmListado
                                     ,command=self.tvListaItem.yview
                                     ,bg_color=conColor["bgLabels"]
                                     ,button_color=conColor["fg_color"]
                                     )
        self.scrollBar.pack(side='right',fill='y')
    
        self.tvListaItem.configure(yscrollcommand=self.scrollBar.set)

        #Evento para selección de filas en treview
        self.tvListaItem.bind('<<TreeviewSelect>>',self.seleccionarProducto)

    def seleccionarProducto(self,event):
        #lleva a los entrys los datos de las facturas seleccionadas

        #Modificamos el estado de los checButtons
        self.cbFijarFactura.deselect()
        self.cbFijarCompra.deselect()
        self.cbNFijarComercio.deselect()
        
        self.fnLimpiar()#Ejecutamos función de limpiar campos
         
        #inicializar variables
        self.vrIdeMercadoTemp = None
        self.vrIdFactura = None
        self.vrnumeroFactura = None
        self.vrValorTotalFactura = None
        self.vrFechaFactura = None
        self.vrNombreComercio = None
        self.vrDescribcionCompra = None

        try: 
              self.vrIdeMercadoTemp = self.tvListaItem.item(self.tvListaItem.selection())['text']
              self.vrNombreProducto = self.tvListaItem.item(self.tvListaItem.selection())['values'][0]
              self.vrCantidadProducto =self.tvListaItem.item(self.tvListaItem.selection())['values'][1]
              self.vrPrecioUnidad =self.tvListaItem.item(self.tvListaItem.selection())['values'][2]
              self.vrPrecioTotal =self.tvListaItem.item(self.tvListaItem.selection())['values'][3]
              self.vrNumeroFactura =self.tvListaItem.item(self.tvListaItem.selection())['values'][4]
              self.vrNombreComercio =self.tvListaItem.item(self.tvListaItem.selection())['values'][5]
              self.vrDescribcionCompra = self.tvListaItem.item(self.tvListaItem.selection())['values'][6]

              self.etNombreProducto.configure(state='normal')
              self.etNombreProducto.insert(0,self.vrNombreProducto)
              self.etNombreProducto.configure(state='disabled')
               
              self.etCantidadProducto.delete(0,'end')
              self.etCantidadProducto.insert(0,self.vrCantidadProducto)

              self.etPrecioUnidad.insert(0,self.vrPrecioUnidad)
              self.etPrecioTotal.insert(0,self.vrPrecioTotal)
              
              self.etNumeroFactura.configure(state='normal')
              self.etNumeroFactura.insert(0,self.vrNumeroFactura)
              self.etNumeroFactura.configure(state='disabled')

              self.etNombreComercio.configure(state='normal')
              self.etNombreComercio.insert(0,self.vrNombreComercio)
              self.etNombreComercio.configure(state='disabled')

              self.etDescribcionMercado.configure(state='normal')
              self.etDescribcionMercado.insert(0, self.vrDescribcionCompra)
              self.etDescribcionMercado.configure(state='disabled')
              
              self.consultarLlaves(self.vrIdeMercadoTemp)

        except:
             pass
    
    def consultarLlaves(self,mercadoId):
        
        self.listaLlaves = []

        #Funcionalidad para consultar las llaves
        objConsultarLlaves = MercadoTempController(mercadoId
                                                   ,None
                                                   ,None
                                                   ,None
                                                   ,None
                                                   ,None
                                                   ,None
                                                   ,None
                                                   )

        self.listaLlaves, mensaje = objConsultarLlaves.consultarKeysMercadosTempController()

        if mensaje[0]==0:
            mss.mensajeError(mensaje[1])
        
    def cantidad (self,event):
        #Calcula el valor total si la cantidad es mallor a 2 productos
        #convertirNumero acepta el formato colombiano (12.500 = doce mil quinientos)
        cantidad = convertirNumero(self.etCantidadProducto.get())
        precioUnidad = convertirNumero(self.etPrecioUnidad.get())

        if cantidad is None or precioUnidad is None:
            self.etPrecioTotal.delete(0,'end')
            self.etPrecioTotal.insert(0,self.etPrecioUnidad.get())

        else:
            if cantidad==1:

                self.etPrecioTotal.delete(0,'end')
                self.etPrecioTotal.insert(0,self.etPrecioUnidad.get())

            if cantidad>1:

                self.etPrecioTotal.delete(0,'end')
                precioTotal = (precioUnidad * cantidad)

                self.etPrecioTotal.insert(0,formatearNumero(precioTotal))
