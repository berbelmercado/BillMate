from customtkinter import CTk,CTkFrame
from views.vwImgConfig import leerImagen as img
from views import configuracionesGenerales as conGen

class VentanaPrincipal(CTk):
    #Creamos la ventana principal
    def __init__ (self):

        super().__init__()
        #calculamos el ancho y alto de la ventana de la máquina
        self.__anchoDePantalla=self.winfo_screenwidth()
        self.__altoDePantalla=self.winfo_screenheight()
        self.geometry(f"{self.__anchoDePantalla-190}x{self.__altoDePantalla-160}+100+30")
        
        #Frame PrincipalGlobal
        self.frameGlogal = CTkFrame(self
                                    ,fg_color='#202020'
                                    ,width=self.__anchoDePantalla-192
                                    ,height=self.__altoDePantalla-162
                                    )
        self.frameGlogal.place(x=0
                               ,y=0)
        #Titulo de la ventana principal
        self.title("Bill Mate")
        #configuraciones de color general
        #self._set_appearance_mode("dark")
        




