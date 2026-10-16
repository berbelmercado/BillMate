# Importaciones
from views import ventanaPrincipal as vp
from views import frameMenu as fm
from views.paginas.inicio import PanelInicio
from views.paginas.datos import PaginaProductos, PaginaFacturas, PaginaComercios, PaginaCompras
from views.paginas.mercados import PaginaMercados
from views.paginas.compra import PaginaCompra
from views.messagebox import mensajesEmergentes
from controller import crearBdController


def main():
    """
    Función principal que inicializa la aplicación.
    Valida si existe la base de datos, si no existe la crea,
    y luego inicializa la interfaz gráfica.
    """
    try:
        # Valida si existe la base de datos, si no existe la crea
        crearBdController.existeBase()

        # Inicializa la ventana principal
        raiz = vp.VentanaPrincipal()

        # Páginas que se muestran a la derecha de la barra lateral, y la barra lateral que navega entre ellas
        raiz.registrarPaginas({'inicio': PanelInicio
                               ,'compra': PaginaCompra
                               ,'mercados': PaginaMercados
                               ,'productos': PaginaProductos
                               ,'facturas': PaginaFacturas
                               ,'comercios': PaginaComercios
                               ,'compras': PaginaCompras})
        fm.FrameMenu(master=raiz.frameGlogal, ventana=raiz)
        raiz.mostrar('inicio')

        # Inicia el bucle principal de la interfaz gráfica
        raiz.mainloop()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        #En el ejecutable no hay consola: el error también se muestra en pantalla
        mensajesEmergentes.mensajeError(f"Error al iniciar la aplicación: {e}")


if __name__ == "__main__":
    main()
