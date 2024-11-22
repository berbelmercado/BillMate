#Importaciones
from views import ventanaPrincipal as vp 
from views import frameMenu as fm
from views import frameListasTreview as trv
from controller import crearBdController

def main():
     #Valisa si existe la base de datos, si no existe la crea
     crearBdController.existeBase() 
     raiz=vp.VentanaPrincipal() 
     fm.FrameMenu(master=raiz)
     trv.TreviewUltimoMercado(master=raiz)
     raiz.mainloop()

if __name__== "__main__":                
    main()
