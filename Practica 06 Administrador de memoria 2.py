import os  # Importa el módulo 'os' para trabajar con el sistema operativo

# Definición de la clase MemoryBlock para representar un bloque de memoria con capacidad y nombre de proceso
class MemoryBlock:
    def __init__(self, capacity):
        self.capacity = capacity  # Capacidad del bloque de memoria en KB
        self.process_name = None  # Nombre del proceso asignado a este bloque

    def allocate(self, process_name):
        self.process_name = process_name  # Asigna un proceso a este bloque

    def deallocate(self):
        self.process_name = None  # Desasigna el proceso de este bloque

# Función para mostrar el estado de los bloques de memoria (ocupados o libres)
def display_memory_blocks(memory_blocks):
    for i, block in enumerate(memory_blocks):
        status = "Occupied" if block.process_name else "Free"  # Estado ocupado o libre
        print(f"Block {i+1} ({block.capacity} KB): {status} - Process: {block.process_name}")

# Algoritmos de asignación de memoria: Primer ajuste, Mejor ajuste, Peor ajuste, Siguiente ajuste
# Cada función intenta asignar un proceso a un bloque de memoria según su algoritmo respectivo

def first_fit(memory_blocks, process_name, size):
    for block in memory_blocks:
        if not block.process_name and block.capacity >= size:  # Si el bloque está libre y tiene suficiente capacidad
            block.allocate(process_name)  # Asigna el proceso a este bloque
            return True  # Devuelve True para indicar asignación exitosa
    return False  # Devuelve False si no se puede asignar el proceso

def best_fit(memory_blocks, process_name, size):
    best_fit_block = None
    for block in memory_blocks:
        if not block.process_name and block.capacity >= size:
            if best_fit_block is None or block.capacity < best_fit_block.capacity:
                best_fit_block = block
    if best_fit_block:
        best_fit_block.allocate(process_name)
        return True
    return False

def worst_fit(memory_blocks, process_name, size):
    worst_fit_block = None
    for block in memory_blocks:
        if not block.process_name and block.capacity >= size:
            if worst_fit_block is None or block.capacity > worst_fit_block.capacity:
                worst_fit_block = block
    if worst_fit_block:
        worst_fit_block.allocate(process_name)
        return True
    return False

def next_fit(memory_blocks, process_name, size, last_allocated_index):
    n = len(memory_blocks)
    for i in range(n):
        index = (last_allocated_index + i) % n
        block = memory_blocks[index]
        if not block.process_name and block.capacity >= size:
            block.allocate(process_name)
            return index
    return -1

# Función para agregar archivos desde un directorio específico al archivo "archivos.txt"
def agregar_archivos_desde_directorio(directorio):
    try:
        with open("archivos.txt", "a") as archivo_salida:  # Abre el archivo "archivos.txt" en modo de escritura (a: append)
            for nombre_archivo in os.listdir(directorio):  # Itera sobre los archivos en el directorio especificado
                ruta_archivo = os.path.join(directorio, nombre_archivo)  # Obtiene la ruta completa del archivo
                if os.path.isfile(ruta_archivo):  # Verifica si el elemento es un archivo
                    tamaño = os.path.getsize(ruta_archivo) // 1024  # Obtiene el tamaño del archivo en KB
                    archivo_salida.write(f"{nombre_archivo}, {tamaño}kb\n")  # Escribe el nombre y tamaño en el archivo "archivos.txt"
            print("Archivos agregados desde el directorio exitosamente.")
    except FileNotFoundError:
        print(f"El directorio '{directorio}' no se encuentra.")

# Función principal del programa
def main():
    num_blocks = int(input("Ingrese el número de bloques de memoria: "))  # Solicita al usuario el número de bloques de memoria
    memory_blocks = []

    for _ in range(num_blocks):
        capacity = int(input(f"Ingrese la capacidad del bloque {len(memory_blocks)+1} en KB: "))
        memory_blocks.append(MemoryBlock(capacity))  # Crea y agrega un bloque de memoria con la capacidad especificada

    while True:
        print("\nElija una opción:\n 1: Asignar proceso\n 2: Agregar bloque de memoria\n 3: Agregar nuevos procesos\n 0: Salir\n ")
        user_choice = input("Opción: ")  # Solicita al usuario que elija una opción

        if user_choice == "0":
            break  # Sale del bucle si el usuario elige la opción 0 (Salir)

        if user_choice == "1":
            while True:
                print("\nElija un algoritmo\n 1: Primer ajuste\n 2: Mejor ajuste\n 3: Peor ajuste\n 4: Siguiente ajuste\n 0: Volver al menú principal\n ")
                algorithm_choice = input("Opción: ")  # Solicita al usuario que elija un algoritmo

                if algorithm_choice == "0":
                    break  # Sale del bucle si el usuario elige la opción 0 (Volver al menú principal)

                if algorithm_choice not in ["1", "2", "3", "4"]:
                    print("Opción no válida. Por favor, ingrese un número válido.")
                    continue  # Continúa solicitando una opción válida si el usuario ingresa un valor no válido

                for block in memory_blocks:
                    block.deallocate()  # Desasigna todos los bloques de memoria

                try:
                    with open("archivos.txt", "r") as file:  # Abre el archivo "archivos.txt" en modo de lectura
                        lines = file.readlines()  # Lee todas las líneas del archivo
                        for line in lines:
                            process_name, size_str = line.strip().split(", ")  # Divide la línea en nombre y tamaño del proceso
                            size = int(size_str[:-2])  # Convierte el tamaño a entero y elimina "kb"

                            allocated = False  # Variable para indicar si se asignó el proceso con éxito
                            if algorithm_choice == "1":
                                allocated = first_fit(memory_blocks, process_name, size)
                            elif algorithm_choice == "2":
                                allocated = best_fit(memory_blocks, process_name, size)
                            elif algorithm_choice == "3":
                                allocated = worst_fit(memory_blocks, process_name, size)
                            elif algorithm_choice == "4":
                                last_allocated_index = -1
                                while True:
                                    last_allocated_index = next_fit(memory_blocks, process_name, size, last_allocated_index)
                                    if last_allocated_index == -1:
                                        break
                                    allocated = True
                                    break

                            if allocated:
                                print(f"Archivo {process_name} asignado con éxito usando el algoritmo seleccionado.")
                            else:
                                print(f"No se pudo asignar el archivo {process_name} usando el algoritmo seleccionado. No hay suficiente espacio.")

                            display_memory_blocks(memory_blocks)  # Muestra el estado de los bloques de memoria

                except FileNotFoundError:
                    print("El archivo 'archivos.txt' no se encuentra.")

        elif user_choice == "2":
            capacity = int(input("Ingrese la capacidad del nuevo bloque de memoria en KB: "))
            position = input("Ingrese 'arriba' o 'abajo' para agregar el bloque de memoria: ")

            if position == "arriba":
                memory_blocks.insert(0, MemoryBlock(capacity))  # Agrega un nuevo bloque de memoria en la parte superior de la lista
            elif position == "abajo":
                memory_blocks.append(MemoryBlock(capacity))  # Agrega un nuevo bloque de memoria al final de la lista
            else:
                print("Posición no válida. Use 'arriba' o 'abajo'.")

        elif user_choice == "3":
            while True:
                print("\nElija una opción para agregar nuevos procesos:\n 1: Desde un archivo físico\n 2: Procesos virtuales\n 0: Volver al menú principal\n ")
                process_choice = input("Opción: ")

                if process_choice == "0":
                    break  # Sale del bucle si el usuario elige la opción 0 (Volver al menú principal)

                if process_choice == "1":
                    directorio = input("Ingrese la ruta del directorio con los archivos (ejemplo: D:\\tareas\\tareas2023B\\sem de so\\Practica 06 Administrador de memoria 2): ")
                    agregar_archivos_desde_directorio(directorio)  # Llama a la función para agregar archivos desde un directorio

                elif process_choice == "2":
                    num_processes = int(input("Ingrese el número de procesos virtuales que desea agregar: "))
                    for _ in range(num_processes):
                        process_name = input("Ingrese el nombre del proceso: ")
                        size = int(input("Ingrese el peso del proceso en KB: "))
                        # Agregar lógica para asignar procesos virtuales
                else:
                    print("Opción no válida. Por favor, ingrese un número válido.")
        else:
            print("Opción no válida. Por favor, ingrese un número válido.")

if __name__ == "__main__":
    main()  # Llama a la función principal cuando se ejecuta el script
