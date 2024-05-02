import tkinter as tk
from tkinter import ttk
import datetime
import threading
import time

# Variables globales para la simulación
N = 1024  # Tamaño de la memoria principal en bytes
memoria_principal = [None] * N  # Lista que representa la memoria principal
sistema_operativo_size = 256  # Tamaño reservado para el sistema operativo

# Función para cargar un proceso en la memoria principal
def cargar_proceso(nombre_proceso, tiempo_consumo):
    global memoria_principal, sistema_operativo_size, N
    
    # Buscar un espacio adecuado en la memoria principal
    for i in range(sistema_operativo_size, N - tiempo_consumo + 1):
        if memoria_principal[i] is None:
            # Espacio encontrado para cargar el proceso
            memoria_principal[i:i+tiempo_consumo] = [nombre_proceso] * tiempo_consumo
            return True
    
    # No hay suficiente espacio en la memoria principal
    return False

# Función para liberar un proceso de la memoria principal al finalizar su ejecución
def liberar_proceso(nombre_proceso):
    global memoria_principal, sistema_operativo_size, N
    
    for i in range(sistema_operativo_size, N):
        if memoria_principal[i] == nombre_proceso:
            memoria_principal[i] = None

# Función para simular la planificación de procesos (Round-robin)
def simulacion_round_robin(lista_procesos):
    global memoria_principal
    
    tiempo_quantum = 1  # Quantum de tiempo para el algoritmo Round-robin
    tiempo_actual = 0
    
    for proceso in lista_procesos:
        nombre_proceso = proceso['nombre']
        tiempo_consumo = proceso['tiempo_consumo']
        
        if cargar_proceso(nombre_proceso, tiempo_consumo):
            # Proceso cargado en la memoria, simular su ejecución
            contador_programa_value.config(text=str(tiempo_actual))
            planificador_value.config(text=nombre_proceso)
            base_limite_values.config(text=f"Base: {sistema_operativo_size}, Límite: {sistema_operativo_size + tiempo_consumo}")
            
            while tiempo_consumo > 0:
                # Ejecutar proceso por un quantum de tiempo
                time.sleep(tiempo_quantum)  # Simula el tiempo de ejecución
                tiempo_consumo -= tiempo_quantum
                
                # Actualizar la interfaz gráfica para mostrar el estado de la CPU
                contador_programa_value.config(text=str(tiempo_actual))
                
                tiempo_actual += tiempo_quantum
            
            # Liberar el proceso al finalizar su ejecución
            liberar_proceso(nombre_proceso)
            contador_programa_value.config(text=str(tiempo_actual))
            planificador_value.config(text="Libre")
            base_limite_values.config(text="Base: 0, Límite: 0")

# Obtener los datos de la tabla de procesos y crear el diccionario lista_procesos
def obtener_lista_procesos():
    lista_procesos = []
    
    for item in process_table.get_children():
        nombre_proceso = process_table.item(item, "text")
        tiempo_llegada = int(process_table.item(item, "values")[0])
        tiempo_consumo = int(process_table.item(item, "values")[1])
        
        proceso = {'nombre': nombre_proceso, 'tiempo_llegada': tiempo_llegada, 'tiempo_consumo': tiempo_consumo}
        lista_procesos.append(proceso)
    
    return lista_procesos

# Obtener la lista de procesos al iniciar la simulación
def iniciar_simulacion():
    global lista_procesos
    lista_procesos = obtener_lista_procesos()
    
    # Iniciar la simulación en un hilo separado
    threading.Thread(target=simulacion_round_robin, args=(lista_procesos,)).start()



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

# Crear la tabla de procesos (Treeview)
process_table = ttk.Treeview(process_frame)
process_table['columns'] = ('TL', 'TC')
process_table.column('#0', width=50, minwidth=50, anchor='center')
process_table.column('TL', width=100, minwidth=100, anchor='center')
process_table.column('TC', width=100, minwidth=100, anchor='center')
process_table.heading('#0', text='P', anchor='center')
process_table.heading('TL', text='TL', anchor='center')
process_table.heading('TC', text='TC', anchor='center')

# Insertar datos de ejemplo en la tabla de procesos
process_table.insert('', 'end', text='A', values=('1', '3'))
process_table.insert('', 'end', text='B', values=('4', '5'))
process_table.insert('', 'end', text='C', values=('1', '2'))
process_table.insert('', 'end', text='D', values=('5', '3'))

process_table.grid(row=1, column=0, padx=5, pady=5)

# Crear el label sobre la tabla de procesos
process_label = tk.Label(process_frame, text="Tabla de Procesos", font=("Arial", 14, "bold"))
process_label.grid(row=0, column=0, padx=5, pady=5)

# Crear la memoria principal (representada con etiquetas de colores)
memory_frame = tk.Frame(main_frame, relief='sunken', borderwidth=2)
memory_frame.grid(row=0, column=1, padx=5, pady=5)

# Agregar los rectángulos de colores para representar la memoria principal
system_os = tk.Label(memory_frame, text="S.O.\n" * 1, background="blue", wraplength=50)
system_os.pack(side='bottom', fill='x')

process_a = tk.Label(memory_frame, text="A\n" * 2, background="green", wraplength=50)
process_a.pack(side='bottom', fill='x')

process_b = tk.Label(memory_frame, text="B\n" * 2, background="red", wraplength=50)
process_b.pack(side='bottom', fill='x')

process_c = tk.Label(memory_frame, text="C\n" * 2, background="red", wraplength=50)
process_c.pack(side='bottom', fill='x')

# Crear el frame para mostrar información sobre la CPU
cpu_frame = tk.LabelFrame(main_frame, text="CPU", relief='raised', borderwidth=2)
cpu_frame.grid(row=0, column=2, padx=5, pady=5)

# Agregar elementos relacionados con la CPU
planificador_label = tk.Label(cpu_frame, text="Planificador: ")
planificador_label.pack()

planificador_value = tk.Label(cpu_frame, text="Libre", font=("Arial", 12, "bold"))
planificador_value.pack()

contador_programa_label = tk.Label(cpu_frame, text="Contador de Programa: ")
contador_programa_label.pack()

contador_programa_value = tk.Label(cpu_frame, text="", font=("Arial", 12, "bold"))
contador_programa_value.pack()

base_limite_label = tk.Label(cpu_frame, text="Base y Límite: ")
base_limite_label.pack()

base_limite_values = tk.Label(cpu_frame, text="Base: 0, Límite: 0", font=("Arial", 12, "bold"))
base_limite_values.pack()

# Crear un frame para mostrar la hora del sistema y el contador
time_frame = tk.Frame(main_frame)
time_frame.grid(row=1, column=2, columnspan=4, padx=5, pady=5, sticky='s')

# Mostrar la hora del sistema dinámicamente
hora = tk.StringVar(value='')   
hora_sistema = tk.Label(time_frame, textvariable=hora, font=("Arial", 12))
hora_sistema.pack()

# Mostrar el contador dinámicamente
contador = tk.IntVar(value=0)   
lblcontador = tk.Label(time_frame, textvariable=contador, font=("Arial", 12))
lblcontador.pack()

# Botón para iniciar la simulación de la planificación de procesos
iniciar_button = tk.Button(main_frame, text="Iniciar Simulación", command=iniciar_simulacion)
iniciar_button.grid(row=2, column=0, columnspan=4, pady=10)

# Función para actualizar la hora del sistema en tiempo real
def update_time():
    while True:
        hora_actual = datetime.datetime.now().strftime("Hora del sistema\n%H:%M:%S hrs")
        hora.set(hora_actual)
        time.sleep(1)

# Hilos para actualizar el contador y la hora del sistema en segundo plano
hilo_contador = threading.Thread(target=update_time)
hilo_contador.start()

# Ejecutar el bucle principal de la interfaz gráfica
root.mainloop()
