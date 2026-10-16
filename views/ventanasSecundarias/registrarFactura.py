from PIL import  Image
from customtkinter import CTkToplevel,CTkLabel,CTkEntry,CTkButton,CTkFrame,CTkImage
from tkcalendar import Calendar
from views.ventanasSecundarias import configuracionVentanasSecundarias as conSec
from views.configuracionesGenerales import dicConfiguracionGeneralColores as conColor
from views.configuracionesGenerales import dicConfiguracionGeneralFuentes as conFuente
from views.configuracionesGenerales import dicConfig as conMaus
from  views.vwImgConfig import leerImagen
from controller import facturasController
from views.messagebox import mensajesEmergentes as mss

class RegistrarFactura(CTkToplevel):
   #constructor
    def __init__(self,master):
        super().__init__(master) #llamamos el constructor de la clase Toplevel
        self.master=master
        self.fg_color=conColor["fg_color"] 
        self.geometry(f"{conSec.dicConfigRegistrarFactura["vpWidth"]}x{conSec.dicConfigRegistrarFactura["vpHeight"]}+{conSec.dicConfigPosicion["vnregistrarFacturaX"]}+{conSec.dicConfigPosicion["vnRegistrarFacturaY"]}")
        self.title("Registrar Facturas")
        #se importan las imagenes que se insertan en los botones
        self.imagenGuardar=CTkImage(dark_image=Image.open(leerImagen("Guardar")),size=(28,28))
        self.imagenCalendario=CTkImage(dark_image=Image.open(leerImagen("Calendario")),size=(28,28))
        self.imagenCancelar=CTkImage(dark_image=Image.open(leerImagen("Cancelar")),size=(28,28))
        self.resizable(False,False)
        # Ponerla encima de las demás
        self.transient(master)
        self.lift()
        self.crearWidget()
    
    def capturarFechaFactura(self):
        
        #Funcionalidad del botón que guarda la fecha después de ser seleccionada en el calendario
        self.etFechaSeleccionadavp.configure(state='normal'
                                         ,fg_color=conColor["bgEntrys"]
                                         ,text_color=conColor["colorLetrasEntry"]
                                        )
        self.etFechaSeleccionadavp.delete(0,'end')
        self.etFechaSeleccionadavp.insert(0,self.clFechaFactura.get_date())
        self.etFechaSeleccionadavp.configure(state='disabled')
        self.venCalendario.destroy()

    def insertarFechaEntry(self):
        #muestra una nueva mentana con el calendario
        self.venCalendario=CTkToplevel(self)
        self.venCalendario.title("Ingresar Fecha")
        self.venCalendario.transient(self)
        self.venCalendario.grab_set()
        width=conSec.dicConfigRegistrarFactura["vcWidth"]
        height=conSec.dicConfigRegistrarFactura["vcHeight"]
        bg=conSec.dicConfigRegistrarFactura["vcBg"]

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
                                        ,fg_color=conColor["bgBotones"]
                                        ,font=(conFuente["Fuente"],conFuente["tamano"])
                                        #,fg=conColor["ColorLetras"]
                                        #,image=self.imagenGuardar
                                        ,command=self.capturarFechaFactura
                                        ,cursor=conMaus["cursor"]
                                        ,compound=conMaus["compound"]
                                        ,width=conSec.dicConfigRegistrarFactura["btnCalWidth"]
                                        )
        self.btnSeleccionarFecha.pack(pady=conSec.dicConfigRegistrarFactura["btCalPady"]
                                      ,)
    
    def btnCancelar(self):
        #Funcionalidad botóon cancelar
        self.destroy()

    def btnGuardar(self):
        insertarFactura=facturasController.insertarFactura(self.etNumeroFactura.get()
                                                           ,self.etIngresarTotalFactura.get()
                                                           ,self.etFechaSeleccionadavp.get())

        if insertarFactura[0]==0 or insertarFactura[0]==2:
            mss.mensajeError(insertarFactura[1])
            self.focus()

        if insertarFactura[0]==1:
            mss.mensajeInformativo(insertarFactura[1])
                    #limpiar campos
            self.etNumeroFactura.delete(0,'end')
            self.etIngresarTotalFactura.delete(0,'end')
            self.etFechaSeleccionadavp.configure(state='normal'
                                                ,fg_color=conColor["bgEntrys"]
                                                ,text_color=conColor["colorLetrasEntry"]
                                            )
            self.etFechaSeleccionadavp.delete(0,'end')
        
    def crearWidget(self):
        #Frame Principal
        self.fmPrincipal= CTkFrame(self
                                ,width=conSec.dicConfigRegistrarFactura["fmWidth"]
                                ,height=conSec.dicConfigRegistrarFactura["fmHeight"]
                                ,fg_color=conColor["fg_color"]
                                )
        self.fmPrincipal.place(x=conSec.dicConfigRegistrarFactura["fmX"]
                              ,y=conSec.dicConfigRegistrarFactura["fmY"]
                              )

        #Label Numero de factura
        self.lbNumeroFactura=CTkLabel(self.fmPrincipal
                                       ,text="Ingrese Número de Factura"
                                       ,fg_color=conColor["bgLabels"]
                                       ,font=(conFuente["Fuente"],conFuente["tamano"])
                                       ,width=conSec.dicConfigRegistrarFactura["lbNumeroFacturaWidth"]
                                       ,height=conSec.dicConfigRegistrarFactura["lbNumeroFacturaHeight"]
                                       ,corner_radius=conMaus["corner_radius"]
                                       ,text_color=conColor["colorLetrasLabel"]
                                       )
        self.lbNumeroFactura.place(x=conSec.dicConfigRegistrarFactura["lbNumeroFacturaX"]
                                   ,y=conSec.dicConfigRegistrarFactura["lbNumeroFacturaY"]
                                   )
        #Entry Número de factura
        self.etNumeroFactura=CTkEntry(self.fmPrincipal
                                      ,fg_color=conColor["bgEntrys"]
                                      ,font=(conFuente["Fuente"],conFuente["tamano"])
                                      ,justify='center'
                                      ,width=conSec.dicConfigRegistrarFactura["etNumeroFacturaWidth"]
                                      ,height=conSec.dicConfigRegistrarFactura["etNumeroFacturaHeight"]
                                      ,corner_radius=conMaus["corner_radius"]
                                      ,text_color=conColor["colorLetrasEntry"]
                                     )
        self.etNumeroFactura.place(x=conSec.dicConfigRegistrarFactura["etNumeroFacturaX"]
                                     ,y=conSec.dicConfigRegistrarFactura["etNumeroFacturaY"]
                                     )
        
        #Label Total Factura
        self.lbIngresarTotalFactura=CTkLabel(self.fmPrincipal
                                            ,text="Ingrese el Valor Total de la Factura"
                                            ,fg_color=conColor["bgLabels"]
                                            ,font=(conFuente["Fuente"],conFuente["tamano"])
                                            ,corner_radius=conMaus["corner_radius"]
                                            ,width=conSec.dicConfigRegistrarFactura["lbIngresarTotalFacturaWidth"]
                                            ,height=conSec.dicConfigRegistrarFactura["lbIngresarTotalFacturaHeight"]
                                            ,text_color=conColor["colorLetrasLabel"]
                                            )
        self.lbIngresarTotalFactura.place(x=conSec.dicConfigRegistrarFactura["lbIngresarTotalFacturaX"]
                                          ,y=conSec.dicConfigRegistrarFactura["lbIngresarTotalFacturaY"]
                                          )
        #Entry Total Factura
        self.etIngresarTotalFactura=CTkEntry(self.fmPrincipal
                                            ,fg_color=conColor["bgEntrys"]
                                            ,font=(conFuente["Fuente"],conFuente["tamano"])
                                            ,justify='center'
                                            ,corner_radius=conMaus["corner_radius"]
                                            ,width=conSec.dicConfigRegistrarFactura["etIngresarTotalFacturaWidth"]
                                            ,height=conSec.dicConfigRegistrarFactura["etIngresarTotalFacturaHeight"]
                                            ,text_color=conColor["colorLetrasEntry"]
                                            )
        self.etIngresarTotalFactura.place(x=conSec.dicConfigRegistrarFactura["etIngresarTotalFacturaX"]
                                          ,y=conSec.dicConfigRegistrarFactura["etIngresarTotalFacturaY"]
                                         )
        #Boton Fecha Factura
        self.btnIngresarFechaFactura=CTkButton(self.fmPrincipal
                                           ,text='  Ingresar Fecha'
                                           ,fg_color=conColor["bgBotones"]
                                          ,font=(conFuente["Fuente"],conFuente["tamano"])
                                           ,command=self.insertarFechaEntry
                                           ,image=self.imagenCalendario
                                           ,cursor=conMaus["cursor"]
                                           ,compound=conMaus["compound"]
                                           ,width=conSec.dicConfigRegistrarFactura["btnIngresarFechaFacturaWidth"]
                                           ,height=conSec.dicConfigRegistrarFactura["btnIngresarFechaFacturaHeight"]
                                           )
        self.btnIngresarFechaFactura.place(x=conSec.dicConfigRegistrarFactura["btnIngresarFechaFacturaX"]
                                          ,y=conSec.dicConfigRegistrarFactura["btnIngresarFechaFacturaY"]
                                          )
        
        #Entry Fecha Seleccionada
        self.etFechaSeleccionadavp=CTkEntry(self.fmPrincipal
                                           ,font=(conFuente["Fuente"],conFuente["tamano"])
                                           ,state='disabled'
                                           ,justify='center'
                                           ,width=conSec.dicConfigRegistrarFactura["etFechaSeleccionadavpWidth"]
                                           ,height=conSec.dicConfigRegistrarFactura["etFechaSeleccionadavpHeight"]
                                           )
        self.etFechaSeleccionadavp.place(x=conSec.dicConfigRegistrarFactura["etFechaSeleccionadavpX"]
                                          ,y=conSec.dicConfigRegistrarFactura["etFechaSeleccionadavpY"]

                                         )
        
        #Boton Guardar
        self.btnGuardarFactura=CTkButton(self.fmPrincipal 
                                           ,text='    Guardar'
                                           ,fg_color=conColor["bgBotones"]
                                           ,font=(conFuente["Fuente"],conFuente["tamano"])
                                           #,fg=conColor["ColorLetras"]
                                           ,command=self.btnGuardar
                                           ,image=self.imagenGuardar
                                           ,cursor=conMaus["cursor"]
                                           ,compound=conMaus["compound"]
                                           ,width=conSec.dicConfigRegistrarFactura["btnGuardarFacturaxWidth"]
                                           ,height=conSec.dicConfigRegistrarFactura["btnGuardarFacturaxHeight"]
                                           )
        self.btnGuardarFactura.place(x=conSec.dicConfigRegistrarFactura["btnGuardarFacturaX"]
                                     ,y=conSec.dicConfigRegistrarFactura["btnGuardarFacturaY"]
                                     )
        #Boton cancelar
        self.btnCancelarFactura=CTkButton(self.fmPrincipal
                                       ,text='Cancelar O Salir'
                                       ,fg_color=conColor["bgBotones"]
                                       ,font=(conFuente["Fuente"],conFuente["tamano"])
                                       #,fg=conColor["ColorLetras"]
                                       ,command=self.btnCancelar
                                       ,image=self.imagenCancelar
                                       ,cursor=conMaus["cursor"]
                                       ,compound=conMaus["compound"]
                                       ,width=conSec.dicConfigRegistrarFactura["btnbtnCancelarFacturaWidth"]
                                       ,height=conSec.dicConfigRegistrarFactura["btnbtnCancelarFacturaHeight"]
                                       )
        self.btnCancelarFactura.place(x=conSec.dicConfigRegistrarFactura["btnCancelarFacturaX"]
                                     ,y=conSec.dicConfigRegistrarFactura["btnbtnCancelarFacturaY"]
                                     )
        self.bind('<Return>', self.fnEventoEnter)#Llamada a evento

    def fnEventoEnter(self,event):
        #Evento para guardar con tecla enter
        try:
            self.btnGuardar()
        except:
            pass