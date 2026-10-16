from customtkinter import CTkToplevel,CTkFrame,CTkLabel,CTkEntry,CTkButton,CTkScrollbar,CTkImage
from PIL import Image
from tkinter import ttk
from views.ventanasSecundarias.configuracionVentanasSecundarias import dicConfigConsultarComercio as conCom
from views.configuracionesGenerales import dicConfig as conMaus
from views.ventanasSecundarias.configuracionVentanasSecundarias  import dicConfigPosicion as conPos
from views.configuracionesGenerales import dicConfiguracionGeneralColores as conColores
from views.configuracionesGenerales import dicConfiguracionGeneralFuentes as conFuentes
from controller.comerciosController import ComerciosController
from views.messagebox import mensajesEmergentes as msx

from views.vwImgConfig import  leerImagen

class ConsultarComercios(CTkToplevel):
    #vista para consulta de facturas
    def __init__(self,master):
        super().__init__(master)
        self.master=master
        self.geometry(f"{conCom['vnConsultarComercioWidth']}x{conCom['vnConsultarComercioHeight']}+{conPos['vnConsultarComerciosX']}+{conPos['vnConsultarComerciosY']}")
        self.title('Consultar Comercios')
        self.imagenBuscar=CTkImage(dark_image=Image.open(leerImagen("Consultar")),size=(28,28))
        self.imagenCancelar=CTkImage(dark_image=Image.open(leerImagen("Cancelar")),size=(28,28))
        self.imagenActualizar=CTkImage(dark_image=Image.open(leerImagen("Actualizar")),size=(28,28))
        self.resizable(False,False)
        self.transient(master)
        self.lift()
        self.widgetsBusquedaComercios()
        self.frameModificacionesComercios()
        #self.estiloTreview()
        self.twConsultarComercios()


    def btnCancelar(self):
         self.destroy()

    def fnEventoConsultarComercio(self,event):
            try:
                self.btnConsultarComercio()
            except:
                pass

    
    def btnConsultarComercio(self):
         
         listadoComercio = []
         #creamos objeto
         objConsultaComercio = ComerciosController(None
                                                   ,self.etBuscarComercios.get()
                                                   ,None)
         
         listadoComercio,mensaje = objConsultaComercio.consultarComerciosController()
        
         if mensaje[0]==1:
              #limpiamos la tabla
              for i in self.twConsultarComerciosRegistrados.get_children():
                   self.twConsultarComerciosRegistrados.delete(i)

              #Cargamos la tabla con la nueva información
              for i in listadoComercio:
                   self.twConsultarComerciosRegistrados.insert(""
                                                               ,"end"
                                                               ,text=i[0]
                                                               ,values=(i[1]
                                                                        ,i[2])
                                                               ,tags='evenrow')
         else:
              msx.mensajeError(mensaje)
                                
    def fnModificarComercios(self):
         #Creamos objeto
          objModificarComercios= ComerciosController(self.comercioId
                                                    ,self.etModificacionesNombreComercio.get()
                                                    ,self.etModificacionesDireccionComercio.get()
                                                    )
          
          mensaje=objModificarComercios.modificarComerciosController()

          if mensaje[0]==1:
              self.twConsultarComercios()
              self.etModificacionesNombreComercio.delete(0,'end')
              self.etModificacionesDireccionComercio.delete(0,'end')

              msx.mensajeInformativo(mensaje[1])

          if mensaje[0]==0:
              msx.mensajeError(mensaje[1])


    def widgetsBusquedaComercios(self):
        #Vista para frame de busquedas
        self.fmBusquedaComercios=CTkFrame(self
                                         ,fg_color=conColores["fg_color"]
                                         )
        self.fmBusquedaComercios.place(x=conCom["fmBusquedaComerciosX"]
                                      ,y=conCom["fmBusquedaComerciosY"]
                                      )
        
        #Label ingresar nombre comercio
        self.lbBuscarComercios = CTkLabel(self.fmBusquedaComercios
                                                ,text='Ingrese Nombre Comercio'
                                                ,fg_color=conColores["bgLabels"]
                                                ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                                ,text_color=conColores["colorLetrasLabel"]
                                                ,corner_radius=8
                                                ,width=conCom["lbBuscarComerciosWidth"]
                                                ,height=conCom["lbBuscarComerciosHeight"]
                                                )
        self.lbBuscarComercios.grid(column=0
                                           ,row=0
                                           ,padx=conCom["padX"]
                                           ,pady=conCom["padY"]
                                           )
        
        #Entry ingresar nombre comercio
        self.etBuscarComercios = CTkEntry(self.fmBusquedaComercios
                                                 ,fg_color=conColores["bgEntrys"]
                                                 #,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                                 ,text_color=conColores["colorLetrasEntry"]
                                                 ,justify='center'
                                                 ,corner_radius=8
                                                 ,width=conCom["etBuscarComerciosWidth"]
                                                 ,height=conCom["etBuscarComerciosHeight"]
                                                 )
        self.etBuscarComercios.grid(column=0
                                ,row=1
                                ,padx=conCom["padX"]
                                ,pady=conCom["padY"]
                                )
        #Button buscar Comercio
        self.btBuscarComercios = CTkButton(self.fmBusquedaComercios
                                           ,text='Buscar'
                                           ,fg_color=conColores["bgBotones"]
                                           ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                           #,text_color=conColores["ColorLetras"]
                                           ,command=self.btnConsultarComercio
                                           ,image=self.imagenBuscar
                                           ,cursor=conMaus["cursor"]
                                           ,compound=conMaus["compound"]
                                           ,width=conCom["btBuscarComerciosWidth"]
                                           ,height=conCom["btBuscarComerciosHeight"]   
                                           )
        self.btBuscarComercios.grid(column=0
                                     ,row=2
                                     ,padx=conCom["padX"]
                                     ,pady=conCom["padY"]     
                                    )
        #Boton cancelar
        self.btnCancelarConsulta=CTkButton(self.fmBusquedaComercios
                                           ,text='Cancelar O Salir'
                                           ,fg_color=conColores["bgBotones"]
                                           ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                           #,fg=conColores["ColorLetras"]
                                           ,command=self.btnCancelar
                                           ,image=self.imagenCancelar
                                           ,cursor=conMaus["cursor"]
                                           ,compound=conMaus["compound"]
                                           ,width=conCom["btnCancelarConsultaWidth"]
                                           ,height=conCom["btnCancelarConsultaHeight"]
                                           )
        self.btnCancelarConsulta.grid(column=0
                                      ,row=3
                                      ,padx=conCom["padX"]
                                      ,pady=conCom["padY"]
                                     )
        
        self.etBuscarComercios.bind('<Key>',self.fnEventoConsultarComercio)   


    def frameModificacionesComercios(self):
            #Frame modificaciones
            self.fmFrameModificacionComercio=CTkFrame(self
                                                      ,fg_color=conColores['fg_color']
                                                      )
            self.fmFrameModificacionComercio.place(x=conCom["fmFrameModificacionComercioX"]
                                                   ,y=conCom["fmFrameModificacionComercioY"])
            
            #Label nombre comercio
            self.lbModificacionesNombreComercio= CTkLabel(self.fmFrameModificacionComercio
                                            ,text='Nombre Comercio'
                                            ,fg_color=conColores["bgLabels"]
                                            ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                            ,text_color=conColores["colorLetrasLabel"]
                                            ,corner_radius=8
                                            ,width=conCom["lbModificacionesNombreComercioWidth"]
                                            ,height=conCom["lbModificacionesNombreComercioHigth"]
                                            )
            self.lbModificacionesNombreComercio.grid(column=0
                                        ,row=0
                                        ,padx=conCom["padX"]
                                        ,pady=conCom["padX"]
                                        )
            #Entry nombre comercio
            self.etModificacionesNombreComercio=CTkEntry(self.fmFrameModificacionComercio
                                            ,fg_color=conColores["bgEntrys"]
                                            #,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                            ,text_color=conColores["colorLetrasEntry"]
                                            ,justify='center'
                                            ,corner_radius=8
                                            ,width=conCom["etModificacionesNombreComercioWidth"]
                                            ,height=conCom["etModificacionesNombreComercioHigth"]
                                            )
            self.etModificacionesNombreComercio.grid(column=0 
                                       ,row=1
                                       ,padx=conCom["padX"]
                                       ,pady=conCom["padX"])
            #Label direccion comercio
            self.lbModificacionesDireccionComercio= CTkLabel(self.fmFrameModificacionComercio
                                            ,text='Dirección Comercio'
                                            ,fg_color=conColores["bgLabels"]
                                            ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                            ,text_color=conColores["colorLetrasLabel"]
                                            ,corner_radius=8
                                            ,width=conCom["lbModificacionesDireccionComercioWidth"]
                                            ,height=conCom["lbModificacionesDireccionComercioHigth"]
                                            )
            self.lbModificacionesDireccionComercio.grid(column=0
                                        ,row=2
                                        ,padx=conCom["padX"]
                                        ,pady=conCom["padX"]
                                        )
            
            #Entry direccion comercio
            self.etModificacionesDireccionComercio=CTkEntry(self.fmFrameModificacionComercio
                                            ,fg_color=conColores["bgEntrys"]
                                            #,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                            ,text_color=conColores["colorLetrasEntry"]
                                            ,justify='center'
                                            ,corner_radius=8
                                            ,width=conCom["etModificacionesDireccionComercioWidth"]
                                            ,height=conCom["etModificacionesDireccionComercioHigth"]
                                            )
            self.etModificacionesDireccionComercio.grid(column=0 
                                       ,row=3
                                       ,padx=conCom["padX"]
                                       ,pady=conCom["padX"])
            
            #Button Modificar factura
            self.btnModificarComercio=CTkButton(self.fmFrameModificacionComercio
                                                ,text=' Actualizar Cambio'
                                                ,fg_color=conColores["bgBotones"]
                                                ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                                #,text_color=conColor["ColorLetras"]
                                                ,command=self.fnModificarComercios
                                                ,image=self.imagenActualizar
                                                ,cursor=conMaus["cursor"]
                                                ,compound=conMaus["compound"]
                                                ,width=conCom["btnModificarComercioWidht"]
                                                ,height=conCom["btnModificarComercioHeight"]
                                                )
            self.btnModificarComercio.grid(column=0
                                           ,row=4
                                           ,padx=conCom["padX"]
                                           ,pady=conCom["padX"]
                                           )
    

    def twConsultarComercios(self):
       
       listadoComercios = []
       consultaComercios = ComerciosController(None
                                               ,None
                                               ,None)
       listadoComercios, mensaje = consultaComercios.consultarListaComercios()
       if mensaje[0]==0:
            msx.mensajeError(mensaje[1])

       #creación frame para treeview
       self.fmTreviewConsultarComercios= CTkFrame(self
                                                  ,fg_color=conColores["fg_color"]
                                                 )
       self.fmTreviewConsultarComercios.place(x=conCom["fmTreviewConsultarComerciosX"]
                                            ,y=conCom["fmTreviewConsultarComerciosY"]
                                           )
       #Label Resultado busqueda
       self.lbResultadoBusquedaComercios = CTkLabel(self.fmTreviewConsultarComercios
                                           ,text='Resultado de Busqueda'
                                           ,fg_color=conColores["bgLabels"]
                                           ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                           ,text_color=conColores["colorLetrasLabel"]
                                           ,corner_radius=8
                                           )
       self.lbResultadoBusquedaComercios.pack(anchor=conCom["lbResultadoBusquedaComerciosAnchor"]
                                     ,pady=conCom["lbResultadoBusquedaComerciosPady"])
       #creación de treview para resultados facturas
       self.twConsultarComerciosRegistrados = ttk.Treeview(self.fmTreviewConsultarComercios
                                                #,style='Treeview'
                                                ,columns=('nombreComercio'
                                                          ,'direccionComercio'
                                                        )
                                                ,height=conCom['twConsultarComerciosRegistradosHeight']
                                                )
       #Configuración para las filas seleccionadas
       self.twConsultarComerciosRegistrados.tag_configure('evenrow'
                                                ,background=conColores["bgGeneral"]
                                                ,foreground=conColores["ColorLetras"]
                                                )
       
       # #Indicamos el titulo de las columnas
       self.twConsultarComerciosRegistrados.heading("#0", text='Comercio Id',)
       self.twConsultarComerciosRegistrados.heading("#1", text='Nombre Comercio',)
       self.twConsultarComerciosRegistrados.heading("#2", text='Direccion Comercio',)
        
       # #configuramos las columnas
       self.twConsultarComerciosRegistrados.column("#0",width=90, anchor='center', )
       self.twConsultarComerciosRegistrados.column("#1",width=220,  anchor='center')
       self.twConsultarComerciosRegistrados.column("#2",width=220,  anchor='center')

       #Insertamos información en la tabla
       for i in listadoComercios:
            self.twConsultarComerciosRegistrados.insert("",'end',text=i[0],values=(i[1],i[2]),tags='evenrow')
       
       self.twConsultarComerciosRegistrados.pack(side='left',fill='y', expand=True)

       self.twConsultarComerciosRegistrados.bind('<<TreeviewSelect>>', self.seleccionarComercios)

       #Scroll barr
       self.scrolbar = CTkScrollbar(self.fmTreviewConsultarComercios
                                    ,command = self.twConsultarComerciosRegistrados.yview
                                    ,orientation = 'vertical'
                                    ,bg_color = conColores["bgLabels"]
                                    ,button_color = conColores["fg_color"]
                                    )
       self.scrolbar.pack(side='right',fill='y')

       self.twConsultarComerciosRegistrados.configure(yscrollcommand=self.scrolbar.set)


       
    def seleccionarComercios(self,event):
        try:
          #Limpiamos el entry
          self.etModificacionesNombreComercio.delete(0,'end')
          self.etModificacionesDireccionComercio.delete(0,'end')

          self.comercioId=None
          self.nombreComercio = None
          self.direccionComercio = None

          #Inicializamos las variables
          self.comercioId = self.twConsultarComerciosRegistrados.item(self.twConsultarComerciosRegistrados.selection())['text']
          self.nombreComercio = self.twConsultarComerciosRegistrados.item(self.twConsultarComerciosRegistrados.selection())['values'][0]
          self.direccionComercio = self.twConsultarComerciosRegistrados.item(self.twConsultarComerciosRegistrados.selection())['values'][1]


          #Insertamos nuevo valor
          self.etModificacionesNombreComercio.insert(0,self.nombreComercio)
          self.etModificacionesDireccionComercio.insert(0,self.direccionComercio)

        except:
          pass