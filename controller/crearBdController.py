from model.crearTablasBd import CreacionBbBillMate, existeBd

def  existeBase():
        
        estado = existeBd()

        if estado==1:
            pass
        if estado==0:
              objCreacionBD = CreacionBbBillMate()
