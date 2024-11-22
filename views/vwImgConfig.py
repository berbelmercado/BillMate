from pathlib import Path
import os
import sys

#Este diccionario contiene las rutas a las imagenes usadas en los botones de registros y consultas etc
dict_rutaImagenes={"Registrar":"img/registrarse-pequeno.png"
                  ,"Consultar":"img/lupa.png"
                  ,"Guardar":"img/guardar-el-archivo.png"
                  ,"Calendario":"img/calendario.png"
                  ,"Cancelar":"img/cancelar.png"
                  ,"Agregar":"img/anadir.png"
                  ,"Eliminar":"img/eliminar.png"
                  ,"Actualizar":"img/actualizar-flecha.png"
                  ,"Limpiar":"img/escoba.png"
                  ,"Logo":"img/Logo.ico"
                  ,"imgLogo":"img/imgLogo.png"
                  ,"cargar":"img/agregar-archivo.png"
}    

#Esta función es la que envía la imagen a los botones recibe por parámetro la imagen que requiere el botón
def leerImagen(imagenRequerida):
        imagen=str(Path(resource_path(dict_rutaImagenes[imagenRequerida])))
        return str(imagen)

def resource_path(relative_path):
        try:
                base_path = sys._MEIPASS
        except Exception:
                base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)




