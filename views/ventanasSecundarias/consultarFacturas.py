from customtkinter import CTkToplevel,CTkFrame,CTkLabel,CTkEntry,CTkButton,CTkScrollbar,CTkImage
from tkinter import ttk
from tkcalendar import Calendar
from PIL import Image
from views.ventanasSecundarias.configuracionVentanasSecundarias import dicConfigConsultarFactura as conFac
from views.ventanasSecundarias.configuracionVentanasSecundarias import dicConfigRegistrarFactura as conReFac
from views.configuracionesGenerales import dicConfig as conMaus
from views.ventanasSecundarias.configuracionVentanasSecundarias  import dicConfigPosicion as conPos
from views.configuracionesGenerales import dicConfiguracionGeneralColores as conColores
from views.configuracionesGenerales import dicConfiguracionGeneralFuentes as conFuentes
from controller.facturasController import FacturaController
from views.messagebox import mensajesEmergentes as msbx
from views.vwImgConfig import  leerImagen


class ConsultarFacturas(CTkToplevel):
    #vista para consulta de facturas
    def __init__(self,master):
        super().__init__(master)
        self.master=master
        self.geometry(f"{conFac['vnConsultarFacturaWidth']}x{conFac['vnConsultarFacturaHeight']}+{conPos['vnConsultarFacturasX']}+{conPos['vnConsultarFacturasY']}")
        self.title('Consultar Facturas')
        #Importamos las imagenes
        self.imagenBuscar=CTkImage(dark_image=Image.open(leerImagen("Consultar")),size=(28,28))
        self.imagenCancelar=CTkImage(dark_image=Image.open(leerImagen("Cancelar")),size=(28,28))
        self.imagenActualizar=CTkImage(dark_image=Image.open(leerImagen("Actualizar")),size=(28,28))
        self.imagenCalendario=CTkImage(dark_image=Image.open(leerImagen("Calendario")),size=(28,28))
        self.imagenGuardar=CTkImage(dark_image=Image.open(leerImagen("Guardar")),size=(28,28))
        self.resizable(False,False)
        self.transient(master)
        self.lift()
        self.widgetBusquedaFacturas()
        self.frameModificaciones()
        self.twConsultarFacturas()
    
    def btnCancelar(self):
         self.destroy()

    def fnEventoConsultarFactura(self,event):
            #Función para buscar facturas con cada letra que se ingresa
            try:
                self.btnBuscarFactura()
            except:
                pass


    def btnBuscarFactura(self):
         #Función para buscar facturas
        listaFacturas = []

        objConsultaFactura = FacturaController(None
                                               ,self.etBuscarFacturas.get()
                                               ,None
                                               ,None)
        
        listaFacturas,mensaje = objConsultaFactura.consultarFacturasController()

        if mensaje[0]==1:
             #Borramos información insertada en la tabla 
             for i in self.twConsultarFacturasRegistradas.get_children():
                  self.twConsultarFacturasRegistradas.delete(i)
             #Insertamos la información consultada
             for i in listaFacturas:
                  self.twConsultarFacturasRegistradas.insert(""
                                                             ,"end"
                                                             ,text=i[0]
                                                             ,values=(i[1]
                                                                      ,i[2]
                                                                      ,i[3])
                                                             ,tags='evenrow')
        else:
             msbx.mensajeError(mensaje[1])
    
    def fnConsultaFactura(self):
          #Consulta facturas registradas

          listadoFacturas = []

          #declaramos objeto
          objConsultaFacturas = FacturaController(None
                                               ,None
                                               ,None
                                               ,None)
          #recuperamos datos
          listadoFacturas, mensaje = objConsultaFacturas.consultarListaFacturas()
          if mensaje[0]==0:
               msbx.mensajeError(mensaje[1])

          return listadoFacturas

    def capturarFechaFactura(self):
     
    #Funcionalidad del botón que guarda la fecha después de ser seleccionada en el calendario
          self.etModificacionesFechaFactura.configure(state='normal'
                                             ,fg_color=conColores["bgEntrys"]
                                             ,text_color=conColores["colorLetrasEntry"]
                                        )
          self.etModificacionesFechaFactura.delete(0,'end')
          self.etModificacionesFechaFactura.insert(0,self.clFechaFactura.get_date())
          self.etModificacionesFechaFactura.configure(state='disabled')
          self.venCalendario.destroy()

    def insertarFechaEntry(self):
        #muestra una nueva mentana con el calendario
        self.venCalendario=CTkToplevel(self)
        self.venCalendario.title("Ingresar Fecha")
        self.venCalendario.transient(self)
        width=conReFac["vcWidth"]
        height=conReFac["vcHeight"]
        bg=conReFac["vcBg"]
        self.venCalendario.grab_set()
       #self.venCalendario.focus()

        #Se crea el calendario
        self.clFechaFactura=Calendar(self.venCalendario)
        self.clFechaFactura.config(selectmode='day'
                                   ,locale='es_ES'
                                   ,date_pattern="yyyy-MM-dd"
                                   )
        self.clFechaFactura.pack()

        #Boton para seleccionar la fecha
        self.btnSeleccionarFecha=CTkButton(self.venCalendario
                                        ,text='Seleccionar'
                                        ,fg_color=conColores["bgBotones"]
                                        ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                        #,fg=conColor["ColorLetras"]
                                        ,image=self.imagenGuardar
                                        ,command=self.capturarFechaFactura
                                        ,cursor=conMaus["cursor"]
                                        ,compound=conMaus["compound"]
                                        ,width=conReFac["btnCalWidth"]
                                        )
        self.btnSeleccionarFecha.pack(pady=conReFac["btCalPady"]
                                      ,)

    def fnModificarFacturas(self):
         #modifica la factura seleccionada en el treevieww
         #Declaramos el objeto 
         
         objModificarFacturas = FacturaController(self.vrIdFactura
                                                  ,self.etModificacionesNumeroFactura.get()
                                                  ,self.etModificacionesTotalFactura.get()
                                                  ,self.etModificacionesFechaFactura.get())
         mensaje = objModificarFacturas.modificarFacturas()
         if mensaje[0]==1:
              self.twConsultarFacturas()
              msbx.mensajeInformativo(mensaje[1])

              self.etModificacionesNumeroFactura.delete(0,'end')
              
              self.etModificacionesTotalFactura.delete(0,'end')
              
              self.etModificacionesFechaFactura.configure(state='normal')
              self.etModificacionesFechaFactura.delete(0,'end')
              self.etModificacionesFechaFactura.configure(state='disabled')

         elif mensaje[0]==0:
              msbx.mensajeError(mensaje[1])
         elif mensaje[0]==2:
              msbx.mensajeError(mensaje[1])


    def widgetBusquedaFacturas(self):
        #Vista para frame de busquedas
        self.fmBusquedaFacturas=CTkFrame(self
                                         ,fg_color=conColores["fg_color"]
                                         )
        self.fmBusquedaFacturas.place(x=conFac["fmBusquedaFacturasX"]
                                      ,y=conFac["fmBusquedaFacturasY"]
                                      )
        
        #Label ingresar numero factura
        self.lbBuscarFacturas = CTkLabel(self.fmBusquedaFacturas
                                        ,text='Ingrese Numero Factura'
                                        ,fg_color=conColores["bgLabels"]
                                        ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                        ,text_color=conColores["colorLetrasLabel"]
                                        ,corner_radius=8
                                        ,width=conFac["lbBuscarFacturasWidth"]
                                        ,height=conFac["lbBuscarFacturasHeight"]
                                        )
        self.lbBuscarFacturas.grid(column=0
                                   ,row=0
                                   ,padx=conFac["padX"]
                                   ,pady=conFac["padY"]
                                   )
        
        #Entry ingresar ingresar numero de factura
        self.etBuscarFacturas = CTkEntry(self.fmBusquedaFacturas
                                        ,fg_color=conColores["bgEntrys"]
                                        #,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                        ,text_color=conColores["colorLetrasEntry"]
                                        ,justify='center'
                                        ,corner_radius=8
                                        ,width=conFac["etBuscarFacturasWidth"]
                                        ,height=conFac["etBuscarFacturasHeight"]
                                        )
        self.etBuscarFacturas.grid(column=0
                                ,row=1
                                ,padx=conFac["padX"]
                                ,pady=conFac["padY"]
                                )
        #Button buscar facturas
        self.btBuscarFacturas = CTkButton(self.fmBusquedaFacturas
                                           ,text='Buscar'
                                           ,fg_color=conColores["bgBotones"]
                                           ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                           #,text_color=conColores["ColorLetras"]
                                           ,command= self.btnBuscarFactura
                                           ,image=self.imagenBuscar
                                           ,cursor=conMaus["cursor"]
                                           ,compound=conMaus["compound"]
                                           ,width=conFac["btBuscarFacturasWidth"]
                                           ,height=conFac["btBuscarFacturasHeight"]   
                                           )
        self.btBuscarFacturas.grid(column=0
                                     ,row=2
                                     ,padx=conFac["padX"]
                                     ,pady=conFac["padY"]     
                                    )
        #Boton cancelar
        self.btnCancelarConsulta=CTkButton(self.fmBusquedaFacturas
                                           ,text='Cancelar O Salir'
                                           ,fg_color=conColores["bgBotones"]
                                           ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                           #,fg=conColores["ColorLetras"]
                                           ,command=self.btnCancelar
                                           ,image=self.imagenCancelar
                                           ,cursor=conMaus["cursor"]
                                           ,compound=conMaus["compound"]
                                           ,width=conFac["btnCancelarConsultaWidth"]
                                           ,height=conFac["btnCancelarConsultaHeight"]
                                           )
        self.btnCancelarConsulta.grid(column=0
                                      ,row=3
                                      ,padx=conFac["padX"]
                                      ,pady=conFac["padX"]
                                     )
        
        #control de eventos
        self.etBuscarFacturas.bind('<Key>',self.fnEventoConsultarFactura)
    
    def frameModificaciones(self):
            #Frame modificaciones
            self.fmFrameModificacionFactura=CTkFrame(self
                                                      ,fg_color=conColores['fg_color']
                                                      )
            self.fmFrameModificacionFactura.place(x=conFac["fmFrameModificacionFacturaX"]
                                                   ,y=conFac["fmFrameModificacionFacturaY"])
            
            #Label numero de factura
            self.lbModificacionesNumeroFactura= CTkLabel(self.fmFrameModificacionFactura
                                            ,text='Numero de  Factura'
                                            ,fg_color=conColores["bgLabels"]
                                            ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                            ,text_color=conColores["colorLetrasLabel"]
                                            ,corner_radius=8
                                            ,width=conFac["lbModificacionesNumeroFacturaWidth"]
                                            ,height=conFac["lbModificacionesNumeroFacturaHigth"]
                                            )
            self.lbModificacionesNumeroFactura.grid(column=0
                                        ,row=0
                                        ,padx=conFac["padX"]
                                        ,pady=conFac["padX"]
                                        )
            #Entry numero de factura
            self.etModificacionesNumeroFactura=CTkEntry(self.fmFrameModificacionFactura
                                            ,fg_color=conColores["bgEntrys"]
                                            #,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                            ,text_color=conColores["colorLetrasEntry"]
                                            ,justify='center'
                                            ,corner_radius=8
                                            ,width=conFac["etModificacionesNumeroFacturaWidth"]
                                            ,height=conFac["etModificacionesNumeroFacturaHigth"]
                                            )
            self.etModificacionesNumeroFactura.grid(column=0 
                                       ,row=1
                                       ,padx=conFac["padX"]
                                       ,pady=conFac["padX"])
            #------------------------------------------
             #Label Total
            self.lbModificacionesTotalFactura= CTkLabel(self.fmFrameModificacionFactura
                                            ,text='Valor Total Factura'
                                            ,fg_color=conColores["bgLabels"]
                                            ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                            ,text_color=conColores["colorLetrasLabel"]
                                            ,corner_radius=8
                                            ,width=conFac["lbModificacionesTotalFacturaWidth"]
                                            ,height=conFac["lbModificacionesTotalFacturaHigth"]
                                            )
            self.lbModificacionesTotalFactura.grid(column=0
                                        ,row=2
                                        ,padx=conFac["padX"]
                                        ,pady=conFac["padX"]
                                        )
            
            #Entry valor total factura
            self.etModificacionesTotalFactura=CTkEntry(self.fmFrameModificacionFactura
                                            ,fg_color=conColores["bgEntrys"]
                                            #,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                            ,text_color=conColores["colorLetrasEntry"]
                                            ,justify='center'
                                            ,corner_radius=8
                                            ,width=conFac["lbModificacionesTotalFacturaWidth"]
                                            ,height=conFac["lbModificacionesTotalFacturaHigth"]
                                            )
            self.etModificacionesTotalFactura.grid(column=0 
                                                   ,row=3
                                                   ,padx=conFac["padX"]
                                                   ,pady=conFac["padX"])
            #-----------------------------------------
            #Label fecha factura
            self.lbModificacionesFechaFactura= CTkLabel(self.fmFrameModificacionFactura
                                            ,text='Fecha de  Factura'
                                            ,fg_color=conColores["bgLabels"]
                                            ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                            ,text_color=conColores["colorLetrasLabel"]
                                            ,corner_radius=8
                                            ,width=conFac["lbModificacionesFechaFacturaWidth"]
                                            ,height=conFac["lbModificacionesFechaFacturaHigth"]
                                            )
            self.lbModificacionesFechaFactura.grid(column=0
                                        ,row=4
                                        ,padx=conFac["padX"]
                                        ,pady=conFac["padX"]
                                        )
            
            #Entry fecha factura
            self.etModificacionesFechaFactura=CTkEntry(self.fmFrameModificacionFactura
                                            ,fg_color=conColores["bgEntrys"]
                                            #,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                            ,text_color=conColores["colorLetrasEntry"]
                                            ,justify='center'
                                            ,corner_radius=8
                                            ,width=conFac["etModificacionesFechaFacturaWidth"]
                                            ,height=conFac["etModificacionesFechaFacturaHigth"]
                                            ,state='disabled'
                                            )
            self.etModificacionesFechaFactura.grid(column=0 
                                       ,row=5
                                       ,padx=conFac["padX"]
                                       ,pady=conFac["padX"])
            
            #Boton Seleccionar Fecha
            self.btnModificarFacturas=CTkButton(self.fmFrameModificacionFactura
                                                ,text='   Cambiar Fecha   '
                                                ,fg_color=conColores["bgBotones"]
                                                ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                                #,text_color=conColor["ColorLetras"]
                                                ,command=self.insertarFechaEntry
                                                ,image=self.imagenCalendario
                                                ,cursor=conMaus["cursor"]
                                                ,compound=conMaus["compound"]
                                                ,width=conFac["btnModificarFacturasWidht"]
                                                ,height=conFac["btnModificarFacturasHeight"]
                                                )
            self.btnModificarFacturas.grid(column=0
                                           ,row=6
                                           ,padx=conFac["padX"]
                                           ,pady=conFac["padX"]
                                           )
            
            #Button Modificar factura
            self.btnModificarFacturas=CTkButton(self.fmFrameModificacionFactura
                                                ,text=' Actualizar Cambio'
                                                ,fg_color=conColores["bgBotones"]
                                                ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                                #,text_color=conColor["ColorLetras"]
                                                ,command=self.fnModificarFacturas
                                                ,image=self.imagenActualizar
                                                ,cursor=conMaus["cursor"]
                                                ,compound=conMaus["compound"]
                                                ,width=conFac["btnModificarFacturasWidht"]
                                                ,height=conFac["btnModificarFacturasHeight"]
                                                )
            self.btnModificarFacturas.grid(column=0
                                           ,row=7
                                           ,padx=conFac["padX"]
                                           ,pady=conFac["padX"]
                                           )
            #Eventos
            self.etModificacionesNumeroFactura.bind('<Return>', self.fnEventoEnter)
            self.etModificacionesTotalFactura.bind('<Return>', self.fnEventoEnter)
    
    
    def twConsultarFacturas(self):
       #Consultamos las facturas registradas
       listadoFacturas = self.fnConsultaFactura()

       #creación frame para treeview
       self.fmTreviewConsultarFacturas= CTkFrame(self
                                                  ,fg_color=conColores["fg_color"]
                                                 )
       self.fmTreviewConsultarFacturas.place(x=conFac["fmPrincipalResultadoX"]
                                            ,y=conFac["fmPrincipalResultadoY"]
                                            )
       #Label Resultado busqueda
       self.lbResultadoBusqueda = CTkLabel(self.fmTreviewConsultarFacturas
                                           ,text='Resultado de Busqueda'
                                           ,fg_color=conColores["bgLabels"]
                                           ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                           ,text_color=conColores["colorLetrasLabel"]
                                           ,corner_radius=8
                                           )
       self.lbResultadoBusqueda.pack(anchor=conFac["lbResultadoBusquedaAnchor"]
                                     ,pady=conFac["lbResultadoBusquedaPady"])
       #creación de treview para resultados facturas
       self.twConsultarFacturasRegistradas = ttk.Treeview(self.fmTreviewConsultarFacturas
                                                ,style='Treeview'
                                                ,columns=('NumeroFactura'
                                                          ,'ValorTotal'
                                                          ,'FechaFactura'
                                                        )
                                                ,height=conFac['twConsultarFacturasRegistradasHeight']
                                                )
       #Configuración para las filas seleccionadas
       self.twConsultarFacturasRegistradas.tag_configure('evenrow'
                                                ,background=conColores["bgGeneral"]
                                                ,foreground=conColores["ColorLetras"]
                                                )
       
       # #Indicamos el titulo de las columnas
       self.twConsultarFacturasRegistradas.heading("#0", text='Factura Id',)
       self.twConsultarFacturasRegistradas.heading("#1", text='Numero Factura',)
       self.twConsultarFacturasRegistradas.heading("#2", text='Valor Total Factura',)
       self.twConsultarFacturasRegistradas.heading("#3", text='Fecha Factura',)
        
       # #configuramos las columnas
       self.twConsultarFacturasRegistradas.column("#0",width=90, anchor='center', )
       self.twConsultarFacturasRegistradas.column("#1",width=160,  anchor='center')
       self.twConsultarFacturasRegistradas.column("#2",width=160,  anchor='center')
       self.twConsultarFacturasRegistradas.column("#3",width=160,  anchor='center')

       #Insertamos los datos consultados desde la base de datos en el treview(tabla)
       for i in listadoFacturas:
            self.twConsultarFacturasRegistradas.insert("",'end',text=i[0],values=(i[1],i[2],i[3],),tags='evenrow')
       
       self.twConsultarFacturasRegistradas.pack(side='left',fill='y', expand=True)

       #Creamos Scroll
       self.scrollBar = CTkScrollbar(self.fmTreviewConsultarFacturas
                                     ,command=self.twConsultarFacturasRegistradas.yview
                                     ,bg_color=conColores["bgLabels"]
                                     ,button_color=conColores["fg_color"]
                                     )
       self.scrollBar.pack(side='right',fill='y')

       self.twConsultarFacturasRegistradas.configure(yscrollcommand=self.scrollBar.set)

       self.twConsultarFacturasRegistradas.bind('<<TreeviewSelect>>',self.seleccionarFactura)

    def seleccionarFactura(self,event):
         #lleva a los entrys los datos de las facturas seleccionadas

         #Limpiamos los campos
         self.etModificacionesNumeroFactura.delete(0,'end')
         self.etModificacionesTotalFactura.delete(0,'end')
         self.etModificacionesFechaFactura.configure(state='normal')
         self.etModificacionesFechaFactura.delete(0,'end')
         
         #inicializar variables
         self.vrIdFactura = None
         self.vrnumeroFactura = None
         self.vrValorTotalFactura = None
         self.vrFechaFactura = None

         try:  
              #Recuperamos los datos del treview
              self.vrIdFactura = self.twConsultarFacturasRegistradas.item(self.twConsultarFacturasRegistradas.selection())['text']
              self.vrnumeroFactura =self.twConsultarFacturasRegistradas.item(self.twConsultarFacturasRegistradas.selection())['values'][0]
              self.vrValorTotalFactura =self.twConsultarFacturasRegistradas.item(self.twConsultarFacturasRegistradas.selection())['values'][1]
              self.vrFechaFactura =self.twConsultarFacturasRegistradas.item(self.twConsultarFacturasRegistradas.selection())['values'][2]

              self.etModificacionesNumeroFactura.insert(0,self.vrnumeroFactura)
              self.etModificacionesTotalFactura.insert(0,self.vrValorTotalFactura)
              self.etModificacionesFechaFactura.insert(0,self.vrFechaFactura)

              self.etModificacionesFechaFactura.configure(state='disabled')
         except:
              pass
         
       

    def fnEventoEnter(self,event):
        #Modificamos las facturas al presionar enter
        try:
            self.fnModificarFacturas()
        except:
            pass