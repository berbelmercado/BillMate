import sqlite3
import os
import sys

class ConexionDb:
    #constructor de conexión a la base de datos
    def __init__(self):
        self.dataBase = self.resource_path('Database\\BillMate.db') #ruta de la base de datos si no existe se crea en la carpeta Database
        self.conexion = sqlite3.connect(self.dataBase)
        self.cursor = self.conexion.cursor()

    def desconectar(self):
        self.conexion.commit() #Realiza cambio en la base de datos
        self.cursor.close()
        self.conexion.close() #Cierra la conexión

    def resource_path(self,relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

