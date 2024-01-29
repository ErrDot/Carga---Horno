import tkinter as tk
from tkinter import *
from tkinter import scrolledtext
import sys
from constantes.funciones import conectar_bdd, cerrar_conexion, ingresar_datos
from constantes import style, config
from tkinter import messagebox
import threading 
from datetime import datetime




class App(tk.Tk):


    ### INICIALIZACION DE APP  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Carga de datos - Horno")
        self.geometry("854x480")
        self.resizable(False, False)
        self.configure(background=style.BACKGROUND)
        self.init_widgets() 

        self.ruta_archivo = config.PATH
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.hora_actual = datetime.now()
        self.hora_actual = datetime.strftime(self.hora_actual, '%d/%m/%Y %H:%M:%S')


    ### WIDGETS - BTN, LABELS, ETC
    def init_widgets(self):
        ### FRAME HEAD
        Frame1 = tk.Frame(self)
        Frame1.configure(background=style.COMPONENT)
        Frame1.pack(
            side=tk.TOP,
            fill=tk.X,
            padx=5,
            pady=5
        )

        ### TEXTO RUTA DE ARCHIVO
        self.title_label = tk.Label(
        Frame1,
        text=config.PATH,
        justify=tk.CENTER,
        **style.STYLE
        )
        self.title_label.pack(
            side=tk.TOP,
            fill=tk.BOTH,
            expand=True,
            padx=5,
            pady=5
        )

        ### CONSOLA EN PANTALLA
        self.console_text = scrolledtext.ScrolledText(
            self, wrap=tk.WORD, width=40, height=20)
        self.console_text.pack(
            expand=True, 
            fill=tk.BOTH, 
            padx=5, 
            pady=5
            )
        sys.stdout = self

        ### FRAME FOOTER
        Frame_footer = tk.Frame(self)
        Frame_footer.configure(background=style.COMPONENT)
        Frame_footer.pack(
            side=tk.BOTTOM,
            fill=tk.X,
            padx=5,
            pady=5
        )

        ### BTN PARA INICIAR EL PROCECESO
        self.btn_iniciar = tk.Button(Frame_footer)
        self.btn_iniciar.config(
            text="INICIAR",
            state=tk.NORMAL,
            width=15,
            height=25,
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
        self.btn_detener = tk.Button(Frame_footer)
        self.btn_detener.config(
            text="DETENER",
            state=tk.NORMAL,
            width=15,
            height=25,
            command=self.stop,
            **style.BTN_STYLE,
            activebackground="white",
            activeforeground=style.TEXT
            )
        self.btn_detener.pack(
            side=tk.RIGHT,
            fill=tk.X,
            padx=50,
            pady=11
        )



    ### FUNCION PARA INICIAR PROCESO, CONEXION E INGRESO DE DATOS
    def iniciar(self):
        if self.ruta_archivo:

            try:
                conectar_bdd()
                self.btn_iniciar.config(state=tk.DISABLED)
                self.write(f"{self.hora_actual}: Conexión exitosa")
            except Exception as ex:
                self.write(f"{self.hora_actual}: Ha producido el siguiente error: {ex}")
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
                self.write(f"{self.hora_actual}: Ha ocurrido el siguiente error: {ex}")
                return         
            
        elif self.ruta_archivo == 1:
            self.write("La ruta del archivo no es correcta o no existe")
        else:
            messagebox.showwarning(message="No hay ningun archivo vinculado", title='WARNING')



    ### FUNCION PARA ENVIAR MENSAJES POR CONSOLA
    def write(self, text):
        self.console_text.insert(tk.END, text + '\n')
        self.console_text.yview(tk.END)


    ### FUNCION PARA DETENER PROCESO
    def stop(self):
        try:
            timer_runs.clear()
            cerrar_conexion()
            self.btn_iniciar.config(state=tk.NORMAL)
        except Exception as ex:
            self.write(f"{self.hora_actual}: El proceso aun no ha sido ejecutado...")
            return



    ### FUNCION DE CERRADA DE APP
    def on_close(self):
        try:
            timer_runs.clear()
            cerrar_conexion()
        except:
            print("")
        # RESTABLECE sys.stdout AL VALOR ORIGINAL AL SALIR DE LA APP
        sys.stdout = sys.__stdout__
        # CERRA APP
        self.destroy()    
        





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