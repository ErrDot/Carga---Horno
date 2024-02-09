import pyodbc # CONECTOR PARA Sql Server
import pandas as pd
from datetime import datetime 
from Funciones.secundarias import fecha_actual, configuracion
import time
from tkinter import messagebox





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
    vi_contador = 0
    v_conectado = "n"
    while vi_contador < 3:
        try:
            global cnn
            cnn = pyodbc.connect(
                'DRIVER={SQL Server};SERVER='+server+';DATABASE='+db+';UID='+user+';PWD='+password
            )
            vi_contador = 10
            v_conectado = "s"
        except:
            vi_contador += 1
            v_conectado = "n"
    return v_conectado






# FUNCIÓN PRINCIPAL
def main(timer_runs, ruta_archivo):
    parametros = configuracion()
    fecha_hora = fecha_actual()
    print(f"{fecha_hora}: Ingresando datos..." )
    # INGRESAR DATOS
    while timer_runs.is_set():
        tiempo = parametros["tiempo"]
        v_conectado = conectar_bdd()
        if v_conectado == "s":
            ingresar_datos(ruta_archivo)

        time.sleep(int(tiempo))  # Segundos


#FUNCIÓN PARA INGRESAR DATOS
def ingresar_datos(ruta_archivo):
    fecha_hora = fecha_actual()

    try: 
        df = pd.read_csv(ruta_archivo, sep=";", parse_dates=["dd-MM-yyyy H:mm:ss"], dayfirst=True, encoding='unicode_escape').fillna('0')
    except Exception as ex:
        messagebox.showerror(message="Archivo erroneo o no vinculado, intente otra vez", title='ERROR')
        return
    
    try:
        # VALORES DECIMALES
        df['T° Sobre Grano'] = df['T° Sobre Grano'].str.replace(',', '.').astype(float)
        df['T° Sobre Tela'] = df['T° Sobre Tela'].str.replace(',', '.').astype(float)
        df['T° Bajo Tela 2'] = df['T° Bajo Tela 2'].str.replace(',', '.').astype(float)
        df['T° AMBIENTE'] = df['T° AMBIENTE'].str.replace(',', '.').astype(float)
        df['%HR Sobre tela'] = df['%HR Sobre tela'].str.replace(',', '.').astype(float)
        # VALORES INT
        df['Presion diferencial'] = df['Presion diferencial'].str.replace(',', '.').astype(float) / 1
        df['GAS ETAPA 1'] = df['GAS ETAPA 1'].str.replace(',', '.').astype(float) / 1
        df['GAS ETAPA 2'] = df['GAS ETAPA 2'].str.replace(',', '.').astype(float) / 1
        df['GAS ETAPA 3'] = df['GAS ETAPA 3'].str.replace(',', '.').astype(float) / 1
        df['GAS ETAPA 4'] = df['GAS ETAPA 4'].str.replace(',', '.').astype(float) / 1
        df['GAS ETAPA 5'] = df['GAS ETAPA 5'].str.replace(',', '.').astype(float) / 1
        df['GAS ETAPA 6'] = df['GAS ETAPA 6'].str.replace(',', '.').astype(float) / 1
        df['TIEMPO BARRA ETAPA 1'] = df['TIEMPO BARRA ETAPA 1'].str.replace(',', '.').astype(float) / 1
        df['TIEMPO BARRA ETAPA 2'] = df['TIEMPO BARRA ETAPA 2'].str.replace(',', '.').astype(float) / 1
        df['TIEMPO BARRA ETAPA 3'] = df['TIEMPO BARRA ETAPA 3'].str.replace(',', '.').astype(float) / 1
        df['TIEMPO BARRA ETAPA 4'] = df['TIEMPO BARRA ETAPA 4'].str.replace(',', '.').astype(float) / 1
        df['TIEMPO BARRA ETAPA 5'] = df['TIEMPO BARRA ETAPA 5'].str.replace(',', '.').astype(float) / 1
        df['TIEMPO BARRA ETAPA 6'] = df['TIEMPO BARRA ETAPA 6'].str.replace(',', '.').astype(float) / 1
        df['SET POINT DE TEMPERATURA ETAPA 1'] = df['SET POINT DE TEMPERATURA ETAPA 1'].str.replace(',', '.').astype(float) / 1
        df['SET POINT DE TEMPERATURA ETAPA 2'] = df['SET POINT DE TEMPERATURA ETAPA 2'].str.replace(',', '.').astype(float) / 1
        df['SET POINT DE TEMPERATURA ETAPA 3'] = df['SET POINT DE TEMPERATURA ETAPA 3'].str.replace(',', '.').astype(float) / 1
        df['SET POINT ETAPA 4'] = df['SET POINT ETAPA 4'].str.replace(',', '.').astype(float) / 1
        df['SET POINT DE TEMPERATURA ETAPA 5'] = df['SET POINT DE TEMPERATURA ETAPA 5'].str.replace(',', '.').astype(float) / 1
        df['SET POINT DE TEMPERATURA ETAPA 6'] = df['SET POINT DE TEMPERATURA ETAPA 6'].str.replace(',', '.').astype(float) / 1
        #PASAR LOS VALORES A INT
        df['Presion diferencial'] = df['Presion diferencial'].astype(int)
        df['GAS ETAPA 1'] = df['GAS ETAPA 1'].astype(int)
        df['GAS ETAPA 2'] = df['GAS ETAPA 2'].astype(int)
        df['GAS ETAPA 3'] = df['GAS ETAPA 3'].astype(int)
        df['GAS ETAPA 4'] = df['GAS ETAPA 4'].astype(int)
        df['GAS ETAPA 5'] = df['GAS ETAPA 5'].astype(int)
        df['GAS ETAPA 6'] = df['GAS ETAPA 6'].astype(int)
        df['TIEMPO BARRA ETAPA 1'] = df['TIEMPO BARRA ETAPA 1'].astype(int)
        df['TIEMPO BARRA ETAPA 2'] = df['TIEMPO BARRA ETAPA 2'].astype(int)
        df['TIEMPO BARRA ETAPA 3'] = df['TIEMPO BARRA ETAPA 3'].astype(int)
        df['TIEMPO BARRA ETAPA 4'] = df['TIEMPO BARRA ETAPA 4'].astype(int)
        df['TIEMPO BARRA ETAPA 5'] = df['TIEMPO BARRA ETAPA 5'].astype(int)
        df['TIEMPO BARRA ETAPA 6'] = df['TIEMPO BARRA ETAPA 6'].astype(int)
        df['SET POINT DE TEMPERATURA ETAPA 1'] = df['SET POINT DE TEMPERATURA ETAPA 1'].astype(int)
        df['SET POINT DE TEMPERATURA ETAPA 2'] = df['SET POINT DE TEMPERATURA ETAPA 2'].astype(int)
        df['SET POINT DE TEMPERATURA ETAPA 3'] = df['SET POINT DE TEMPERATURA ETAPA 3'].astype(int)
        df['SET POINT ETAPA 4'] = df['SET POINT ETAPA 4'].astype(int)
        df['SET POINT DE TEMPERATURA ETAPA 5'] = df['SET POINT DE TEMPERATURA ETAPA 5'].astype(int)
        df['SET POINT DE TEMPERATURA ETAPA 6'] = df['SET POINT DE TEMPERATURA ETAPA 6'].astype(int)
    except Exception as ex:
        print(f"{fecha_hora}: Ha ocurrido el siguiente error: {ex}")
        return 
    

    try:    
        # CURSOR PARA INGRESAR DATOS
        cursor_insert = cnn.cursor()
        ultimo = ultimo_registro()
    except:
        fecha_act = fecha_actual()
        print(f"{fecha_act}: Ups, algo salió mal")
        return


    # Contador de registros ingresados
    contador = 0
    try:
        ultimoRegistro = ultimo[0]
        if ultimoRegistro == None:
            ultimoRegistro = datetime.strptime("17/01/2018 10:05:00", '%d/%m/%Y %H:%M:%S')
        else:
            ultimoRegistro = datetime.strftime(ultimoRegistro, '%d/%m/%Y %H:%M:%S')
            ultimoRegistro = datetime.strptime(ultimoRegistro, '%d/%m/%Y %H:%M:%S')
    except Exception as ex:
        print(f"{fecha_hora}: Ups, algo salió mal...")
        return     


    try:
        # For PARA INTERAR .DAT
        for i, row in df.iterrows():   
            # Formateo de fecha
            campo_fecha = row['dd-MM-yyyy H:mm:ss']
            v_fecha = datetime.strftime(campo_fecha, '%d/%m/%Y %H:%M:%S')
            fecha = datetime.strptime(v_fecha, '%d/%m/%Y %H:%M:%S')
            
            
            if fecha != ultimoRegistro and fecha > ultimoRegistro:
                try:
                    # SENTENCIA SQL
                    sql = f'''INSERT INTO HornoMiagTTE (Fecha, Batch, Variedad, TSobreGrano, TSobreTela,TBajoTela2,
                                TAmbiente, HRSobreTela, PAperturaDamper, PresionDiferencial, GasTotal, GasEtapa1,
                                GasEtapa2, GasEtapa3, GasEtapa4, GasEtapa5, GasEtapa6, TiempoTotal, TiempoBarraE1,
                                TiempoBarraE2, TiempoBarraE3, TiempoBarraE4, TiempoBarraE5, TiempoBarraE6, SPTemp1,
                                SPTemp2, SPTemp3, SPTemp4, SPTemp5, SPTemp6, BotonStart)
                                VALUES ('{v_fecha}', '{row['Numero de Batch']}', '{row['Variedad']}', '{row['T° Sobre Grano']}', 
                                    '{row['T° Sobre Tela']}','{row['T° Bajo Tela 2']}', '{row['T° AMBIENTE']}', '{row['%HR Sobre tela']}', 
                                    '{row['Porcentaje de apertura de DAMPER']}', '{row['Presion diferencial']}', '{row['GAS TOTAL']}', 
                                    '{row['GAS ETAPA 1']}', '{row['GAS ETAPA 2']}','{row['GAS ETAPA 3']}','{row['GAS ETAPA 4']}', 
                                    '{row['GAS ETAPA 5']}', '{row['GAS ETAPA 6']}', '{row['TIEMPO TOTAL']}', '{row['TIEMPO BARRA ETAPA 1']}',
                                    '{row['TIEMPO BARRA ETAPA 2']}', '{row['TIEMPO BARRA ETAPA 3']}', '{row['TIEMPO BARRA ETAPA 4']}', 
                                    '{row['TIEMPO BARRA ETAPA 5']}','{row['TIEMPO BARRA ETAPA 6']}', '{row['SET POINT DE TEMPERATURA ETAPA 1']}', 
                                    '{row['SET POINT DE TEMPERATURA ETAPA 2']}','{row['SET POINT DE TEMPERATURA ETAPA 3']}', '{row['SET POINT ETAPA 4']}', 
                                    '{row['SET POINT DE TEMPERATURA ETAPA 5']}', '{row['SET POINT DE TEMPERATURA ETAPA 6']}', '{row['Boton Start']}')'''
                    cursor_insert.execute(sql)
                    contador += 1
                except:
                    print(f"{fecha_hora}: Error en fila \n {v_fecha} - {row['Numero de Batch']}")
        # Confirmación del ingreso
        cnn.commit()
        cursor_insert.close()
        cnn.close()
    except TypeError:
        messagebox.showerror(message="Error en archivo, Favor informar a Depto. TI", title='ERROR')
        return
    except:
        return

    print(f"{fecha_hora}: Se han ingresado: {contador} registros")


### FUNCIÓN PARA PARAR CERRAR CONEXION BDD
def cerrar_conexion():
    fecha_hora = fecha_actual()
    try:
        cnn.close()
        print(f"{fecha_hora}: La conexión se ha cerrado")
    except:
        print(f"{fecha_hora}: Conexión cerrada...")
        
        


### RECUPERAR ÚLTIMO REGISTRO BDD
def ultimo_registro():
    cursor = cnn.cursor()
    sql = "SELECT MAX(Fecha) FROM HornoMiagTTE"
    cursor.execute(sql)

    global registro_fecha
    registro_fecha = cursor.fetchone()

    cursor.close()
    ultima_fecha = []
    for i in registro_fecha:
        ultima_fecha.append(i)
    return ultima_fecha
    

