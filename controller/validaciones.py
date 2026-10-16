#Validaciones compartidas por los controladores

def esNumero(texto):
    #Devuelve True si el texto se puede convertir a número (vacío, espacios o letras no)
    try:
        float(texto)
        return True
    except (TypeError, ValueError):
        return False
