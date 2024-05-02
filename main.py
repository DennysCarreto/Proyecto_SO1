import tkinter as tk
from tkinter import ttk
import datetime, time
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading
import time
import random

N = 1024
memoria_principal = [None] * N
procesos_en_memoria = {}
contador_proceso = 0
semaphore = threading.Semaphore()

# asigna espacio en memoria a un proceso
def asignar_espacio_en_memoria(tiempo_consumo):
    global contador_proceso
    for i in range(N):
        if all([memoria_principal[j] is None for j in range(i, min(i + tiempo_consumo, N))]):
            contador_proceso += 1
            for j in range(i, i + tiempo_consumo):
                memoria_principal[j] = contador_proceso
            procesos_en_memoria[contador_proceso] = (hex(i), tiempo_consumo)
            return True
    return False

#libera espacio en memoria al finalizar un proceso
def liberar_espacio_en_memoria(id_proceso):
    inicio, fin = procesos_en_memoria[id_proceso]
    inicio = int(inicio, 16)  # Convertir inicio a entero
    fin = inicio + fin - 1  # Calcular el valor final (fin) como inicio + duración - 1
    for i in range(inicio, fin + 1):
        memoria_principal[i] = None
    del procesos_en_memoria[id_proceso]



def ejecutar_proceso(proceso_id, inicio, fin):
    inicio = int(inicio, 16)  # Convertir inicio a entero
    fin = inicio + fin - 1  # Calcular el valor final (fin) como inicio + duración - 1
    for tiempo_restante in range(fin - inicio + 1):
        direccion_actual = inicio + tiempo_restante
        time.sleep(1)
        if tiempo_restante == fin - inicio:
            liberar_espacio_en_memoria(proceso_id)
            actualizar_tabla_procesos()
            agregar_a_historial(proceso_id, "Finalizado", inicio, fin)
        else:
            semaphore.release()

def actualizar_tabla_procesos():
    process_table.delete(*process_table.get_children())
    for id_proceso, (inicio, fin) in procesos_en_memoria.items():
        process_table.insert('', 'end', text=str(id_proceso), values=(f'{int(inicio, 16)} s', f'{fin} s'))

def agregar_proceso():
    tiempo_consumo = random.randint(1, 20)  # Tamaño aleatorio del proceso
    if not asignar_espacio_en_memoria(tiempo_consumo):
        messagebox.showinfo("Pila llena", "No se puede agregar más procesos, la pila está llena")
    else:
        proceso_id = contador_proceso
        tiempo_llegada = time.strftime('%H:%M:%S')
        #proceso_info = f"ID: {proceso_id}, Tiempo de llegada: {time.strftime('%H:%M:%S')}, Tiempo de consumo: {tiempo_consumo} s\n"
        process_table.insert('', 'end', text=str(proceso_id), values=(tiempo_llegada, tiempo_consumo))
        #new_processes_text.insert(tk.END, proceso_info)
        actualizar_tabla_procesos()

def generar_procesos_aleatorios():
    tiempo_consumo = random.randint(1, 20)  # Tamaño aleatorio del proceso
    if not asignar_espacio_en_memoria(tiempo_consumo):
        messagebox.showinfo("Pila llena", "No se puede agregar más procesos, la pila está llena")
    else:
        proceso_id = contador_proceso
        tiempo_llegada = time.strftime('%H:%M:%S')
        proceso_info = f"ID: {proceso_id}, Tiempo de llegada: {time.strftime('%H:%M:%S')}, Tiempo de consumo: {tiempo_consumo} s\n"
        process_table.insert('', 'end', text=str(proceso_id), values=(tiempo_llegada, tiempo_consumo))
        #process_table.insert(tk.END,proceso_info)
        #new_processes_text.insert(tk.END, proceso_info)
        actualizar_tabla_procesos()

def ejecutar_procesos_round_robin():
    tiempo_quantum = 5
    procesos_en_espera = list(procesos_en_memoria.keys())

    while procesos_en_espera:
        proceso_actual = procesos_en_espera.pop(0)
        inicio, fin = procesos_en_memoria[proceso_actual]
        semaphore.acquire()  # Esperar a que se libere el semáforo
        hilo_proceso = threading.Thread(target=ejecutar_proceso, args=(proceso_actual, inicio, fin))
        hilo_proceso.start()

def agregar_a_historial(id_proceso, estado, hora_inicio, hora_fin=None):
    if estado == "Finalizado":
    #historial_info = f"ID: {id_proceso}, Estado: {estado}, Inicio: {inicio} s, Fin: {fin} s\n"
        historial.insert('', 'end', text=id_proceso, values=(estado, hora_inicio, hora_fin ))
        #historial.insert('', 'end', text=id_proceso, values=(estado, inicio, fin))
        #historial_text.insert(tk.END, historial_info)
    else:
        historial.insert('', 'end', text=id_proceso, values=(estado, hora_inicio, hora_fin))

def iniciar_simulacion():
   # generar_procesos_aleatorios()
    ejecutar_procesos_round_robin()


def update_time():
    while True:
        hora_actual = datetime.datetime.now().strftime("Hora del sistema\n%H:%M:%S hrs")
        hora.set(hora_actual)
        time.sleep(1)


def update_contador():
    while True:
        contador.set(contador.get() + 1)
        time.sleep(1)


# Crear la ventana principal
root = tk.Tk()
root.title("URL 2024")

# Crear los estilos para los widgets
style = ttk.Style()
style.theme_use("clam")

# Crear el frame principal
main_frame = tk.Frame(root)
main_frame.grid(row=0, column=0, padx=10, pady=10)

# Crear un frame para la tabla de procesos y el label
process_frame = tk.Frame(main_frame)
process_frame.grid(row=0, column=0, padx=5, pady=5)

# Crear la tabla de procesos
process_table = ttk.Treeview(process_frame)
process_table['columns'] = ('TL', 'TC')
process_table.column('#0', width=50, minwidth=50, anchor='center')
process_table.column('TL', width=90, minwidth=50, anchor='center')
process_table.column('TC', width=50, minwidth=50, anchor='center')
process_table.heading('#0', text='P', anchor='center')
process_table.heading('TL', text='TL', anchor='center')
process_table.heading('TC', text='TC', anchor='center')

'''
# Insertar datos de ejemplo en la tabla de procesos
process_table.insert('', 'end', text='A', values=('1', '3'))
process_table.insert('', 'end', text='B', values=('4', '5'))
process_table.insert('', 'end', text='C', values=('1', '2'))
process_table.insert('', 'end', text='D', values=('5', '3'))
'''

process_table.grid(row=1, column=0, padx=5, pady=5)

# Crear el label sobre la tabla de procesos
process_label = tk.Label(process_frame, text="Tabla de Procesos", font=("Arial", 14, "bold"))
process_label.grid(row=0, column=0, padx=5, pady=5)

# Crear la memoria principal
memory_frame = tk.Frame(main_frame, relief='sunken', borderwidth=2)
memory_frame.grid(row=0, column=1, padx=5, pady=5)

# Agregar los rectángulos de colores para representar la memoria principal
system_os = tk.Label(memory_frame, text="S.O.\n" * 1, background="cyan", wraplength=50, width=15)
system_os.pack(side='bottom', fill='x')
process_a = tk.Label(memory_frame, text="A\n" * 2, background="green", wraplength=50)
process_a.pack(side='bottom', fill='x')
process_b = tk.Label(memory_frame, text="B\n" * 2, background="red", wraplength=50)
process_b.pack(side='bottom', fill='x')
process_c = tk.Label(memory_frame, text="C\n" * 2, background="red", wraplength=50)
process_c.pack(side='bottom', fill='x')

# Crear el CPU
cpu_frame = tk.LabelFrame(main_frame, text="CPU", relief='raised', borderwidth=2)
cpu_frame.grid(row=0, column=2, padx=5, pady=5)

# Agregar los elementos del CPU
planificador = tk.Label(cpu_frame, text="Planificador")
planificador.pack(pady=5)

planificador_value = tk.Label(cpu_frame, text="A", font=("Arial", 12, "bold"))
planificador_value.pack(pady=5)

contador_programa = tk.Label(cpu_frame, text="Contador de programa")
contador_programa.pack(pady=5)

contador_programa_value = tk.Label(cpu_frame, text="d", font=("Arial", 12, "bold"))
contador_programa_value.pack(pady=5)

base_limite = tk.Label(cpu_frame, text="Base Limite")
base_limite.pack(pady=5)

base_limite_values = tk.Label(cpu_frame, text="b h", font=("Arial", 12, "bold"))
base_limite_values.pack(pady=5)

historial = ttk.Treeview(cpu_frame, height=3)
historial['columns'] = ('Estado', 'Hora inicio', 'Hora fin')
historial.column('#0', width=50, minwidth=50, anchor='center')
historial.column('Estado', width=100, minwidth=100, anchor='center')
historial.column('Hora inicio', width=100, minwidth=100, anchor='center')
historial.column('Hora fin', width=100, minwidth=100, anchor='center')
historial.heading('#0', text='ID', anchor='center')
historial.heading('Estado', text='Estado', anchor='center')
historial.heading('Hora inicio', text='Hora inicio', anchor='center')
historial.heading('Hora fin', text='Hora fin', anchor='center')

'''
historial.insert('', 'end', text='a', values=('new', '13:00:00', '13:00:04'))
historial.insert('', 'end', text='b', values=('lists', '13:00:04', '13:00:08'))
historial.insert('', 'end', text='c', values=('lists', '13:00:08', ''))
'''

historial.pack(pady=5)

# Crear un frame para la hora del sistema
time_frame = tk.Frame(main_frame)
time_frame.grid(row=1, column=2, columnspan=4, padx=5, pady=5, sticky='s')

# Agregar la hora del sistema
hora = tk.StringVar(value='')   # hora
hora_sistema = tk.Label(time_frame, textvariable=hora, font=("Arial", 12))
hora_sistema.pack(pady=5)

# Contador
contador = tk.IntVar(value=0)   # contador = 0
lblcontador = tk.Label(time_frame, textvariable=contador, font=("Arial", 12))
lblcontador.pack(pady=5)

# Crear el botón "Iniciar"
iniciar_button = tk.Button(main_frame, text="Iniciar", command=iniciar_simulacion)
iniciar_button.grid(row=2, column=0, columnspan=4, pady=10)

agregar_button = tk.Button(main_frame, text="Agregar Proceso", command=agregar_proceso)
agregar_button.grid(row=1, columnspan=4, pady=10)

# Hilos para actualización de la hora y contador
hilo_contador = threading.Thread(target=update_contador)
hilo_contador.start()
hilo_time = threading.Thread(target=update_time)
hilo_time.start()


root.mainloop()
