from tkinter import ttk
from customtkinter import CTkLabel,CTkFrame,set_appearance_mode,set_default_color_theme,CTkScrollbar,CTkScrollableFrame
from views import configuracionesGenerales as conGen
from controller import mercadosController
from views.frameTotal import WidgetsDatos

class TreviewUltimoMercado(CTkFrame):
    """
    Clase que representa el Treeview del último mercado.
    """

    def __init__(self,master=None):
        super().__init__(master)
        self.master=master
        #Apariencia
        self._fg_color =conGen.dicConfiguracionGeneralColores['bgGeneral']
        self.place(x=conGen.dicConfigFrameUltimoMercado["fmXFramePrincipal"]
                   ,y=conGen.dicConfigFrameUltimoMercado["fmyFramePrincipal"]
                  )      
        self.estiloTreview()
        self.crearTreview()
        WidgetsDatos(self.master,conGen.dicConfigFrameUltimoMercado["fmDatosX"],conGen.dicConfigFrameUltimoMercado["fmDatosY"],self.listaProductos)#Calcula el total y cantidad de productos agregados

    def estiloTreview(self):
        #Configuracion del treeview
        self.tvResultadosStyle=ttk.Style()
        
        self.tvResultadosStyle.theme_use("clam")
        #cCambia el estilo del encabezado
        self.tvResultadosStyle.configure("Treeview.Heading"
                                         ,background = conGen.dicConfiguracionGeneralColores["bgLabels"]
                                         ,foreground = conGen.dicConfiguracionGeneralColores["colorLetrasLabel"]
                                         
                                         )

        #Cambia el estilo de letras y tamaño de letra del treeview
        self.tvResultadosStyle.configure("Treeview", font=(conGen.dicConfiguracionGeneralFuentes["Fuente"],10)
                                         ,background=conGen.dicConfiguracionGeneralColores["bgGeneral"]
                                         ,fieldbackground = conGen.dicConfiguracionGeneralColores["fg_color"]#cambia el fondo de la tabla
                                         )

        #Cambia el estilo de la fila seleccionada
        self.tvResultadosStyle.map('Treeview'
                                   , background=[('selected',conGen.dicConfiguracionGeneralColores["ColorLetras"])]
                                   , foreground=[('selected',conGen.dicConfiguracionGeneralColores["bgGeneral"])])

    def crearTreview(self): 
        self.listaProductos, mensaje = mercadosController.consultarUltimoMercado()
        
        self.fmPrincipal=CTkFrame(self
                                  ,fg_color=conGen.dicConfiguracionGeneralColores["fg_color"]
                                  ,width=1000#conGen.dicConfigFrameUltimoMercado["fmWidthFramePrincipal"]
                                  ,height=1000#conGen.dicConfigFrameUltimoMercado["fmHeightFramePrincipal"]
                                  )
        self.fmPrincipal.pack(anchor='nw')

        self.label1=CTkLabel(self.fmPrincipal
                            ,fg_color=conGen.dicConfiguracionGeneralColores["bgLabels"]
                            ,text='Ultimo Mercado Registrado'
                            ,text_color=conGen.dicConfiguracionGeneralColores["colorLetrasLabel"]
                            ,font=(conGen.dicConfiguracionGeneralFuentes["Fuente"],14)
                            #,fg=conGen.dicConfiguracionGeneralColores["ColorLetras"]
                            ,justify='center'    
                            ,corner_radius=8      
                            )
        self.label1.pack(pady=conGen.dicConfigFrameUltimoMercado["lbPady"])
        
        #Creación de Tabla
        self.tvResultados=ttk.Treeview(self.fmPrincipal,
                                       style="Treeview",
                                       columns=('Producto'
                                                ,'cantidad'
                                                ,'precioUnidad'
                                                ,'precioTotal'
                                                ,'numeroFactura'
                                                ,'fechaFactura'
                                                ,'comercio'
                                                ,'descMercado' 
                                                )
                                        ,)

        #Cambia el estilo para las columnas insertadas
        self.tvResultados.tag_configure('evenrow'
                                        ,background=conGen.dicConfiguracionGeneralColores["bgGeneral"]
                                        
                                        ,foreground=conGen.dicConfiguracionGeneralColores["ColorLetras"]
                                        )

        # #Indicamos el titulo de las columnas
        self.tvResultados.heading("#0", text='Id',)
        self.tvResultados.heading("#1", text='Producto',)
        self.tvResultados.heading("#2", text='Cantidad',)
        self.tvResultados.heading("#3", text='Precio Unidad',) 
        self.tvResultados.heading("#4", text='Precio Total',)
        self.tvResultados.heading("#5", text='Numero de Factura',)
        self.tvResultados.heading("#6", text='Fecha Factura',)
        self.tvResultados.heading("#7", text='Comercio',)
        self.tvResultados.heading("#8", text='Desc. Mercado',)
        
        # #configuramos las columnas
        self.tvResultados.column("#0",width=50, anchor='center',)
        self.tvResultados.column("#1",width=160, anchor='center',)
        self.tvResultados.column("#2",width=60,  anchor='center')
        self.tvResultados.column("#3",width=90, anchor='center')
        self.tvResultados.column("#4",width=85, anchor='center')
        self.tvResultados.column("#5",width=120, anchor='center')
        self.tvResultados.column("#6",width=100, anchor='center')
        self.tvResultados.column("#7",width=160, anchor='center')
        self.tvResultados.column("#8",width=100, anchor='center')

        self.tvResultados.pack(side='left',fill='y', expand=True)

        for i in self.listaProductos:
            self.tvResultados.insert(""
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
        
        #scroll bar
        self.scrollBarr=CTkScrollbar(self.fmPrincipal
                     #,hover=True
                     ,command=self.tvResultados.yview
                     ,orientation='vertical'
                     ,bg_color=conGen.dicConfiguracionGeneralColores["bgLabels"]
                     ,button_color=conGen.dicConfiguracionGeneralColores["fg_color"]
                     )
        self.scrollBarr.pack(side='right', fill="y")
        self.tvResultados.configure(yscrollcommand=self.scrollBarr.set)