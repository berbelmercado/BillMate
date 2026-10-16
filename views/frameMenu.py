"""Barra lateral de la ventana principal: logo, acción principal y accesos a registros y consultas"""
from customtkinter import CTkFrame,CTkButton,CTkImage,CTkLabel
from PIL import Image
from views import configuracionesGenerales as conGen
from views.configuracionesGenerales import dicTemaInicio as tema
from views.configuracionesGenerales import dicConfigInicio as conIni
from views.vwImgConfig import leerImagen
from views.ventanasSecundarias import registrarFactura as rf
from views.ventanasSecundarias import registrarComercio as rc
from views.ventanasSecundarias import registrarProductos as rp
from views.ventanasSecundarias import nuevaCompra as nc
from views.ventanasSecundarias import consultarProductos as cp
from views.ventanasSecundarias import consultarMercados as cm
from views.ventanasSecundarias import consultarFacturas as cf
from views.ventanasSecundarias import consultarComercios as cc
from views.ventanasSecundarias import registrarCompras as rcp
from views.ventanasSecundarias import consultarCompras as conCom
from views.messagebox import mensajesEmergentes as mss
from controller.crearBdController import abrirCarpetaDatosController

class FrameMenu(CTkFrame):

    #Barra lateral; se ubica en la columna 0 del contenedor de la ventana principal
    def __init__(self,master):
        super().__init__(master
                         ,fg_color=tema["lateral"]
                         ,corner_radius=0
                         ,width=conIni["anchoLateral"])
        self.master=master
        self.grid(row=0, column=0, sticky='ns')
        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=1)
        self.crearWidgets()

    def mostrarVentanaRegistrarFactura(self):
        #muestra la ventana secundaria para registrar factura
        ventanaRegistrarFactura=rf.RegistrarFactura(self.master)

    def mostrarVentanaRegistrarComercio(self):
        #muestra la ventana secundaria para registrar comercio
        ventanaRegistrarComercio=rc.RegistrarComercio(self.master)

    def mostrarVentanaRegistrarProducto(self):
        #ventana secundaria registrar producto
        ventanaRegistrarProducto=rp.RegistrarProductos(self.master)

    def mostrarVentanaAgregarMercado(self):
        #ventana secundaria registrar mercado
        ventanaAgregarMercado=nc.NuevaCompra(self.master)

    def mostrarVentanaconsultarProductos(self):
        #ventana secundaria consultar productos
        ventanaConsultarProducto=cp.ConsultarProductos(self.master)

    def mostrarVentanaConsultarFacturas(self):
        ventanaConsultarFacturas= cf.ConsultarFacturas(self.master)

    def mostrarVentanaConsultarMercados(self):
        #ventana secundaria consultar mercados
        ventanaConsultarMercados=cm.ConsultarMercados(self.master)

    def mostrarVentanaConsultarComercios(self):
        #ventana secundaria consultar comercios
        ventanaConsultarComercios=cc.ConsultarComercios(self.master)

    def mostrarVentanaRegistrarCompras(self):
        #Ventana secundaria registrar compra
        ventanaRegistrarCompras = rcp.RegistrarCompras(self.master)

    def mostrarVentanaConsultarCompras(self):
        #Ventana secundaria registrar compra
        ventanaConsultarCompras = conCom.ConsultarCompras(self.master)

    def abrirCarpetaDatos(self):
        #Abre la carpeta donde está guardada la base de datos
        mensaje = abrirCarpetaDatosController()
        if mensaje[0] == 0:
            mss.mensajeError(mensaje[1])

    def icono(self, nombre, tamano):
        imagen = Image.open(leerImagen(nombre))
        return CTkImage(light_image=imagen, dark_image=imagen, size=(tamano, tamano))

    def fuente(self, tamano, peso='normal'):
        return (conIni["fuente"], tamano, peso)

    def botonLateral(self, fila, texto, comando, imagen):
        #Botón plano alineado a la izquierda, que se resalta al pasar el mouse
        boton = CTkButton(self
                          ,text=texto
                          ,command=comando
                          ,image=imagen
                          ,compound='left'
                          ,anchor='w'
                          ,fg_color='transparent'
                          ,hover_color=tema["botonHover"]
                          ,text_color=tema["texto"]
                          ,font=self.fuente(conIni["tamanoBoton"])
                          ,height=conIni["altoBoton"]
                          ,corner_radius=conIni["radioBoton"]
                          ,cursor=conGen.dicConfig["cursor"])
        boton.grid(row=fila, column=0, sticky='ew', padx=conIni["padY"], pady=1)
        return boton

    def seccion(self, fila, texto):
        CTkLabel(self
                 ,text=texto
                 ,text_color=tema["textoSuave"]
                 ,font=self.fuente(conIni["tamanoSeccion"], 'bold')
                 ,height=conIni["altoSeccion"]
                 ,anchor='w').grid(row=fila, column=0, sticky='ew', padx=conIni["padX"] + 4, pady=(conIni["padY"], 2))

    def crearWidgets(self):
        iconoRegistrar = self.icono("Registrar", conIni["iconoTamano"])
        iconoConsultar = self.icono("Consultar", conIni["iconoTamano"])

        #Logo y nombre
        CTkLabel(self
                 ,text='  BillMate'
                 ,image=self.icono("imgLogo", conIni["logoTamano"])
                 ,compound='left'
                 ,text_color=tema["texto"]
                 ,font=self.fuente(conIni["tamanoNombreApp"], 'bold')
                 ,anchor='w').grid(row=0, column=0, sticky='ew', padx=conIni["padX"], pady=(conIni["padX"] - 2, conIni["padY"] // 2))

        #Acción principal
        CTkButton(self
                  ,text='Agregar Mercados'
                  ,command=self.mostrarVentanaAgregarMercado
                  ,image=self.icono("Agregar", conIni["iconoTamano"])
                  ,compound='left'
                  ,fg_color=tema["acento"]
                  ,hover_color=tema["acentoHover"]
                  ,text_color='white'
                  ,font=self.fuente(conIni["tamanoBoton"], 'bold')
                  ,height=conIni["altoBotonPrincipal"]
                  ,corner_radius=conIni["radioBoton"]
                  ,cursor=conGen.dicConfig["cursor"]).grid(row=1, column=0, sticky='ew', padx=conIni["padX"], pady=conIni["padY"] // 2)

        fila = 2
        for titulo, icono, botones in (('REGISTRAR', iconoRegistrar, (('Facturas', self.mostrarVentanaRegistrarFactura)
                                                                      ,('Comercios', self.mostrarVentanaRegistrarComercio)
                                                                      ,('Productos', self.mostrarVentanaRegistrarProducto)
                                                                      ,('Compras', self.mostrarVentanaRegistrarCompras)))
                                       ,('CONSULTAR', iconoConsultar, (('Mercados', self.mostrarVentanaConsultarMercados)
                                                                       ,('Productos', self.mostrarVentanaconsultarProductos)
                                                                       ,('Facturas', self.mostrarVentanaConsultarFacturas)
                                                                       ,('Comercios', self.mostrarVentanaConsultarComercios)
                                                                       ,('Compras', self.mostrarVentanaConsultarCompras)))):
            self.seccion(fila, titulo)
            fila += 1
            for texto, comando in botones:
                self.botonLateral(fila, f'  {texto}', comando, icono)
                fila += 1

        #La fila vacía empuja "Carpeta de datos" al pie de la barra
        self.grid_rowconfigure(fila, weight=1)
        carpeta = self.botonLateral(fila + 1, '  Carpeta de datos', self.abrirCarpetaDatos, self.icono("Guardar", conIni["iconoTamano"]))
        carpeta.grid_configure(pady=(0, conIni["padY"]))
