from tkinter import messagebox

def mensajeInformativo(mensaje):
    #mensaje de exito
    messagebox.showinfo(title='Información',message=mensaje)

def mensajeError(mensaje):
    #muestra mensajes de error
    messagebox.showerror(title='Error',message=mensaje)