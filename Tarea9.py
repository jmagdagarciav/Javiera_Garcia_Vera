import mysql.connector
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# -------------------
# Conexión a MySQL
# -------------------
def conectar():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            port=3307,
            user="javiera",
            password="0903",
            database="agencia_vehiculos"  # Cambia según tu base
        )
        return conexion
    except mysql.connector.Error as err:
        messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos:\n{err}")
        return None

# -------------------
# Funciones CRUD
# -------------------
def agregar_vehiculo():
    con = conectar()
    if con is None:
        return
    try:
        cursor = con.cursor()
        cursor.execute("""
            INSERT INTO Vehiculos (Marca, Modelo, Año, Combustible, Disponible)
            VALUES (%s, %s, %s, %s, %s)
        """, (entry_marca.get(), entry_modelo.get(), entry_ano.get(), entry_combustible.get(), True))
        con.commit()
        messagebox.showinfo("Éxito", "Vehículo agregado correctamente ✅")
        mostrar_vehiculos()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo agregar el vehículo:\n{e}")
    finally:
        con.close()

def mostrar_vehiculos():
    for fila in tree.get_children():
        tree.delete(fila)
    con = conectar()
    if con is None:
        return
    cursor = con.cursor()
    cursor.execute("SELECT * FROM Vehiculos")
    for row in cursor.fetchall():
        tree.insert("", END, values=row)
    cursor.close()
    con.close()

def actualizar_vehiculo():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Advertencia", "Selecciona un vehículo")
        return
    id_actualizar = tree.item(selected_item)['values'][0]
    con = conectar()
    if con is None:
        return
    cursor = con.cursor()
    cursor.execute("""
        UPDATE Vehiculos SET Marca=%s, Modelo=%s, Año=%s, Combustible=%s, Disponible=%s
        WHERE ID=%s
    """, (entry_marca.get(), entry_modelo.get(), entry_ano.get(), entry_combustible.get(), combo_disponible.get(), id_actualizar))
    con.commit()
    cursor.close()
    con.close()
    mostrar_vehiculos()
    messagebox.showinfo("Éxito", "Vehículo actualizado correctamente 🔄")

def borrar_vehiculo():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Advertencia", "Selecciona un vehículo")
        return
    if messagebox.askyesno("Confirmar", "¿Seguro que deseas eliminar este vehículo?"):
        id_borrar = tree.item(selected_item)['values'][0]
        con = conectar()
        if con is None:
            return
        cursor = con.cursor()
        cursor.execute("DELETE FROM Vehiculos WHERE ID=%s", (id_borrar,))
        con.commit()
        cursor.close()
        con.close()
        mostrar_vehiculos()
        messagebox.showinfo("Éxito", "Vehículo eliminado correctamente 🗑️")

def seleccionar_vehiculo(event):
    selected_item = tree.selection()
    if selected_item:
        values = tree.item(selected_item)['values']
        entry_marca.delete(0, END)
        entry_marca.insert(0, values[1])
        entry_modelo.delete(0, END)
        entry_modelo.insert(0, values[2])
        entry_ano.delete(0, END)
        entry_ano.insert(0, values[3])
        entry_combustible.delete(0, END)
        entry_combustible.insert(0, values[4])
        combo_disponible.set(values[5])

# -------------------
# Interfaz Tkinter
# -------------------
root = Tk()
root.title("Gestión de Vehículos")
root.geometry("800x500")

# Labels y Entradas
Label(root, text="Marca").grid(row=0, column=0, padx=5, pady=5)
entry_marca = Entry(root)
entry_marca.grid(row=0, column=1, padx=5, pady=5)

Label(root, text="Modelo").grid(row=1, column=0, padx=5, pady=5)
entry_modelo = Entry(root)
entry_modelo.grid(row=1, column=1, padx=5, pady=5)

Label(root, text="Año").grid(row=2, column=0, padx=5, pady=5)
entry_ano = Entry(root)
entry_ano.grid(row=2, column=1, padx=5, pady=5)

Label(root, text="Combustible").grid(row=3, column=0, padx=5, pady=5)
entry_combustible = Entry(root)
entry_combustible.grid(row=3, column=1, padx=5, pady=5)

Label(root, text="Disponible").grid(row=4, column=0, padx=5, pady=5)
combo_disponible = ttk.Combobox(root, values=[True, False])
combo_disponible.grid(row=4, column=1, padx=5, pady=5)
combo_disponible.set(True)

# Botones
Button(root, text="Agregar", command=agregar_vehiculo).grid(row=5, column=0, padx=5, pady=10)
Button(root, text="Actualizar", command=actualizar_vehiculo).grid(row=5, column=1, padx=5, pady=10)
Button(root, text="Borrar", command=borrar_vehiculo).grid(row=5, column=2, padx=5, pady=10)
Button(root, text="Mostrar todos", command=mostrar_vehiculos).grid(row=5, column=3, padx=5, pady=10)

# Tabla
columns = ("ID", "Marca", "Modelo", "Año", "Combustible", "Disponible")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
tree.grid(row=6, column=0, columnspan=4, padx=10, pady=10)
tree.bind("<<TreeviewSelect>>", seleccionar_vehiculo)

# Inicializar
mostrar_vehiculos()
root.mainloop()


