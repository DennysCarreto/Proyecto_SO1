import tkinter as tk
from tkinter import ttk
import datetime, time
import threading


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

# Crear la memoria principal
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

proceso_table = ttk.Treeview(cpu_frame, height=3)
proceso_table['columns'] = ('Estado', 'Hora inicio', 'Hora fin')
proceso_table.column('#0', width=50, minwidth=50, anchor='center')
proceso_table.column('Estado', width=100, minwidth=100, anchor='center')
proceso_table.column('Hora inicio', width=100, minwidth=100, anchor='center')
proceso_table.column('Hora fin', width=100, minwidth=100, anchor='center')
proceso_table.heading('#0', text='ID', anchor='center')
proceso_table.heading('Estado', text='Estado', anchor='center')
proceso_table.heading('Hora inicio', text='Hora inicio', anchor='center')
proceso_table.heading('Hora fin', text='Hora fin', anchor='center')

proceso_table.insert('', 'end', text='a', values=('new', '13:00:00', '13:00:04'))
proceso_table.insert('', 'end', text='b', values=('lists', '13:00:04', '13:00:08'))
proceso_table.insert('', 'end', text='c', values=('lists', '13:00:08', ''))

proceso_table.pack(pady=5)

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
iniciar_button = tk.Button(main_frame, text="Iniciar")
iniciar_button.grid(row=2, column=0, columnspan=4, pady=10)

# Hilos para actualización de la hora y contador
hilo_contador = threading.Thread(target=update_contador)
hilo_contador.start()
hilo_time = threading.Thread(target=update_time)
hilo_time.start()


root.mainloop()
