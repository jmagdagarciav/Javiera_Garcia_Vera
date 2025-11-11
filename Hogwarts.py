def obtener_cantidad(prompt):
    while True:
        try:
            valor = int(input(prompt))
            if valor < 0:
                print("Error: La cantidad no puede ser negativa. Intenta nuevamente.")
            else:
                return valor
        except ValueError:
            print("Error: Debes ingresar un número entero válido.")

def main():
    print("Bienvenido al sistema de inventario de Hogwarts\n")

    while True:
        # Solicitar cantidad en existencia
        libros_existencia = obtener_cantidad("Ingresa la cantidad de libros en existencia: ")

        # Solicitar cantidad vendida
        libros_vendidos = obtener_cantidad("Ingresa la cantidad de libros vendidos hoy: ")

        # Verificar que no se vendieron más libros de los que existen
        if libros_vendidos > libros_existencia:
            print("Error: La cantidad vendida no puede exceder la cantidad en inventario. Intenta nuevamente.\n")
        else:
            libros_restantes = libros_existencia - libros_vendidos
            print("\nRegistro exitoso.")
            print(f"Libros vendidos hoy: {libros_vendidos}")
            print(f"Libros restantes en inventario: {libros_restantes}")
            break

if __name__ == "__main__":
    main()

