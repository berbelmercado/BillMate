from customtkinter import CTk,CTkFrame
from views.vwImgConfig import leerImagen
from views.configuracionesGenerales import dicTema as tema
from views.configuracionesGenerales import dicConfigInicio as conIni
from views.componentes import prepararEstiloTablas


class VentanaPrincipal(CTk):
    #Ventana principal: barra lateral (FrameMenu) en la columna 0 y la página visible en la 1
    def __init__ (self):

        super().__init__(fg_color=tema["fondo"])
        ancho = self.winfo_screenwidth() - conIni["margenAncho"]
        alto = self.winfo_screenheight() - conIni["margenAlto"]
        self.geometry(f'{ancho}x{alto}+{conIni["vnX"]}+{conIni["vnY"]}')
        self.minsize(conIni["vnMinWidth"], conIni["vnMinHeight"])
        self.title("Bill Mate")
        self.iconbitmap(leerImagen("Logo"))
        prepararEstiloTablas()

        #Contenedor que llena la ventana; es el master de la barra lateral y de las páginas
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.frameGlogal = CTkFrame(self, fg_color=tema["fondo"], corner_radius=0)
        self.frameGlogal.grid(row=0, column=0, sticky='nsew')
        self.frameGlogal.grid_columnconfigure(1, weight=1)
        self.frameGlogal.grid_rowconfigure(0, weight=1)

        self.fabricas = {}      #nombre de página -> clase; se registran en main.py
        self.paginas = {}       #páginas ya creadas
        self.menu = None        #barra lateral, para resaltar el botón de la página visible
        self.paginaActual = None

    def registrarPaginas(self, fabricas):
        self.fabricas.update(fabricas)

    def mostrar(self, nombre):
        #Muestra la página en la columna derecha (la crea la primera vez) y oculta la anterior
        if nombre not in self.paginas:
            self.paginas[nombre] = self.fabricas[nombre](self.frameGlogal)
        pagina = self.paginas[nombre]
        if self.paginaActual is not None and self.paginaActual is not pagina:
            self.paginaActual.grid_forget()
        pagina.grid(row=0, column=1, sticky='nsew')
        self.paginaActual = pagina
        if self.menu is not None:
            self.menu.marcarActivo(nombre)
        pagina.refrescar()
