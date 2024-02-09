import tkinter as tk
import sys
from tkinter import *
from tkinter import scrolledtext
from Funciones.principales import conectar_bdd, main, fecha_actual, cerrar_conexion
from Funciones.secundarias import fecha_actual, configuracion, resourcePath
from constantes import style
from tkinter import messagebox
import threading
from src.Vparametros import VentanaSecundaria







### PESTAÑA PRINCIPAL
class App(tk.Tk):


    ### INICIALIZACION DE APP  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Carga de datos - Horno Talagante")
        self.icono = tk.PhotoImage(file=resourcePath("assets/4k.gif"))
        self.iconphoto(True, self.icono)
        self.geometry("854x480")
        self.resizable(False, False)
        self.configure(background=style.BACKGROUND)
        self.init_widgets() 
        self.iniciar()
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

        # BTN PARA INGRESAR PARAMETROS
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

        #BTN PARA CERRAR APP
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

        ### CONSOLA EN PANTALLA
        self.console_output = scrolledtext.ScrolledText(
            self, wrap=tk.WORD, width=40, height=10)
        self.console_output.pack(
            expand=True, 
            fill=tk.BOTH, 
            padx=5,
            pady=5)
        sys.stdout = ConsoleRedirector(self.console_output)

        ### BTN PARA INICIAR EL PROCECESO
        self.btn_iniciar = tk.Button(Frame1)
        self.btn_iniciar.config(
            text="INICIAR",
            state=tk.NORMAL,
            width=9,
            height=2,
            command=self.iniciar,
            **style.BTN_STYLE,
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


    ### FUNCIÓN PARA ABRIR SEGUNDA VENTANA
    def abrir_ventana(self):
        if not VentanaSecundaria.en_uso:
            self.ventana_secundaria = VentanaSecundaria()



    ### FUNCIÓN PARA ESCRIBIR EN PANTALLA
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
                self.btn_iniciar.config(state=tk.DISABLED)
                self.btn_cerrar.config(state=tk.DISABLED)    
                global timer_runs        
                timer_runs = threading.Event()
                timer_runs.set()
                t = threading.Thread(target=main, args=(timer_runs, self.ruta_archivo,))
                t.start()
            except Exception as ex:
                messagebox.showerror(message="Error al ingresar datos.", title='ERROR')
                print(f"{fecha_hora}: Ha ocurrido el siguiente error: {ex}")
                return         
            
        else:
            messagebox.showwarning(message="No hay ningun archivo vinculado", title='WARNING')
    


    ### FUNCION PARA DETENER PROCESO
    def stop(self):
        fecha_hora = fecha_actual()
        try:
            timer_runs.clear()
            cerrar_conexion()
            self.btn_iniciar.config(state=tk.NORMAL)
            self.btn_cerrar.config(state=tk.NORMAL)
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
        # CERRA APP
        self.destroy()    


### CLASE PARA REDIRIGIR MENSAJES DE CONSOLA
class ConsoleRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, text):
        self.text_widget.insert(tk.END, text + '\n')
        self.text_widget.see(tk.END)
    
    def flush(self):
        pass

