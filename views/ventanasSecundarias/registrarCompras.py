from customtkinter import CTkToplevel,CTkButton,CTkLabel,CTkImage,CTkFrame,CTkEntry
from PIL import Image
from datetime import date
from views.ventanasSecundarias.configuracionVentanasSecundarias import dicConfigRegistrarCompra as reCom
from views.ventanasSecundarias.configuracionVentanasSecundarias import dicConfigPosicion as pos
from views.configuracionesGenerales import dicConfiguracionGeneralColores as color
from views.configuracionesGenerales import dicConfiguracionGeneralFuentes as fuente
from views.configuracionesGenerales import dicConfig as maus
from controller.comprasController import ComprasController
from views.messagebox import mensajesEmergentes as mss
from views.vwImgConfig import leerImagen


class RegistrarCompras(CTkToplevel):
#clase para la vista de registro de compra

    def __init__(self,master):
        super().__init__(master)#importamos el construcor de la clase CTkToplevel
        self.master= master

        #definimos alto ancho y posición de la ventana
        self.geometry(f"{reCom['vnRegistrarCompraWidth']}x{reCom['vnRegistrarCompraHeight']}+{pos['vnRegistrarCompraX']}+{pos['vnRegistrarCompraY']}")
        
        #Importamos imagenes
        self.imgGuardar = CTkImage(dark_image=Image.open(leerImagen('Guardar')),size=(28,28))
        self.imgCancelar = CTkImage(dark_image=Image.open(leerImagen('Cancelar')),size=(28,28))

        self.transient(master)
        self.lift()
        self.crearWidgets()


    def fnGuardarCompra(self):
        #Función botón guardar
        
        fecha=date.today() #Se optiene fecha actual

        #Se crea objeto para inserción de información
        objGuardarCompra= ComprasController(None
                                            ,self.etDescribcionCompra.get()
                                            ,fecha)
        #Se optiene el status de inserción
        control = objGuardarCompra.insertarCompras()

        if control[0]==1:
            #Se muestra mensaje de inserción

            mss.mensajeInformativo(control[1])
            self.etDescribcionCompra.delete(0,'end')
        if control[0]==0:
            #Se muestra mensaje de error

            mss.mensajeError(control[1])

    def fnCancelar(self):
        #Función botón cancelar
        self.destroy()


    def crearWidgets(self):
        #Crea lo widgets necesarios para registrar las compras

        self.fmRegistroCompra = CTkFrame(self
                                         ,fg_color=color['fg_color']
                                         )
        self.fmRegistroCompra.pack(padx=reCom['fmRegistroCompraPadX']
                                   ,pady=reCom['fmRegistroCompraPadY']
                                   )
        #Label describcion compra
        self.lbDescribcionCompra = CTkLabel(self.fmRegistroCompra
                                            ,text= 'Describción Compra'
                                            ,fg_color=color['bgLabels']
                                            ,font=(fuente['Fuente'],fuente['tamano'])
                                            ,text_color=color["colorLetrasLabel"]
                                            ,width=reCom['lbDescribcionCompraWidth']
                                            ,height=reCom['lbDescribcionCompraHeight']
                                            ,corner_radius=8
                                            )
        self.lbDescribcionCompra.grid(row=0
                                      ,column=0
                                      ,padx=reCom['padxCompras']
                                      ,pady=reCom['padyCompras']
                                      )
        
        #Label entry describcion compra

        self.etDescribcionCompra = CTkEntry(self.fmRegistroCompra
                                            ,fg_color=color["bgEntrys"]
                                            ,font=(fuente["Fuente"],fuente["tamano"])
                                            ,text_color=color["colorLetrasEntry"]
                                            ,justify='center'                             
                                            ,width=reCom['etDescribcionCompraWidth']
                                            ,height=reCom['etDescribcionCompraHeight']
                                            ,corner_radius=8
                                            )
        self.etDescribcionCompra.grid(row=0
                                      ,column=1
                                      ,padx=reCom['padxCompras']
                                      ,pady=reCom['padyCompras']
                                      )
        
        #Boton Guardar
        self.btnGuardarCompras=CTkButton(self.fmRegistroCompra 
                                           ,text='    Guardar'
                                           ,fg_color=color["bgBotones"]
                                           ,font=(fuente["Fuente"],fuente["tamano"])
                                           #,text_color=color["ColorLetras"]
                                           ,command=self.fnGuardarCompra
                                           ,image=self.imgGuardar
                                           ,cursor=maus["cursor"]
                                           ,compound=maus["compound"]
                                           )
        self.btnGuardarCompras.grid(row=1
                                    ,column=0
                                    ,padx=reCom['padxCompras']
                                    ,pady=reCom['padyCompras']
                                    )

        #Boton cancelar
        self.btnCancelarFactura=CTkButton(self.fmRegistroCompra
                                       ,text='Cancelar O Salir'
                                       ,fg_color=color["bgBotones"]
                                       ,font=(fuente["Fuente"],fuente["tamano"])
                                       #,text_color=color["ColorLetras"]
                                       ,command=self.fnCancelar
                                       ,image=self.imgCancelar
                                       ,cursor=maus["cursor"]
                                       ,compound=maus["compound"]
                                       )
        self.btnCancelarFactura.grid(row=1
                                    ,column=1
                                    ,padx=reCom['padxCompras']
                                    ,pady=reCom['padyCompras']
                                    )
        

        
        self.bind('<Return>', self.fnEventoEnter)#Llamada a evento

    def fnEventoEnter(self,event):
        #Evento para guardar con tecla enter
        try:
            self.fnGuardarCompra()
        except:
            pass