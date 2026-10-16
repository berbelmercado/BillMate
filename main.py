# Importaciones
from views import ventanaPrincipal as vp
from views import frameMenu as fm
from views import frameListasTreview as trv
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

        # Añade el menú y la vista de lista a la ventana principal
        fm.FrameMenu(master=raiz.frameGlogal)
        trv.TreviewUltimoMercado(master=raiz.frameGlogal)

        # Inicia el bucle principal de la interfaz gráfica
        raiz.mainloop()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")


if __name__ == "__main__":
    main()
