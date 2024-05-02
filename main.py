import tkinter as tk
from tkinter import ttk, messagebox
import time

# Constantes
MEMORIA_SIZE = 1024  # Tamaño de la memoria principal (en bytes)
SISTEMA_OPERATIVO_SIZE = 256  # Tamaño reservado para el sistema operativo
QUANTUM = 5  # Quantum de tiempo para el algoritmo Round-robin (en segundos)

# Clase Proceso
class Proceso:
    def __init__(self, id, tiempo_llegada, tiempo_consumo):
        self.id = id
        self.tiempo_llegada = tiempo_llegada
        self.tiempo_consumo = tiempo_consumo
        self.tiempo_restante = tiempo_consumo
        self.estado = "Listo"
        self.hora_inicio = None
        self.hora_finalizacion = None

# Función para agregar un proceso a la memoria principal
def agregar_proceso(proceso):
    espacio_disponible = buscar_espacio_disponible(proceso.tiempo_consumo)
    if espacio_disponible is not None:
        inicio, fin = espacio_disponible
        canvas_memoria.create_rectangle(10, inicio * 20 + 10, 200, fin * 20 + 10, fill="green", outline="")
        canvas_memoria.create_text(30, (inicio + fin) * 10 + 15, text=proceso.id, font=("Arial", 10))
        procesos_en_memoria.append((proceso, inicio, fin))
        tabla_procesos.insert("", "end", values=(proceso.id, proceso.tiempo_llegada, proceso.tiempo_consumo))
    else:
        messagebox.showerror("Error", "No hay suficiente espacio en memoria principal para el proceso.")

# Función para buscar un espacio disponible en la memoria principal
def buscar_espacio_disponible(tamano):
    inicio = SISTEMA_OPERATIVO_SIZE
    fin = inicio
    while fin < MEMORIA_SIZE:
        if any(inicio >= rango[1] or fin <= rango[2] for rango in procesos_en_memoria):
            inicio = fin + 1  # Avanzar inicio al siguiente espacio disponible
            fin = inicio
        else:
            if fin - inicio + 1 >= tamano:  # Espacio suficiente encontrado
                return inicio, fin
            else:
                fin += 1
    return None  # No se encontró espacio disponible

# Función para eliminar un proceso de la memoria principal
def eliminar_proceso(proceso):
    for i, (p, inicio, fin) in enumerate(procesos_en_memoria):
        if p == proceso:
            canvas_memoria.create_rectangle(10, inicio * 20 + 10, 200, fin * 20 + 10, fill="white", outline="")
            procesos_en_memoria.pop(i)
            break

# Función para planificar los procesos (Round-robin)
def planificador():
    global proceso_en_ejecucion
    for proceso in procesos:
        if proceso.estado == "Listo":
            proceso.estado = "En ejecución"
            proceso.hora_inicio = time.strftime("%H:%M:%S")
            tabla_procesos.item(tabla_procesos.get_children()[procesos.index(proceso)], values=(proceso.id, proceso.tiempo_llegada, proceso.tiempo_consumo, proceso.estado, proceso.hora_inicio, ""))
            proceso_en_ejecucion = proceso
            for i in range(QUANTUM):
                if proceso.tiempo_restante > 0:
                    proceso.tiempo_restante -= 1
                    mostrar_instruccion_en_ejecucion(proceso)
                    time.sleep(1)
                    actualizar_reloj()
            if proceso.tiempo_restante == 0:
                proceso.estado = "Finalizado"
                proceso.hora_finalizacion = time.strftime("%H:%M:%S")
                tabla_procesos.item(tabla_procesos.get_children()[procesos.index(proceso)], values=(proceso.id, proceso.tiempo_llegada, proceso.tiempo_consumo, proceso.estado, proceso.hora_inicio, proceso.hora_finalizacion))
                eliminar_proceso(proceso)
            else:
                proceso.estado = "Listo"
                tabla_procesos.item(tabla_procesos.get_children()[procesos.index(proceso)], values=(proceso.id, proceso.tiempo_llegada, proceso.tiempo_consumo, proceso.estado, proceso.hora_inicio, ""))
    # Programar la ejecución recursiva del planificador
    root.after(1000, planificador)

# Función para mostrar la instrucción en ejecución
def mostrar_instruccion_en_ejecucion(proceso):
    global proceso_en_ejecucion
    if proceso_en_ejecucion is None:
        return
    inicio, fin = next((rango[1], rango[2]) for rango in procesos_en_memoria if rango[0] == proceso_en_ejecucion)
    direccion_instruccion = inicio * 20 + 10 + proceso.tiempo_consumo - proceso.tiempo_restante
    canvas_memoria.create_rectangle(10, direccion_instruccion, 200, direccion_instruccion + 10, fill="yellow", outline="")
    canvas_memoria.create_text(30, direccion_instruccion + 5, text=f"Instrucción en ejecución: {hex(direccion_instruccion)}", font=("Arial", 10))

# Función para actualizar el reloj del sistema
def actualizar_reloj():
    reloj_actual = time.strftime("%H:%M:%S")
    label_reloj.config(text=f"Hora del sistema\n{reloj_actual} hrs")
    root.after(1000, actualizar_reloj)

# Función para agregar un proceso a la tabla de procesos
def agregar_proceso_tabla():
    tiempo_llegada = entrada_tiempo_llegada.get()
    tiempo_consumo = entrada_tiempo_consumo.get()
    if tiempo_llegada.isdigit() and tiempo_consumo.isdigit():
        nuevo_proceso = Proceso(f"P{len(procesos) + 1}", int(tiempo_llegada), int(tiempo_consumo))
        procesos.append(nuevo_proceso)
        agregar_proceso(nuevo_proceso)
    else:
        messagebox.showerror("Error", "Los tiempos de llegada y consumo deben ser números enteros.")

# Crear la ventana principal
root = tk.Tk()
root.title("URL 2024")

# Crear el frame principal
frame_principal = tk.Frame(root)
frame_principal.pack(padx=10, pady=10)

# Crear el frame para la tabla de procesos
frame_tabla = tk.Frame(frame_principal)
frame_tabla.grid(row=0, column=0, padx=5, pady=5)

# Crear la tabla de procesos
tabla_procesos = ttk.Treeview(frame_tabla, columns=("P", "TL", "TC", "Estado", "Hora Inicio", "Hora Fin"))
tabla_procesos.heading("#0", text="P")
tabla_procesos.heading("P", text="P")
tabla_procesos.heading("TL", text="TL")
tabla_procesos.heading("TC", text="TC")
tabla_procesos.heading("Estado", text="Estado")
tabla_procesos.heading("Hora Inicio", text="Hora Inicio")
tabla_procesos.heading("Hora Fin", text="Hora Fin")
tabla_procesos.column("#0", width=50)
tabla_procesos.column("P", width=50)
tabla_procesos.column("TL", width=50)
tabla_procesos.column("TC", width=50)
tabla_procesos.column("Estado", width=100)
tabla_procesos.column("Hora Inicio", width=100)
tabla_procesos.column("Hora Fin", width=100)
tabla_procesos.grid(row=1, column=0, padx=5, pady=5)

# Crear el canvas para la memoria
# Crear el frame para la memoria principal y la CPU
frame_memoria_cpu = tk.Frame(frame_principal)
frame_memoria_cpu.grid(row=0, column=1, padx=10, pady=10)

# Crear el canvas para la memoria principal
canvas_memoria = tk.Canvas(frame_memoria_cpu, width=210, height=400, bg="white")
canvas_memoria.grid(row=0, column=0, padx=5, pady=5)

# Dibujar el espacio para el sistema operativo
canvas_memoria.create_rectangle(10, 10, 200, 50, fill="blue", outline="")
canvas_memoria.create_text(105, 30, text="S.O.", font=("Arial", 10))

# Crear el frame para la CPU
frame_cpu = tk.Frame(frame_memoria_cpu, relief="solid", borderwidth=1)
frame_cpu.grid(row=0, column=1, padx=10, pady=10)

# Crear la sección de la CPU
label_planificador = tk.Label(frame_cpu, text="Planificador", font=("Arial", 12, "bold"))
label_planificador.pack(pady=5)

label_proceso_actual = tk.Label(frame_cpu, text="A", font=("Arial", 10))
label_proceso_actual.pack(pady=2)

label_contador_programa = tk.Label(frame_cpu, text="Contador de programa", font=("Arial", 10))
label_contador_programa.pack(pady=2)

label_contador_valor = tk.Label(frame_cpu, text="d", font=("Arial", 10))
label_contador_valor.pack(pady=2)

label_base = tk.Label(frame_cpu, text="Base: b", font=("Arial", 10))
label_base.pack(pady=2)

label_limite = tk.Label(frame_cpu, text="Límite: b", font=("Arial", 10))
label_limite.pack(pady=2)

# Crear el frame para la tabla de procesos en ejecución
frame_tabla_ejecucion = tk.Frame(frame_cpu, relief="solid", borderwidth=1)
frame_tabla_ejecucion.pack(pady=10)

tabla_ejecucion = ttk.Treeview(frame_tabla_ejecucion, columns=("ID", "Estado", "Hora Inicio", "Hora Fin"), show="headings", height=3)
tabla_ejecucion.heading("ID", text="ID")
tabla_ejecucion.heading("Estado", text="Estado")
tabla_ejecucion.heading("Hora Inicio", text="Hora Inicio")
tabla_ejecucion.heading("Hora Fin", text="Hora Fin")
tabla_ejecucion.column("ID", width=50, anchor="center")
tabla_ejecucion.column("Estado", width=100, anchor="center")
tabla_ejecucion.column("Hora Inicio", width=100, anchor="center")
tabla_ejecucion.column("Hora Fin", width=100, anchor="center")
tabla_ejecucion.pack()

# Crear el label para el reloj del sistema
label_reloj = tk.Label(root, text="Hora del sistema\n00:00:00 hrs", font=("Arial", 12))
label_reloj.pack(pady=10)

# Crear el botón "Iniciar"
boton_iniciar = tk.Button(root, text="Iniciar", command=planificador)
boton_iniciar.pack(pady=10)

# Crear la entrada para el tiempo de llegada y consumo
frame_entrada = tk.Frame(root)
frame_entrada.pack(pady=10)

label_tiempo_llegada = tk.Label(frame_entrada, text="Tiempo de llegada (segundos):")
label_tiempo_llegada.pack(side=tk.LEFT, padx=5)
entrada_tiempo_llegada = tk.Entry(frame_entrada)
entrada_tiempo_llegada.pack(side=tk.LEFT, padx=5)

label_tiempo_consumo = tk.Label(frame_entrada, text="Tiempo de consumo (segundos):")
label_tiempo_consumo.pack(side=tk.LEFT, padx=5)
entrada_tiempo_consumo = tk.Entry(frame_entrada)
entrada_tiempo_consumo.pack(side=tk.LEFT, padx=5)

boton_agregar = tk.Button(frame_entrada, text="Agregar proceso", command=agregar_proceso_tabla)
boton_agregar.pack(side=tk.LEFT, padx=5)

# Inicializar variables
procesos = []
procesos_en_memoria = []
proceso_en_ejecucion = None

# Iniciar el reloj del sistema
actualizar_reloj()

# Iniciar el bucle principal de la ventana
root.mainloop() 