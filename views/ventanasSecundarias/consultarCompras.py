from customtkinter import CTkToplevel,CTkFrame,CTkLabel,CTkEntry,CTkButton,CTkScrollbar,CTkImage
from PIL import Image
from tkinter import ttk
from views.ventanasSecundarias.configuracionVentanasSecundarias import dicConfigConsultarCompra as conCom
from views.configuracionesGenerales import dicConfig as conMaus
from views.ventanasSecundarias.configuracionVentanasSecundarias  import dicConfigPosicion as conPos
from views.configuracionesGenerales import dicConfiguracionGeneralColores as conColores
from views.configuracionesGenerales import dicConfiguracionGeneralFuentes as conFuentes
from controller.comprasController import ComprasController
from views.messagebox import mensajesEmergentes as msx

from views.vwImgConfig import  leerImagen

class ConsultarCompras(CTkToplevel):
    #vista para consulta de facturas
    def __init__(self,master):
        super().__init__(master)
        self.master=master
        self.geometry(f"{conCom['vnConsultarComprasWidth']}x{conCom['vnConsultarComprasHeight']}+{conPos['vnConsultarComerciosX']}+{conPos['vnConsultarComerciosY']}")
        self.title('Consultar Compras')
        self.imagenBuscar=CTkImage(dark_image=Image.open(leerImagen("Consultar")),size=(28,28))
        self.imagenCancelar=CTkImage(dark_image=Image.open(leerImagen("Cancelar")),size=(28,28))
        self.imagenActualizar=CTkImage(dark_image=Image.open(leerImagen("Actualizar")),size=(28,28))
        self.resizable(False,False)   
        self.widgetsBusquedaCompras()
        self.frameModificacionesCompras()
        self.twConsultarCompras()
        self.grab_set()


    def btnCancelar(self):
         #Boton cancelar
         self.destroy()

    def fnEventoConsultarCompras(self,event):
            #Consultar Compras al digitar cualquier letra
            try:
                self.btnConsultarCompras()
            except:
                pass
    
    def btnConsultarCompras(self):
         #Funcionalidad botón consultar
         listadoCompras = []
         
         #Creamos objeto
         objConsultaCompras = ComprasController(None
                                                ,self.etBuscarCompras.get()
                                                ,None)
         
         listadoCompras,mensaje = objConsultaCompras.consultarCompra()
        
         if mensaje[0]==1:
              
              #impiamos la tabla
              for i in self.twConsultarComprasRegistradas.get_children():
                   self.twConsultarComprasRegistradas.delete(i)

              #Cargamos la tabla con la nueva información
              for i in listadoCompras:
                   self.twConsultarComprasRegistradas.insert(""
                                                               ,"end"
                                                               ,text=i[0]
                                                               ,values=(i[1]
                                                                        ,i[2])
                                                                ,tags='evenrow')
         if mensaje[0]==0:
              #Mostramos error
              msx.mensajeError(mensaje)
                                
    def fnModificarCompra(self):
         #Creamos objeto
          objModificarCompra= ComprasController(self.compraId
                                               ,self.etModificacionesDescribcionCompra.get()
                                               ,None
                                               )
          
          mensaje=objModificarCompra.modificarCompra()

          if mensaje[0]==1:
              #ejecutamos nuevamente la lista
              self.twConsultarCompras()

              #limpiamos entry
              self.etModificacionesDescribcionCompra.delete(0,'end')

              #Imprimimos mensaje en la pantalla
              msx.mensajeInformativo(mensaje[1])

          if mensaje[0]==0:
              #Imprimimos mensaje en la pantalla
              msx.mensajeError(mensaje[1])


    def widgetsBusquedaCompras(self):
        #Vista para frame de busquedas
        self.fmBusquedaCompras=CTkFrame(self
                                         ,fg_color=conColores["fg_color"]
                                         )
        self.fmBusquedaCompras.place(x=conCom["fmBusquedaComprasX"]
                                      ,y=conCom["fmBusquedaComprasY"]
                                      )
        
        #Label ingresar describción compra
        self.lbBuscarCompras = CTkLabel(self.fmBusquedaCompras
                                                ,text='Ingrese Nombre Comercio'
                                                ,fg_color=conColores["bgLabels"]
                                                ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                                ,text_color=conColores["colorLetrasLabel"]
                                                ,corner_radius=8
                                                ,width=conCom["lbBuscarComprasWidth"]
                                                ,height=conCom["lbBuscarComprassHeight"]
                                                )
        self.lbBuscarCompras.grid(column=0
                                           ,row=0
                                           ,padx=conCom["padX"]
                                           ,pady=conCom["padY"]
                                           )
        
        #Entry ingresar describción compra
        self.etBuscarCompras = CTkEntry(self.fmBusquedaCompras
                                                 ,fg_color=conColores["bgEntrys"]
                                                 #,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                                 ,text_color=conColores["colorLetrasEntry"]
                                                 ,justify='center'
                                                 ,corner_radius=8
                                                 ,width=conCom["etBuscarComprasWidth"]
                                                 ,height=conCom["etBuscarComprasHeight"]
                                                 )
        self.etBuscarCompras.grid(column=0
                                ,row=1
                                ,padx=conCom["padX"]
                                ,pady=conCom["padY"]
                                )
        #Button buscar facturas
        self.btBuscarCompras = CTkButton(self.fmBusquedaCompras
                                           ,text='Buscar'
                                           ,fg_color=conColores["bgBotones"]
                                           ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                           #,text_color=conColores["ColorLetras"]
                                           ,command=self.btnConsultarCompras
                                           ,image=self.imagenBuscar
                                           ,cursor=conMaus["cursor"]
                                           ,compound=conMaus["compound"]
                                           ,width=conCom["btBuscarComprasWidth"]
                                           ,height=conCom["btBuscarComprassHeight"]   
                                           )
        self.btBuscarCompras.grid(column=0
                                     ,row=2
                                     ,padx=conCom["padX"]
                                     ,pady=conCom["padY"]     
                                    )
        #Boton cancelar
        self.btnCancelarConsulta=CTkButton(self.fmBusquedaCompras
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
        #Control de evento
        self.etBuscarCompras.bind('<Key>',self.fnEventoConsultarCompras)
        
    def frameModificacionesCompras(self):
            #Frame modificaciones
            self.fmFrameModificacionCompras=CTkFrame(self
                                                      ,fg_color=conColores['fg_color']
                                                      )
            self.fmFrameModificacionCompras.place(x=conCom["fmFrameModificacionComprasX"]
                                                   ,y=conCom["fmFrameModificacionComprasY"])
            
            #Label describción compra
            self.lbModificacionesDescribcionCompras= CTkLabel(self.fmFrameModificacionCompras
                                            ,text='Nombre Comercio'
                                            ,fg_color=conColores["bgLabels"]
                                            ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                            ,text_color=conColores["colorLetrasLabel"]
                                            ,corner_radius=8
                                            ,width=conCom["lbModificacionesDescribcionComprasWidth"]
                                            ,height=conCom["lbModificacionesDescribcionComprasHigth"]
                                            )
            self.lbModificacionesDescribcionCompras.grid(column=0
                                        ,row=0
                                        ,padx=conCom["padX"]
                                        ,pady=conCom["padX"]
                                        )
            #Entry describción compra
            self.etModificacionesDescribcionCompra=CTkEntry(self.fmFrameModificacionCompras
                                            ,fg_color=conColores["bgEntrys"]
                                            #,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                            ,text_color=conColores["colorLetrasEntry"]
                                            ,justify='center'
                                            ,corner_radius=8
                                            ,width=conCom["etModificacionesDescribcionCompraWidth"]
                                            ,height=conCom["etModificacionesDescribcionCompraHigth"]
                                            )
            self.etModificacionesDescribcionCompra.grid(column=0 
                                       ,row=1
                                       ,padx=conCom["padX"]
                                       ,pady=conCom["padX"])
            
            #Button Modificar Compra
            self.btnModificarCompra=CTkButton(self.fmFrameModificacionCompras
                                                ,text=' Actualizar Cambio'
                                                ,fg_color=conColores["bgBotones"]
                                                ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                                #,text_color=conColor["ColorLetras"]
                                                ,command=self.fnModificarCompra
                                                ,image=self.imagenActualizar
                                                ,cursor=conMaus["cursor"]
                                                ,compound=conMaus["compound"]
                                                ,width=conCom["btnModificarCompraWidht"]
                                                ,height=conCom["btnModificarCompraHeight"]
                                                )
            self.btnModificarCompra.grid(column=0
                                           ,row=4
                                           ,padx=conCom["padX"]
                                           ,pady=conCom["padX"]
                                           )
            
    def twConsultarCompras(self):
       
       listadoComprasRegistradas = []
       objConsultaComprasRegistradas = ComprasController (None
                                               ,None
                                               ,None)
       listadoComprasRegistradas=objConsultaComprasRegistradas.consultarComprasRegistradasController()

       #creación frame para treeview
       self.fmTreviewConsultarCompras= CTkFrame(self
                                                  ,fg_color=conColores["fg_color"]
                                                 )
       self.fmTreviewConsultarCompras.place(x=conCom["fmTreviewConsultarComprasX"]
                                            ,y=conCom["fmTreviewConsultarComprasY"]
                                           )
       #Label Resultado busqueda
       self.lbResultadoBusquedaCompras = CTkLabel(self.fmTreviewConsultarCompras
                                           ,text='Resultado de Busqueda'
                                           ,fg_color=conColores["bgLabels"]
                                           ,font=(conFuentes["Fuente"],conFuentes["tamano"])
                                           ,text_color=conColores["colorLetrasLabel"]
                                           ,corner_radius=8
                                           )
       self.lbResultadoBusquedaCompras.pack(anchor=conCom["lbResultadoBusquedaComprasAnchor"]
                                     ,pady=conCom["lbResultadoBusquedaComprasPady"])
       #creación de treview para resultados facturas
       self.twConsultarComprasRegistradas = ttk.Treeview(self.fmTreviewConsultarCompras
                                                ,style='Treeview'
                                                ,columns=('describcionCompra'
                                                          ,'fechaRegistro'
                                                        )
                                                ,height=conCom['twConsultarComprasRegistradasHeight']
                                                )
       #Configuración para las filas seleccionadas
       self.twConsultarComprasRegistradas.tag_configure('evenrow'
                                                ,background=conColores["bgGeneral"]
                                                ,foreground=conColores["ColorLetras"]
                                                )
       
       # #Indicamos el titulo de las columnas
       self.twConsultarComprasRegistradas.heading("#0", text='Comercio Id',)
       self.twConsultarComprasRegistradas.heading("#1", text='Describcion Compra',)
       self.twConsultarComprasRegistradas.heading("#2", text='Fecha De Registro',)
        
       # #configuramos las columnas
       self.twConsultarComprasRegistradas.column("#0",width=90, anchor='center', )
       self.twConsultarComprasRegistradas.column("#1",width=220,  anchor='center')
       self.twConsultarComprasRegistradas.column("#2",width=220,  anchor='center')

       #Insertamos la información en la tabla(Treview)
       for i in listadoComprasRegistradas:
            
          self.twConsultarComprasRegistradas.insert("",'end',text=i[0],values=(i[1],i[2]),tags='evenrow')
       
       self.twConsultarComprasRegistradas.pack(side='left',fill='y', expand=True)

       self.twConsultarComprasRegistradas.bind('<<TreeviewSelect>>', self.seleccionarCompras)#Evento

       #Scroll barr
       self.scrolbar = CTkScrollbar(self.fmTreviewConsultarCompras
                                    ,command = self.twConsultarComprasRegistradas.yview
                                    ,orientation = 'vertical'
                                    ,bg_color = conColores["bgLabels"]
                                    ,button_color = conColores["fg_color"]
                                    )
       self.scrolbar.pack(side='right',fill='y')

       self.twConsultarComprasRegistradas.configure(yscrollcommand=self.scrolbar.set)


       
    def seleccionarCompras(self,event):
        #Limpiamos el entry
        self.etModificacionesDescribcionCompra.delete(0,'end')
       
        self.compraId=None
        self.describcionCompra = None
        self.fechaRegistroCompra = None
        try:
        
          #Inicializamos las variables
          self.compraId = self.twConsultarComprasRegistradas.item(self.twConsultarComprasRegistradas.selection())['text']
          self.describcionCompra = self.twConsultarComprasRegistradas.item(self.twConsultarComprasRegistradas.selection())['values'][0]
          self.fechaRegistroCompra = self.twConsultarComprasRegistradas.item(self.twConsultarComprasRegistradas.selection())['values'][1]

          #Insertamos nuevo valor
          self.etModificacionesDescribcionCompra.insert(0,self.describcionCompra)
        except:
          pass