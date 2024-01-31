import tkinter as tk
import sys
from tkinter import *
from tkinter import scrolledtext
from Funciones.principales import conectar_bdd, ingresar_datos, fecha_actual, cerrar_conexion
from Funciones.secundarias import fecha_actual, configuracion, guardar_data
from constantes import style
from tkinter import messagebox
import threading





### PESTAÑA PARA PARAMETROS
class VentanaSecundaria(tk.Toplevel):
    en_uso = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Parametros")
        self.geometry("235x300")
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
            text="Minutos: "
        ).grid(row=6, column=1)
        self.entry_tiempo_lectura = tk.Entry(self)
        self.entry_tiempo_lectura.grid(row=6, column=2, padx=10, pady=10)



        self.btn_guardar = tk.Button(self, text="Guardar", command=self.guardar_datos).grid(
            row=7, column=1, padx=10, pady=10
        )


    ### FUNCION PARA GUARDAR PARAMETROS
    def guardar_datos(self):
        
        server = self.entry_server.get()
        base_datos = self.entry_bdd.get()
        user = self.entry_user.get()
        password = self.entry_password.get()
        direccion = self.entry_path.get()
        tiempo = self.entry_tiempo_lectura.get()


        parametros = {"server": server,"bdd": base_datos,"user":user,"password":password,"path":direccion,"tiempo":tiempo}
        guardar_data(parametros)

        
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

               


        


### PESTAÑA PRINCIPAL
class App(tk.Tk):


    ### INICIALIZACION DE APP  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Carga de datos - Horno")
        self.geometry("854x480")
        self.resizable(False, False)
        self.configure(background=style.BACKGROUND)
        self.init_widgets() 

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        


    ### WIDGETS - BTN, LABELS, ETC
    def init_widgets(self):
        ### FRAME HEAD
        Frame1 = tk.Frame(self)
        Frame1.configure(background=style.COMPONENT)
        Frame1.pack(
            side=tk.TOP,
            fill=tk.X,
            expand=False,
            padx=5,
            pady=5
        )

        self.btn_parametros = tk.Button(Frame1)
        self.btn_parametros.config(
            text="Parametros",
            state=tk.NORMAL,
            width=9,
            height=2,
            command=self.abrir_ventana,
            **style.BTN_STYLE,
            activebackground="white",
            activeforeground=style.TEXT
            )
        self.btn_parametros.pack(
            side=tk.RIGHT,
            fill=tk.X,
            padx=10,
            pady=11
        )

        self.btn_cerrar = tk.Button(Frame1)
        self.btn_cerrar.config(
            text="CERRAR",
            state=tk.NORMAL,
            width=9,
            height=2,
            command=self.on_close,
            **style.BTN_STYLE,
            activebackground="white",
            activeforeground=style.TEXT
            )
        self.btn_cerrar.pack(
            side=tk.RIGHT,
            fill=tk.X,
            padx=10,
            pady=11
        )

        '''Frame_central = tk.Frame(self)
        Frame_central.configure(background=style.FRAME_CENTRAL)
        Frame_central.pack(
            side=tk.TOP,
            fill=tk.BOTH,
            expand=True,
            padx=5,
            pady=5
        )'''

        ### CONSOLA EN PANTALLA

        self.console_output = scrolledtext.ScrolledText(
            self, wrap=tk.WORD, width=40, height=10)
        self.console_output.pack(expand=True, fill=tk.BOTH)
        sys.stdout = ConsoleRedirector(self.console_output)




        

        ### FRAME FOOTER
        Frame_footer = tk.Frame(self)
        Frame_footer.configure(background=style.COMPONENT)
        Frame_footer.pack(
            side=tk.BOTTOM,
            fill=tk.X,
            expand=False,
            padx=5,
            pady=5
        )

        ### BTN PARA INICIAR EL PROCECESO
        self.btn_iniciar = tk.Button(Frame1)
        self.btn_iniciar.config(
            text="INICIAR",
            state=tk.NORMAL,
            width=9,
            height=2,
            command=self.iniciar,
            **style.BTN_STYLE,
            #relief=tk.FLAT,
            activebackground="white",
            activeforeground=style.TEXT
            )
        self.btn_iniciar.pack(
            side=tk.LEFT,
            fill=tk.X,
            padx=50,
            pady=11
        )


        ### BTN PARA PARA EL PROCESO
        self.btn_detener = tk.Button(Frame1)
        self.btn_detener.config(
            text="DETENER",
            state=tk.NORMAL,
            width=9,
            height=2,
            command=self.stop,
            **style.BTN_STYLE,
            activebackground="white",
            activeforeground=style.TEXT
            )
        self.btn_detener.pack(
            side=tk.LEFT,
            fill=tk.X,
            padx=50,
            pady=11
        )



    def abrir_ventana(self):
        if not VentanaSecundaria.en_uso:
            self.ventana_secundaria = VentanaSecundaria()

    def write(self, text):
        self.console_output.insert(tk.END, text)
        self.console_output.see(tk.END)
        self.update_idletasks()

    ### FUNCION PARA INICIAR PROCESO, CONEXION E INGRESO DE DATOS
    def iniciar(self):
        param = configuracion()
        self.ruta_archivo = param["path"]
        fecha_hora = fecha_actual()
        if self.ruta_archivo != "":
            try:
                conectar_bdd()
                self.btn_iniciar.config(state=tk.DISABLED)
                print(f"{fecha_hora}: Conexión exitosa")
            except Exception as ex:
                print(f"{fecha_hora}: Ha producido el siguiente error: {ex}")
                messagebox.showerror(message="No se ha podido establecer conexión con el servidor", title='ERROR')
                return
            
            try:    
                global timer_runs        
                timer_runs = threading.Event()
                timer_runs.set()
                t = threading.Thread(target=ingresar_datos, args=(timer_runs, self.ruta_archivo,))
                t.start()
            except Exception as ex:
                messagebox.showerror(message="Error al ingresar datos.", title='ERROR')
                print(f"{fecha_hora}: Ha ocurrido el siguiente error: {ex}")
                return         
            
        else:
            print("La ruta del archivo no es correcta o no existe")
            messagebox.showwarning(message="No hay ningun archivo vinculado", title='WARNING')



    ### FUNCION PARA ENVIAR MENSAJES POR CONSOLA
    


    ### FUNCION PARA DETENER PROCESO
    def stop(self):
        fecha_hora = fecha_actual()
        try:
            timer_runs.clear()
            cerrar_conexion()
            self.btn_iniciar.config(state=tk.NORMAL)
        except Exception as ex:
            print(f"{fecha_hora}: El proceso aun no ha sido ejecutado...")
            return



    ### FUNCION DE CERRADA DE APP
    def on_close(self):
        try:
            timer_runs.clear()
            cerrar_conexion()
        except:
            print("")
        # RESTABLECE sys.stdout AL VALOR ORIGINAL AL SALIR DE LA APP
        #sys.stdout = sys.__stdout__
        # CERRA APP
        self.destroy()    



class ConsoleRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, text):
        self.text_widget.insert(tk.END, text + '\n')
        self.text_widget.see(tk.END)
    
    def flush(self):
        pass





##### EL PATIO DE LOS CALLADOS
    ### FUNCION PARA SUBIR ARCHIVO - RIP
    '''def subirArchivo(self):
        archivo = filedialog.askopenfilename(
            title="Subir archivo",
            filetypes=(
                ("Ficheros de datos", "*.dat"),
                ("Archivos de texto", "*.txt"),
                ("Todos los archivos", "*.*")
            )
        )
        if archivo:
            self.ruta_archivo = archivo
            self.title_label.config(text=f"Ruta del archivo: {self.ruta_archivo}")
            print(f"Path actualizado: {archivo}")'''       




        # btn RIP.
    '''tk.Button(
            optionsFrame,
            text="Subir Archivo",
            command= ...,
            **style.BTN_STYLE,
            relief=tk.FLAT,
            activebackground=style.BACKGROUND,
            activeforeground=style.TEXT
        ).pack(
            side=tk.LEFT,
            fill=tk.X,
            padx=12,
            pady=12
        )'''