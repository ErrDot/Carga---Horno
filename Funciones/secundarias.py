from datetime import datetime
import json
import sys
import os


### FUNCIÓN PARA RUTA DE PYINSTALLER
def resourcePath(relativePath):
    try:
        basePath = sys._MEIPASS
    except Exception:
        basePath = os.path.abspath(".")

    return os.path.join(basePath, relativePath)



### FUNCIÓN PARA GUARADAR PARAMETROS
def guardar_data(param):
    with open(resourcePath("config.json"), "w") as archivo:
        json.dump(param, archivo, indent=4)
            


### FUNCION PARA LEER ARCHIVO JSON
def configuracion():
    with open(resourcePath("config.json"), "r") as archivo:
        parametros = json.load(archivo)
    return parametros



### OBTENER Y FORMATEAR HORA ACUTAL
def fecha_actual():    
    hora_actual = datetime.now()
    hora_actual = datetime.strftime(hora_actual, '%d/%m/%Y %H:%M:%S')
    return hora_actual