import pyodbc # CONECTOR PARA Sql Server
#import mysql.connector # CONECTOR DE MySql
import pandas as pd
from datetime import datetime 
from Funciones.secundarias import fecha_actual, configuracion
import time





# FUNCIÓN PARA VACIAR ARCHIVO
def eliminar_lineas(contador):
    ### OBTENER Y FORMATEAR HORA ACUTAL
    fecha_hora = fecha_actual()
    parametros = configuracion()
    try:
        with open(parametros["path"], 'r') as archivo:
            lineas = archivo.readlines()

        lineas = [lineas[0]] + lineas[contador :-1]

        with open(parametros["path"], 'w') as archivo:
            archivo.writelines(lineas)

        print(f"{fecha_hora}: Se han eliminado {contador} registros")
    except Exception as ex:
        print(f"{fecha_hora}: Error al eliminar líneas del archivo: {ex}")



# FUNCIÓN PARA CONECTAR CON BDD
def conectar_bdd():
    parametros = configuracion()
    # DATOS DE CONEXIÓN
    server = parametros["server"]
    db = parametros["bdd"]
    user = parametros["user"]
    password = parametros["password"]
    # CONECTAR A BASE DE DATOS
    global cnn
    cnn = pyodbc.connect(
        'DRIVER={SQL Server};SERVER='+server+';DATABASE='+db+';UID='+user+';PWD='+password
    )
    
    '''cnn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Hola1234',
        database='prueba'
    )'''
    


# FUNCIÓN PARA INGRESAR DATOS - FUNCION PRINCIPAL
def ingresar_datos(timer_runs, ruta_archivo):
    fecha_hora = fecha_actual()
    parametros = configuracion() 
    print(f"{fecha_hora}: Ingresando datos..." )
    while timer_runs.is_set():
        tiempo = parametros["tiempo"]
        fecha_hora = fecha_actual()
        # INGRESAR DATOS 
        df = pd.read_csv(ruta_archivo, sep=";", parse_dates=["dd-MM-yyyy H:mm:ss"], dayfirst=True).fillna('0')

        # Contador de registros ingresados
        contador = 0
        cursor_insert = cnn.cursor()
        for i, row in df.iterrows():   

            # Formateo de fecha
            hora = row['dd-MM-yyyy H:mm:ss']
            hora = datetime.strftime(hora, '%d/%m/%Y %H:%M:%S')

            # SENTENCIA SQL
            sql = f'''INSERT INTO controlPlc (fechaRegistro, valorTexto, valorDecimal, valorEntero, valorBinario)
                    VALUES ('{hora}', '{row['VARIEDAD HORNO']}', '{row['decimal']}', '{row['NUMERO DE BATCH HORNO']}', '{row['binario']}')'''

            cursor_insert.execute(sql)

            contador += 1

        cnn.commit()
        cursor_insert.close()

        print(f"{fecha_hora}: Se han ingresado: {contador} registros")

        if contador == 0:
            pass
        else:
            eliminar_lineas(contador)
        time.sleep(int(tiempo))  # 20 segundos
    


### FUNCIÓN PARA PARAR CERRAR CONEXION BDD
def cerrar_conexion():
    fecha_hora = fecha_actual()
    try:
        cnn.close()
        print(f"{fecha_hora}: La conexión se ha cerrado")
    except:
        print(f"{fecha_hora}: La conexión ya estaba cerrada o no estaba establecida")
        return
        


### RECUPERAR ÚLTIMO REGISTRO BDD
def ultimo_registro():
    cursor = cnn.cursor()
    sql = "SELECT MAX(fechaRegistro) FROM controlPlc"
    cursor.execute(sql)

    global registro_fecha
    registro_fecha = cursor.fetchone()

    cursor.close()
    print(registro_fecha)




    