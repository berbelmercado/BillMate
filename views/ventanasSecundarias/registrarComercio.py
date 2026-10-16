from customtkinter import CTkToplevel,CTkFrame,CTkLabel,CTkEntry,CTkButton,CTkImage
from PIL import Image
from views.ventanasSecundarias import configuracionVentanasSecundarias as conSec
from views.configuracionesGenerales import dicConfiguracionGeneralColores as conColor
from views.configuracionesGenerales import dicConfiguracionGeneralFuentes as conFuente
from views.configuracionesGenerales import dicConfig as conMaus
from controller import comerciosController
from views.messagebox import mensajesEmergentes as msbx
from  views.vwImgConfig import leerImagen

class RegistrarComercio(CTkToplevel):
   def __init__(self,master):
        super().__init__(master)
        self.fg_color=conColor["fg_color"]
        self.geometry(f"{conSec.dicConfigRegistrarComercio["vpWidth"]}x{conSec.dicConfigRegistrarComercio["vpHeight"]}+{conSec.dicConfigPosicion["vnregistrarComercioX"]}+{conSec.dicConfigPosicion["vnRegistrarComercioY"]}")
        self.title("Registrar Comercios")
        #se importan las imagenes que se insertan en los botones
        self.imagenGuardar=CTkImage(dark_image=Image.open(leerImagen("Guardar")),size=(28,28))
        self.imagenCancelar=CTkImage(dark_image=Image.open(leerImagen("Cancelar")),size=(28,28))
        #self.imagenCancelar=CTkImage(Image.open(imagen.leerImagen("Cancelar")))
        self.resizable(False,False)
        self.master=master
        self.transient(master)
        self.lift()
        self.crearWidget()

   def btnCancelar(self):
        #Funcionalidad botóon cancelar
        self.destroy()
   
   def btnGuardarComercios(self):
       #Funcionalidad para el botón guardar
       validaIsercion = comerciosController.insertarComercio(self.etNombreComercio.get()
                                                            ,self.etDireccionComercio.get())

       #Retorna la validación de los campos
       if validaIsercion[0]==1:
           msbx.mensajeInformativo(validaIsercion[1])
           self.etNombreComercio.delete(0,'end')
           self.etDireccionComercio.delete(0,'end')
       elif validaIsercion[0]==0:
           msbx.mensajeError(validaIsercion[1])

       
   def crearWidget(self):
      #Frame 
      self.fmPrincipalRegistrarComercio= CTkFrame(self,
                                                  width=conSec.dicConfigRegistrarComercio["fmWidth"]
                                                 ,height=conSec.dicConfigRegistrarComercio["fmHeight"]
                                                 ,fg_color=conColor["fg_color"]
                                                  )
      self.fmPrincipalRegistrarComercio.place(x=conSec.dicConfigRegistrarComercio["fmX"]
                              ,y=conSec.dicConfigRegistrarComercio["fmY"]
                              )

      #Label Nombre Comercio
      self.lbIngresarNombreComercio=CTkLabel(self.fmPrincipalRegistrarComercio
                                             ,text="Ingrese Nombre del comercio"
                                             ,fg_color=conColor["bgLabels"]
                                             ,text_color=conColor["colorLetrasLabel"]
                                             ,font=(conFuente["Fuente"],conFuente["tamano"])
                                             ,width=conSec.dicConfigRegistrarComercio["lbNomberComercioWidth"]
                                             ,height=conSec.dicConfigRegistrarComercio["lbNombreComercioHeight"]
                                             ,corner_radius=8
                                             )
      self.lbIngresarNombreComercio.place(x=conSec.dicConfigRegistrarComercio["lbNombreComercioX"]
                                          ,y=conSec.dicConfigRegistrarComercio["lbNombreComercioY"]
                                         )
      

      #Label Direccion Comercio
      self.lbIngresarDireccionComercio=CTkLabel(self.fmPrincipalRegistrarComercio
                                                ,text="Ingrese Dirección Del Comercio"
                                                ,fg_color=conColor["bgLabels"]
                                                ,text_color=conColor["colorLetrasLabel"]
                                                ,font=(conFuente["Fuente"],conFuente["tamano"])
                                                ,width=conSec.dicConfigRegistrarComercio["lbDireccionComercioWidth"]
                                                ,height=conSec.dicConfigRegistrarComercio["lbDireccionComercioHeight"]
                                                ,corner_radius=8
                                                )
      self.lbIngresarDireccionComercio.place(x=conSec.dicConfigRegistrarComercio["lbDireccionComercioX"]
                                     ,y=conSec.dicConfigRegistrarComercio["lbDireccionComercioY"]
                                     )
      
      #Entry Nombre Comercio
      self.etNombreComercio=CTkEntry(self.fmPrincipalRegistrarComercio
                                          ,fg_color=conColor["bgEntrys"]
                                          ,font=(conFuente["Fuente"],conFuente["tamano"])
                                          ,text_color=conColor["colorLetrasEntry"]
                                          ,justify='center'
                                          ,corner_radius=8
                                          ,width=conSec.dicConfigRegistrarComercio["etNombreComercioWidth"]
                                          ,height=conSec.dicConfigRegistrarComercio["etNombreComercioHeight"]
                                          )
      self.etNombreComercio.place(x=conSec.dicConfigRegistrarComercio["etNombreComercioX"]
                                       ,y=conSec.dicConfigRegistrarComercio["etNombreComercioY"]
                                       )     
      
      #Entry Dirección Comercio 
      self.etDireccionComercio=CTkEntry(self.fmPrincipalRegistrarComercio
                                          ,fg_color=conColor["bgEntrys"]
                                          ,font=(conFuente["Fuente"],conFuente["tamano"])
                                          ,text_color=conColor["colorLetrasEntry"]
                                          ,justify='center'
                                          ,corner_radius=8
                                          ,width=conSec.dicConfigRegistrarComercio["etDireccionComercioWidth"]
                                          ,height=conSec.dicConfigRegistrarComercio["etDireccionComercioHeight"]
                                          )
      self.etDireccionComercio.place(x=conSec.dicConfigRegistrarComercio["etDireccionComerioX"]
                                       ,y=conSec.dicConfigRegistrarComercio["etDireccionComercioY"]
                                       )      
      
      #Boton Guardar
      self.btnGuardarFactura=CTkButton(self.fmPrincipalRegistrarComercio
                                       ,text='Guardar'
                                       ,fg_color=conColor["bgBotones"]
                                       ,font=(conFuente["Fuente"],conFuente["tamano"])
                                       #,text_color=conColor["colorLetrasEntry"]
                                       ,command=self.btnGuardarComercios
                                       ,image=self.imagenGuardar
                                       ,cursor=conMaus["cursor"]
                                       ,compound=conMaus["compound"]
                                       ,corner_radius=8
                                       ,width=conSec.dicConfigRegistrarComercio["btnGuardarComercioWidth"]
                                       ,height=conSec.dicConfigRegistrarComercio["btnGuardarComercioHeight"]
                                       )
      self.btnGuardarFactura.place(x=conSec.dicConfigRegistrarComercio["btnGuardarComercioX"]
                                     ,y=conSec.dicConfigRegistrarComercio["btnGuardarComercioY"]
                                     )
      
      #Boton Cancelar
      self.btnCancelarFactura=CTkButton(self.fmPrincipalRegistrarComercio
                                       ,text='Cancelar O Salir'
                                       ,fg_color=conColor["bgBotones"]
                                       ,font=(conFuente["Fuente"],conFuente["tamano"])
                                       #,text_color=conColor["ColorLetras"]
                                       ,command=self.btnCancelar
                                       ,image=self.imagenCancelar
                                       ,cursor=conMaus["cursor"]
                                       ,compound=conMaus["compound"]
                                       ,corner_radius=8
                                       ,width=conSec.dicConfigRegistrarComercio["btnCancelarComercioWidth"]
                                       ,height=conSec.dicConfigRegistrarComercio["btnCancelarComercioHeight"]
                                       )
      self.btnCancelarFactura.place(x=conSec.dicConfigRegistrarComercio["btnCancelarComercioX"]
                                     ,y=conSec.dicConfigRegistrarComercio["btnCancelarComercioY"]
                                     )
      self.bind('<Return>', self.fnEventoEnter)#Llamada a evento

   def fnEventoEnter(self,event):
        #Evento para guardar con tecla enter
        try:
            self.btnGuardar()
        except:
            pass