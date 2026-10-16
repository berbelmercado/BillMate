import sqlite3
from model.rutas import ruta_base_datos

class ConexionDb:
    #constructor de conexión a la base de datos
    def __init__(self):
        self.dataBase = ruta_base_datos() #ruta de la base de datos, ver model/rutas.py
        self.conexion = sqlite3.connect(self.dataBase)
        self.cursor = self.conexion.cursor()

    def desconectar(self):
        self.conexion.commit() #Realiza cambio en la base de datos
        self.cursor.close()
        self.conexion.close() #Cierra la conexión

