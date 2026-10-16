"""Barra lateral de la ventana principal: logo, acción principal y navegación entre páginas"""
from customtkinter import CTkFrame,CTkButton,CTkImage,CTkLabel
from PIL import Image
from views import configuracionesGenerales as conGen
from views.configuracionesGenerales import dicTema as tema
from views.configuracionesGenerales import dicConfigInicio as conIni
from views.vwImgConfig import leerImagen
from views.messagebox import mensajesEmergentes as mss
from controller.crearBdController import abrirCarpetaDatosController

class FrameMenu(CTkFrame):

    #Barra lateral; se ubica en la columna 0 del contenedor de la ventana principal
    def __init__(self,master,ventana):
        super().__init__(master
                         ,fg_color=tema["lateral"]
                         ,corner_radius=0
                         ,width=conIni["anchoLateral"])
        self.master=master
        self.ventana=ventana            #VentanaPrincipal, que muestra las páginas
        self.ventana.menu=self
        self.botonesPagina={}           #nombre de página -> botón, para resaltar la visible
        self.grid(row=0, column=0, sticky='ns')
        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=1)
        self.crearWidgets()

    def abrirCarpetaDatos(self):
        #Abre la carpeta donde está guardada la base de datos
        mensaje = abrirCarpetaDatosController()
        if mensaje[0] == 0:
            mss.mensajeError(mensaje[1])

    def marcarActivo(self, nombre):
        #Resalta el botón de la página visible
        for nombrePagina, boton in self.botonesPagina.items():
            boton.configure(fg_color=tema["botonHover"] if nombrePagina == nombre else 'transparent')

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
        iconoInicio = self.icono("imgLogo", conIni["iconoTamano"])
        iconoConsultar = self.icono("Consultar", conIni["iconoTamano"])
        iconoDatos = self.icono("Registrar", conIni["iconoTamano"])

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
                  ,command=lambda: self.ventana.mostrar('compra')
                  ,image=self.icono("Agregar", conIni["iconoTamano"])
                  ,compound='left'
                  ,fg_color=tema["acento"]
                  ,hover_color=tema["acentoHover"]
                  ,text_color='white'
                  ,font=self.fuente(conIni["tamanoBoton"], 'bold')
                  ,height=conIni["altoBotonPrincipal"]
                  ,corner_radius=conIni["radioBoton"]
                  ,cursor=conGen.dicConfig["cursor"]).grid(row=1, column=0, sticky='ew', padx=conIni["padX"], pady=conIni["padY"] // 2)

        #Cada botón muestra una página (nombre registrado en VentanaPrincipal) o ejecuta un comando
        fila = 2
        for titulo, botones in (('GENERAL', (('Inicio', iconoInicio, 'inicio', None)
                                             ,('Mercados', iconoConsultar, 'mercados', None)))
                                ,('DATOS', (('Productos', iconoDatos, 'productos', None)
                                            ,('Facturas', iconoDatos, 'facturas', None)
                                            ,('Comercios', iconoDatos, 'comercios', None)
                                            ,('Compras', iconoDatos, 'compras', None)))):
            self.seccion(fila, titulo)
            fila += 1
            for texto, icono, pagina, comando in botones:
                if pagina is not None:
                    comando = lambda nombre=pagina: self.ventana.mostrar(nombre)
                boton = self.botonLateral(fila, f'  {texto}', comando, icono)
                if pagina is not None:
                    self.botonesPagina[pagina] = boton
                fila += 1

        #La fila vacía empuja "Carpeta de datos" al pie de la barra
        self.grid_rowconfigure(fila, weight=1)
        carpeta = self.botonLateral(fila + 1, '  Carpeta de datos', self.abrirCarpetaDatos, self.icono("Guardar", conIni["iconoTamano"]))
        carpeta.grid_configure(pady=(0, conIni["padY"]))
