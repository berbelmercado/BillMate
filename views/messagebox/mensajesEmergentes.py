from tkinter import messagebox,Tk

def mensajeInformativo(mensaje):
    # mensaje de éxito, siempre encima
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    messagebox.showinfo(title='Información', message=mensaje, parent=root)
    root.destroy()

def mensajeError(mensaje):
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    messagebox.showerror(title='Error', message=mensaje, parent=root)
    root.destroy()