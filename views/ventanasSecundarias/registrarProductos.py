from PIL import Image
from customtkinter import CTkToplevel,CTkLabel,CTkButton,CTkFrame,CTkEntry,CTkImage
from views.ventanasSecundarias import configuracionVentanasSecundarias as conSec
from views.configuracionesGenerales import dicConfiguracionGeneralColores as conColor
from views.configuracionesGenerales import dicConfiguracionGeneralFuentes as conFuente
from views.configuracionesGenerales import dicConfig as conMaus
from views.vwImgConfig import leerImagen
from controller.productosController import ProductosController
from views.messagebox import mensajesEmergentes as msbx


class RegistrarProductos(CTkToplevel):
    #Clase para view registro de productos
    def __init__(self,master):
        super().__init__(master)
        self.master=master
        self.geometry(f"{conSec.dicConfigRegistrarProducto["vpWidth"]}x{conSec.dicConfigRegistrarProducto["vpHeight"]}+{conSec.dicConfigPosicion["vnregistrarProductosX"]}+{conSec.dicConfigPosicion["vnRegistrarProductosY"]}")
        self.title("Registrar Productos")
        #se importan las imagenes que se insertan en los botones
        self.imagenGuardar=CTkImage(dark_image=Image.open(leerImagen("Guardar")),size=(28,28))
        self.imagenCancelar=CTkImage(dark_image=Image.open(leerImagen("Cancelar")),size= (28,28))
        self.resizable(False,False)    
        #self.grab_set()
        self.wm_attributes("-topmost", 1)
        self.crearWidget()

    def validaVentana(self):
        if self.winfo_exists() == True:
            self.btnCancelar()

    def btnCancelar(self):
        #Funcionalidad botóon cancelar
        self.destroy()

    def btnGuardar(self):
        productos = ProductosController(None
                              ,self.etIngresarNombreProducto.get()
                              )
        mensaje=productos.insertarProducto()
        if mensaje[0]==1:
            msbx.mensajeInformativo(mensaje[1])
        if mensaje[0]==0:
            msbx.mensajeError(mensaje[1])

        self.etIngresarNombreProducto.delete(0,'end')

    def crearWidget(self):
        #Frame 
        self.fmPrincipalRegistrarProducto= CTkFrame(self
                                                    ,width=conSec.dicConfigRegistrarProducto["fmWidth"]
                                                    ,height=conSec.dicConfigRegistrarProducto["fmHeight"]
                                                    ,fg_color=conColor["fg_color"]
                                                    )
        self.fmPrincipalRegistrarProducto.place(x=conSec.dicConfigRegistrarProducto["fmX"]
                                                ,y=conSec.dicConfigRegistrarProducto["fmY"]
                                                )
        #Label Nombre Producto
        self.lbIngresarNombreProducto=CTkLabel(self.fmPrincipalRegistrarProducto
                                               ,text="Ingrese Nombre del Producto"
                                               ,fg_color=conColor["bgLabels"]
                                               ,text_color=conColor["colorLetrasLabel"]
                                               ,font=(conFuente["Fuente"],conFuente["tamano"])
                                               ,width=conSec.dicConfigRegistrarProducto["lbNomberProductoWidth"]
                                               ,height=conSec.dicConfigRegistrarProducto["lbNombreProductoHeight"]
                                               ,corner_radius=8
                                                )
        self.lbIngresarNombreProducto.place(x=conSec.dicConfigRegistrarProducto["lbNombreProductoX"]
                                            ,y=conSec.dicConfigRegistrarProducto["lbNombreProductoY"]
                                           )
        #Entry Nombre Producto
        self.etIngresarNombreProducto=CTkEntry(self.fmPrincipalRegistrarProducto
                                               ,fg_color=conColor["bgEntrys"]
                                               ,font=(conFuente["Fuente"],conFuente["tamano"])
                                               ,text_color=conColor["colorLetrasEntry"]
                                               ,justify='center'
                                               ,corner_radius=8
                                               ,width=conSec.dicConfigRegistrarProducto["etNombreProductoWidth"]
                                               ,height=conSec.dicConfigRegistrarProducto["etNombreProductoHeight"]
                                               )
        self.etIngresarNombreProducto.place(x=conSec.dicConfigRegistrarProducto["etNombreProductoX"]
                                       ,y=conSec.dicConfigRegistrarProducto["etNombreProductoY"]
                                       )    

        #Boton Guardar   
        self.btnGuardarProducto=CTkButton(self.fmPrincipalRegistrarProducto
                                         ,text='Guardar'
                                         ,fg_color=conColor["bgBotones"]
                                         ,font=(conFuente["Fuente"],conFuente["tamano"])
                                         #,text_color=conColor["ColorLetras"]
                                         ,command=self.btnGuardar
                                         ,image=self.imagenGuardar
                                         ,cursor=conMaus["cursor"]
                                         ,compound=conMaus["compound"]
                                         ,width=conSec.dicConfigRegistrarProducto["btnGuardarProductoWidth"]
                                         ,height=conSec.dicConfigRegistrarProducto["btnGuardarProductoHeight"]
                                         )
        self.btnGuardarProducto.place(x=conSec.dicConfigRegistrarProducto["btnGuardarProductoX"]
                                        ,y=conSec.dicConfigRegistrarProducto["btnGuardarProductoY"]
                                        )
        
        #Boton Cancelar
        self.btnCancelarRegistroProducto=CTkButton(self.fmPrincipalRegistrarProducto
                                                   ,text='Cancelar O Salir'
                                                   ,fg_color=conColor["bgBotones"]
                                                   ,font=(conFuente["Fuente"],conFuente["tamano"])
                                                   #,text_color=conColor["ColorLetras"]
                                                   ,command=self.btnCancelar
                                                   ,image=self.imagenCancelar
                                                   ,cursor=conMaus["cursor"]
                                                   ,compound=conMaus["compound"]
                                                   ,width=conSec.dicConfigRegistrarProducto["btnCancelarProductoWidth"]
                                                   ,height=conSec.dicConfigRegistrarProducto["btnCancelarProductoHeight"]
                                                   )
        self.btnCancelarRegistroProducto.place(x=conSec.dicConfigRegistrarProducto["btnCancelarProductoX"]
                                        ,y=conSec.dicConfigRegistrarProducto["btnCancelarProductoY"]
                                        ) 
        
        self.etIngresarNombreProducto.bind('<Return>', self.fnEventoEnter)#Llamada a evento

    def fnEventoEnter(self,event):
        #Evento para guardar con tecla enter
        try:
            self.btnGuardar()
        except:
            pass