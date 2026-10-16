import sqlite3
from model.rutas import ruta_base_datos

class CursorSeguro(sqlite3.Cursor):
    #Si una sentencia falla, revierte la transacción y cierra la conexión antes de relanzar el error.
    #Sin esto la conexión quedaba abierta a medias y la siguiente escritura fallaba con "database is locked"
    def execute(self, *args):
        try:
            return super().execute(*args)
        except Exception:
            self.connection.rollback()
            self.connection.close()
            raise

class ConexionDb:
    #constructor de conexión a la base de datos
    def __init__(self):
        self.dataBase = ruta_base_datos() #ruta de la base de datos, ver model/rutas.py
        self.conexion = sqlite3.connect(self.dataBase)
        self.cursor = self.conexion.cursor(factory=CursorSeguro)
        self.cursor.execute('PRAGMA foreign_keys = ON') #SQLite no valida las claves foráneas si no se activa

    def desconectar(self):
        self.conexion.commit() #Realiza cambio en la base de datos
        self.cursor.close()
        self.conexion.close() #Cierra la conexión

