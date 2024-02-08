import tkinter as tk
from tkinter import *
from Funciones.secundarias import fecha_actual, configuracion, guardar_data, resourcePath
from constantes import style
from tkinter import messagebox





### PESTAÑA PARA PARAMETROS
class VentanaSecundaria(tk.Toplevel):
    en_uso = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Parametros")
        self.geometry("235x300")
        self.icono = tk.PhotoImage(file=resourcePath("assets/4k.gif"))
        self.iconphoto(True, self.icono)
        self.configure(background=style.BACKGROUND)
        self.resizable(False, False)
        self.sec_widgets()
        self.mostrar_config()


        self.focus()
        self.__class__.en_uso = True

    def destroy(self):
        self.__class__.en_uso = False
        return super().destroy()
    
    def sec_widgets(self):
        
        self.label_server = tk.Label(
            self,
            text="Servidor: "
        ).grid(row=1, column=1)
        self.entry_server = tk.Entry(self)
        self.entry_server.grid(row=1, column=2, padx=10, pady=10)

        self.label_bdd = tk.Label(
            self,
            text="Bdd: "
        ).grid(row=2, column=1)
        self.entry_bdd = tk.Entry(self)
        self.entry_bdd.grid(row=2, column=2, padx=10, pady=10)

        self.label_user = tk.Label(
            self,
            text="Usuario: "
        ).grid(row=3, column=1)
        self.entry_user = tk.Entry(self)
        self.entry_user.grid(row=3, column=2, padx=10, pady=10)

        self.label_password = tk.Label(
            self,
            text="Contraseña: "
        ).grid(row=4, column=1)
        self.entry_password = tk.Entry(self,show="*")
        self.entry_password.grid(row=4, column=2, padx=10, pady=10)

        self.label_path = tk.Label(
            self,
            text="PATH: "
        ).grid(row=5, column=1)
        self.entry_path = tk.Entry(self)
        self.entry_path.grid(row=5, column=2, padx=10, pady=10)

        self.label_tiempo_lectura = tk.Label(
            self,
            text="Segundos: "
        ).grid(row=6, column=1)
        self.entry_tiempo_lectura = tk.Entry(self)
        self.entry_tiempo_lectura.grid(row=6, column=2, padx=10, pady=10)



        self.btn_guardar = tk.Button(self, text="Guardar", command=self.guardar_datos).grid(
            row=7, column=1, padx=10, pady=10
        )


    ### FUNCION PARA GUARDAR PARAMETROS
    def guardar_datos(self):
        fecha_hora = fecha_actual()
        try:
            server = self.entry_server.get()
            base_datos = self.entry_bdd.get()
            user = self.entry_user.get()
            password = self.entry_password.get()
            direccion = self.entry_path.get()
            tiempo = self.entry_tiempo_lectura.get()


            parametros = {"server": server,"bdd": base_datos,"user":user,"password":password,"path":direccion,"tiempo":tiempo}
            guardar_data(parametros)
            messagebox.showinfo(message="Datos guardados", title="Guardado Exitoso")
        except Exception as ex:
            print(f"{fecha_hora}Ha ocurrido el siguiente error: {ex}")
            messagebox.showerror(message="Ha ocurrido un error al intentar guardo los datos", title='ERROR')
            return
        self.destroy()


    ### FUNCIÓN PARA MOSTRAR CONFIGURACIÓN
    def mostrar_config(self):
        v_parametros = configuracion()
        server = v_parametros["server"]
        db = v_parametros["bdd"]
        user = v_parametros["user"]
        password = v_parametros["password"]
        direccion = v_parametros["path"]
        tiempo = v_parametros["tiempo"]

        self.entry_server.insert(0, server)
        self.entry_bdd.insert(0, db)
        self.entry_user.insert(0, user)
        self.entry_password.insert(0, password)
        self.entry_path.insert(0, direccion)
        self.entry_tiempo_lectura.insert(0, tiempo)