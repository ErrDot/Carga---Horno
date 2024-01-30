from datetime import datetime
import json




### FUNCION PARA LEER ARCHIVO JSON
def configuracion():
    with open("constantes/config.json", "r") as archivo:
        parametros = json.load(archivo)
    return parametros



### OBTENER Y FORMATEAR HORA ACUTAL
def fecha_actual():    
    hora_actual = datetime.now()
    hora_actual = datetime.strftime(hora_actual, '%d/%m/%Y %H:%M:%S')
    return hora_actual