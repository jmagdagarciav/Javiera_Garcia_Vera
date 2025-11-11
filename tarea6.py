import json
import os

# Archivos para guardar datos
ARCH_PROVEEDORES = "proveedores.json"
ARCH_ARTICULOS = "articulos.json"

# --- Funciones auxiliares ---

def cargar_datos(archivo):
    """Carga datos desde un archivo JSON o devuelve lista vacía si no existe"""
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return []

def guardar_datos(archivo, datos):
    """Guarda lista de datos en un archivo JSON"""
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

# --- Inicialización de datos ---
proveedores = cargar_datos(ARCH_PROVEEDORES)
articulos = cargar_datos(ARCH_ARTICULOS)

# --- Funciones principales ---
def agregar_proveedor():
    nombre = input("Nombre del proveedor: ")
    ubicacion = input("Ubicación del proveedor: ")
    proveedor = {"nombre": nombre, "ubicacion": ubicacion}
    proveedores.append(proveedor)
    guardar_datos(ARCH_PROVEEDORES, proveedores)
    print("✅ Proveedor agregado.\n")

def agregar_articulo():
    nombre = input("Nombre del artículo: ")
    categoria = input("Categoría: ")
    precio = float(input("Precio: "))
    proveedor = input("Proveedor asociado: ")

    # Validar que exista el proveedor
    nombres_prov = [p["nombre"] for p in proveedores]
    if proveedor not in nombres_prov:
        print("⚠️ El proveedor no existe. Agrega primero el proveedor.\n")
        return

    articulo = {
        "nombre": nombre,
        "categoria": categoria,
        "precio": precio,
        "proveedor": proveedor
    }
    articulos.append(articulo)
    guardar_datos(ARCH_ARTICULOS, articulos)
    print("✅ Artículo agregado.\n")

def mostrar_informacion():
    print("\n=== Proveedores ===")
    print(json.dumps(proveedores, indent=4, ensure_ascii=False))
    print("\n=== Artículos ===")
    print(json.dumps(articulos, indent=4, ensure_ascii=False))
    print()

# --- Menú principal ---
def menu():
    while True:
        print("----- Menú -----")
        print("1. Agregar proveedor")
        print("2. Agregar artículo")
        print("3. Mostrar información")
        print("4. Salir")
        opcion = input("Elija una opción: ")

        if opcion == "1":
            agregar_proveedor()
        elif opcion == "2":
            agregar_articulo()
        elif opcion == "3":
            mostrar_informacion()
        elif opcion == "4":
            print("Saliendo...")
            break
        else:
            print("Opción inválida.\n")

# --- Ejecución ---
menu()
