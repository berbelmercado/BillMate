from tkinter import ttk
from customtkinter import CTk,CTkFrame
from views.vwImgConfig import leerImagen
from views import configuracionesGenerales as conGen
from views.configuracionesGenerales import dicTemaInicio as tema
from views.configuracionesGenerales import dicConfigInicio as conIni


def estiloTablas():
    #Estilo de las tablas (ttk.Treeview) de las ventanas secundarias; la de inicio usa 'Inicio.Treeview'
    estilo = ttk.Style()
    estilo.theme_use("clam")
    estilo.configure("Treeview.Heading"
                     ,background=conGen.dicConfiguracionGeneralColores["bgLabels"]
                     ,foreground=conGen.dicConfiguracionGeneralColores["colorLetrasLabel"])
    estilo.configure("Treeview"
                     ,font=(conGen.dicConfiguracionGeneralFuentes["Fuente"],10)
                     ,background=conGen.dicConfiguracionGeneralColores["bgGeneral"]
                     ,fieldbackground=conGen.dicConfiguracionGeneralColores["fg_color"])
    estilo.map('Treeview'
               ,background=[('selected',conGen.dicConfiguracionGeneralColores["ColorLetras"])]
               ,foreground=[('selected',conGen.dicConfiguracionGeneralColores["bgGeneral"])])


class VentanaPrincipal(CTk):
    #Ventana principal: barra lateral (FrameMenu) en la columna 0 y pantalla de inicio (PanelInicio) en la 1
    def __init__ (self):

        super().__init__(fg_color=tema["fondo"])
        ancho = self.winfo_screenwidth() - conIni["margenAncho"]
        alto = self.winfo_screenheight() - conIni["margenAlto"]
        self.geometry(f'{ancho}x{alto}+{conIni["vnX"]}+{conIni["vnY"]}')
        self.minsize(conIni["vnMinWidth"], conIni["vnMinHeight"])
        self.title("Bill Mate")
        self.iconbitmap(leerImagen("Logo"))
        estiloTablas()

        #Contenedor que llena la ventana; es el master de la barra lateral, del inicio y de las ventanas secundarias
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.frameGlogal = CTkFrame(self, fg_color=tema["fondo"], corner_radius=0)
        self.frameGlogal.grid(row=0, column=0, sticky='nsew')
        self.frameGlogal.grid_columnconfigure(1, weight=1)
        self.frameGlogal.grid_rowconfigure(0, weight=1)
