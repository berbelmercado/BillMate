import tkinter
from tkinter import messagebox,Tk

def ventanaActiva():
    # Ventana de la app que tiene el foco, para que el mensaje salga encima de ella
    raiz = tkinter._default_root
    if raiz is None:
        return None
    try:
        widget = raiz.focus_get()
    except (KeyError, tkinter.TclError):
        widget = None
    return widget.winfo_toplevel() if widget is not None else raiz

def mostrarMensaje(funcion, titulo, mensaje):
    padre = ventanaActiva()
    if padre is not None:
        funcion(title=titulo, message=mensaje, parent=padre)
        return
    # Sin ventana principal (error al arrancar): raíz temporal oculta
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    funcion(title=titulo, message=mensaje, parent=root)
    root.destroy()

def mensajeInformativo(mensaje):
    mostrarMensaje(messagebox.showinfo, 'Información', mensaje)

def mensajeError(mensaje):
    mostrarMensaje(messagebox.showerror, 'Error', mensaje)
