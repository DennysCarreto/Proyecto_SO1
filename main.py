import tkinter as tk
from tkinter import ttk
import datetime, time
import threading

# Mutex para controlar el acceso a la región crítica
mutex = threading.Lock()


# Función para actualizar la región crítica (buffer)
def actualizar_region_critica():
    datos_actualizados = ''
    for i in range(CANTIDAD_BUFFER):
        datos_actualizados += '[' + str(buffer[i]) + '] '
    datos_buffer.set(datos_actualizados)


# def edit_cell(event):
#     row = process_table.identify_row(event.y)
#     column = process_table.identify_column(event.x)
#     if row:  # Verificar que la fila no esté vacía
#         x, y, width, height = process_table.bbox(row, column)
#
#         # Crear un campo de entrada para editar el valor
#         entry = tk.Entry(process_table)
#         entry.place(x=x, y=y, width=width, height=height)
#         entry.insert(0, process_table.set(row, column))
#
#         def save_value():
#             process_table.set(row, column, entry.get())
#             entry.destroy()
#
#         def on_return(event):
#             save_value()
#
#         def on_focus_out(event):
#             save_value()
#
#         entry.bind('<Return>', on_return)
#         entry.bind('<FocusOut>', on_focus_out)
#         entry.focus_set()


def update_time():
    while True:
        hora_actual = datetime.datetime.now().strftime("Hora del sistema\n%H:%M:%S hrs")
        hora.set(hora_actual)
        time.sleep(1)


def update_contador():
    while True:
        contador.set(contador.get() + 1)
        time.sleep(1)


# Función para editar los elementos de la tabla
def edit_cell(event):
    row = process_table.identify_row(event.y)
    column = process_table.identify_column(event.x)
    if row:  # Verificar que la fila no esté vacía.
        x, y, width, height = process_table.bbox(row, column)

        # Crear un campo de entrada para editar el valor
        entry = tk.Entry(process_table)
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, process_table.set(row, column))

        def save_value():
            process_table.set(row, column, entry.get())
            entry.destroy()

        def on_return(event):
            save_value()

        def on_focus_out(event):
            save_value()

        entry.bind('<Return>', on_return)
        entry.bind('<FocusOut>', on_focus_out)
        entry.focus_set()

def insertar_elemento():
    if process_table.get_children():  # Verificar si hay procesos en la tabla
        # Obtener el primer proceso de la tabla
        proceso = process_table.item(process_table.get_children()[0])['values'][0]
        tiempo_llegada = int(process_table.item(process_table.get_children()[0])['values'][1])
        tiempo_consumo = int(process_table.item(process_table.get_children()[0])['values'][2])

        # Obtener la fecha y hora de inicio
        inicio = datetime.datetime.now()

        # Simular la llegada del proceso
        time.sleep(tiempo_llegada)

        # Adquirir el mutex antes de acceder a la región crítica
        with mutex:
            # Encontrar el primer espacio libre de izquierda a derecha
            for i in range(CANTIDAD_BUFFER):
                if buffer[i] == 0:
                    posicion = i
                    break
            buffer[posicion] = proceso
            actualizar_region_critica()

        # Simular el consumo del proceso
        time.sleep(tiempo_consumo)

        # Obtener la fecha y hora de fin
        fin = datetime.datetime.now()

        # Adquirir el mutex antes de acceder a la región crítica
        with mutex:
            # Encontrar la posición del proceso en el buffer
            posicion = buffer.index(proceso)
            buffer[posicion] = 0
            actualizar_region_critica()

        # Actualizar la tabla con la fecha y hora de inicio y fin
        process_table.set(process_table.get_children()[0], 'Inicio', inicio.strftime("%Y-%m-%d %H:%M:%S"))
        process_table.set(process_table.get_children()[0], 'Fin', fin.strftime("%Y-%m-%d %H:%M:%S"))

        # Guardar los detalles del proceso en un archivo de texto
        with open("procesos_terminados.txt", "a") as file:
            file.write(f"Proceso: {proceso}, Inicio: {inicio.strftime('%Y-%m-%d %H:%M:%S')}, Fin: {fin.strftime('%Y-%m-%d %H:%M:%S')}\n")

        print(f'Proceso {proceso} terminado')

        # Eliminar el proceso de la tabla después de un tiempo
        process_table.after(2000, lambda: process_table.delete(process_table.get_children()[0]))

        # Llamar a la función de nuevo si quedan procesos en la tabla
        if process_table.get_children():
            threading.Thread(target=insertar_elemento).start()

def abrir_ventana_agregar_proceso():
    ventana_agregar = tk.Toplevel(root)
    ventana_agregar.title("Agregar Proceso")

    # Crear las etiquetas y entradas para el proceso, tiempo de llegada y tiempo de consumo
    label_proceso = tk.Label(ventana_agregar, text="Proceso:")
    label_proceso.pack()
    entry_proceso = tk.Entry(ventana_agregar)
    entry_proceso.pack()

    label_tiempo_llegada = tk.Label(ventana_agregar, text="Tiempo de Llegada:")
    label_tiempo_llegada.pack()
    entry_tiempo_llegada = tk.Entry(ventana_agregar)
    entry_tiempo_llegada.pack()

    label_tiempo_consumo = tk.Label(ventana_agregar, text="Tiempo de Consumo:")
    label_tiempo_consumo.pack()
    entry_tiempo_consumo = tk.Entry(ventana_agregar)
    entry_tiempo_consumo.pack()

    # Función para agregar el proceso a la tabla
    def agregar_proceso():
        proceso = entry_proceso.get()
        tiempo_llegada = entry_tiempo_llegada.get()
        tiempo_consumo = entry_tiempo_consumo.get()
        process_table.insert('', 'end', values=(proceso, tiempo_llegada, tiempo_consumo, '', ''))
        ventana_agregar.destroy()

    # Crear el botón "Agregar"
    boton_agregar = tk.Button(ventana_agregar, text="Agregar", command=agregar_proceso)
    boton_agregar.pack(pady=10)


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
process_table = ttk.Treeview(process_frame, columns=('Proceso', 'TLlegada', 'TConsumo', 'Inicio', 'Fin'), show='headings')
process_scrollbar = ttk.Scrollbar(process_frame, orient="vertical", command=process_table.yview)
process_scrollbar.grid(row=1, column=1, sticky='ns')
process_table.configure(yscrollcommand=process_scrollbar.set)
process_table.heading('Proceso', text='Proceso')
process_table.column('Proceso', width=100)
process_table.heading('TLlegada', text='TLlegada')
process_table.column('TLlegada', width=100)
process_table.heading('TConsumo', text='TConsumo')
process_table.column('TConsumo', width=100)
process_table.heading('Inicio', text='Inicio')
process_table.column('Inicio', width=150)
process_table.heading('Fin', text='Fin')
process_table.column('Fin', width=150)
# Insertar datos de ejemplo en la tabla de procesos
process_table.insert('', 'end', values=('A', '1', '3', '', ''))
process_table.insert('', 'end', values=('B', '4', '5', '', ''))
process_table.insert('', 'end', values=('C', '1', '2', '', ''))
process_table.insert('', 'end', values=('D', '5', '3', '', ''))

process_table.grid(row=1, column=0, padx=5, pady=5)

# Enlazar la función edit_cell al evento <Double-1> del Treeview
process_table.bind('<Double-1>', edit_cell)

# Crear el label sobre la tabla de procesos
process_label = tk.Label(process_frame, text="Tabla de Procesos", font=("Arial", 14, "bold"))
process_label.grid(row=0, column=0, padx=5, pady=5)


# Crear la memoria principal
memory_frame = tk.Frame(main_frame, relief='sunken', borderwidth=2)
memory_frame.grid(row=0, column=1, padx=5, pady=5)

# Configuración de grid para más control sobre la disposición
memory_frame.columnconfigure(0, weight=1)  # Esto hace que la columna dentro de memory_frame sea expandible

# Crear el label sobre la Memoria
memory_label = tk.Label(memory_frame, text="Memoria Principal", font=("Arial", 14, "bold"))
memory_label.grid(row=0, column=0, sticky='ew')

# Agregar los rectángulos de colores para representar la memoria principal
system_os = tk.Label(memory_frame, text="S.O.\n" * 1, background="blue", wraplength=100)
system_os.grid(row=4, column=0, sticky='ew')

process_a = tk.Label(memory_frame, text="A\n" * 2, background="green", wraplength=100)
process_a.grid(row=3, column=0, sticky='ew')

process_b = tk.Label(memory_frame, text="B\n" * 2, background="red", wraplength=100)
process_b.grid(row=2, column=0, sticky='ew')

process_c = tk.Label(memory_frame, text="C\n" * 2, background="red", wraplength=100)
process_c.grid(row=1, column=0, sticky='ew')


# Crear el CPU
cpu_frame = tk.LabelFrame(main_frame, text="CPU", relief='raised', borderwidth=2)
cpu_frame.grid(row=0, column=2, padx=5, pady=5)

proceso_table = ttk.Treeview(cpu_frame, height=3)
proceso_table['columns'] = ('Estado', 'Hora inicio', 'Hora fin')
cpu_scrollbar = ttk.Scrollbar(cpu_frame, orient="vertical", command=proceso_table.yview)
cpu_scrollbar.pack(side='right', fill='y')
proceso_table.configure(yscrollcommand=cpu_scrollbar.set)

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


# Crear un frame para el buffer y la hora del sistema
buffer_frame = tk.Frame(main_frame)
buffer_frame.grid(row=0, column=1, padx=5, pady=5)

# Crear el buffer
CANTIDAD_BUFFER = 5
buffer = [0] * CANTIDAD_BUFFER
datos_buffer = tk.StringVar(value='[0] [0] [0] [0] [0] ')
buffer_label = tk.Label(buffer_frame, textvariable=datos_buffer, font=("Arial", 25))
buffer_label.pack(pady=5)

# Crear un frame para la hora del sistema
time_frame = tk.Frame(main_frame)
time_frame.grid(row=1, column=2, columnspan=4, padx=5, pady=5, sticky='s')

# Agregar la hora del sistema
hora = tk.StringVar(value='')  # hora
hora_sistema = tk.Label(time_frame, textvariable=hora, font=("Arial", 12))
hora_sistema.pack(pady=5)

# Contador
contador = tk.IntVar(value=0)  # contador = 0
lblcontador = tk.Label(time_frame, textvariable=contador, font=("Arial", 12))
lblcontador.pack(pady=5)

# Crear el botón "Iniciar"
iniciar_button = tk.Button(main_frame, text="Iniciar", command=lambda: threading.Thread(target=insertar_elemento).start())
iniciar_button.grid(row=1, column=0, columnspan=2, pady=10)
# Crear el botón "Agregar Proceso"
agregar_proceso_button = tk.Button(main_frame, text="Agregar Proceso", command=abrir_ventana_agregar_proceso)
agregar_proceso_button.grid(row=2, column=0, columnspan=2, pady=10)

# Hilos para actualización de la hora y contador
hilo_contador = threading.Thread(target=update_contador)
hilo_contador.start()
hilo_time = threading.Thread(target=update_time)
hilo_time.start()

root.mainloop()
