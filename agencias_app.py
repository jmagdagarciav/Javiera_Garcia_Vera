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
            port=3307,             # ⚠️ Ajusta si usas otro puerto MySQL
            user="javiera",
            password="0903",
            database="AgenciasDB"
        )
        return conexion
    except mysql.connector.Error as err:
        messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos:\n{err}")
        return None

# -------------------
# Funciones CRUD
# -------------------

def agregar_agencia():
    try:
        con = conectar()
        if con is None:
            return
        cursor = con.cursor()
        cursor.execute("""
            INSERT INTO AgenciaEspacial (ID, Nombre, Pais, FechaCreacion)
            VALUES (%s, %s, %s, %s)
        """, (entry_id.get(), entry_nombre.get(), entry_pais.get(), entry_fecha.get()))
        con.commit()
        messagebox.showinfo("Éxito", "Agencia agregada correctamente ✅")
        mostrar_agencias()
    except mysql.connector.errors.IntegrityError:
        messagebox.showerror("Error", "El ID ya existe o los datos son inválidos")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo agregar la agencia:\n{e}")
    finally:
        if con:
            con.close()

def mostrar_agencias():
    for fila in tree.get_children():
        tree.delete(fila)
    con = conectar()
    if con is None:
        return
    cursor = con.cursor()
    cursor.execute("SELECT * FROM AgenciaEspacial")
    for row in cursor.fetchall():
        tree.insert("", END, values=row)
    cursor.close()
    con.close()

def borrar_agencia():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Advertencia", "Selecciona una agencia para eliminar")
        return
    respuesta = messagebox.askyesno("Confirmar", "¿Seguro que deseas eliminar esta agencia?")
    if respuesta:
        con = conectar()
        if con is None:
            return
        cursor = con.cursor()
        id_borrar = tree.item(selected_item)['values'][0]
        cursor.execute("DELETE FROM AgenciaEspacial WHERE ID=%s", (id_borrar,))
        con.commit()
        cursor.close()
        con.close()
        mostrar_agencias()
        messagebox.showinfo("Éxito", "Agencia eliminada correctamente 🗑️")

def actualizar_agencia():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Advertencia", "Selecciona una agencia para actualizar")
        return
    id_actualizar = tree.item(selected_item)['values'][0]
    con = conectar()
    if con is None:
        return
    cursor = con.cursor()
    cursor.execute("""
        UPDATE AgenciaEspacial
        SET Nombre=%s, Pais=%s, FechaCreacion=%s
        WHERE ID=%s
    """, (entry_nombre.get(), entry_pais.get(), entry_fecha.get(), id_actualizar))
    con.commit()
    cursor.close()
    con.close()
    mostrar_agencias()
    messagebox.showinfo("Éxito", "Agencia actualizada correctamente 🔄")

def seleccionar_agencia(event):
    selected_item = tree.selection()
    if selected_item:
        values = tree.item(selected_item)['values']
        entry_id.delete(0, END)
        entry_id.insert(0, values[0])
        entry_nombre.delete(0, END)
        entry_nombre.insert(0, values[1])
        entry_pais.delete(0, END)
        entry_pais.insert(0, values[2])
        entry_fecha.delete(0, END)
        entry_fecha.insert(0, values[3])

# -------------------
# Interfaz Tkinter
# -------------------
root = Tk()
root.title("Gestión de Agencias Espaciales")
root.geometry("750x500")
root.resizable(False, False)

# Labels y entradas
Label(root, text="ID", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=10, pady=10)
entry_id = Entry(root)
entry_id.grid(row=0, column=1, padx=10, pady=10)

Label(root, text="Nombre", font=("Arial", 10, "bold")).grid(row=1, column=0, padx=10, pady=10)
entry_nombre = Entry(root, width=50)
entry_nombre.grid(row=1, column=1, padx=10, pady=10)

Label(root, text="País", font=("Arial", 10, "bold")).grid(row=2, column=0, padx=10, pady=10)
entry_pais = Entry(root)
entry_pais.grid(row=2, column=1, padx=10, pady=10)

Label(root, text="Fecha Creación (YYYY-MM-DD)", font=("Arial", 10, "bold")).grid(row=3, column=0, padx=10, pady=10)
entry_fecha = Entry(root)
entry_fecha.grid(row=3, column=1, padx=10, pady=10)

# Botones CRUD
Button(root, text="Agregar", command=agregar_agencia, bg="#4CAF50", fg="white", width=12).grid(row=4, column=0, padx=10, pady=10)
Button(root, text="Actualizar", command=actualizar_agencia, bg="#2196F3", fg="white", width=12).grid(row=4, column=1, padx=10, pady=10)
Button(root, text="Borrar", command=borrar_agencia, bg="#F44336", fg="white", width=12).grid(row=4, column=2, padx=10, pady=10)
Button(root, text="Mostrar todas", command=mostrar_agencias, bg="#9C27B0", fg="white", width=15).grid(row=4, column=3, padx=10, pady=10)

# Tabla Treeview
columns = ("ID", "Nombre", "Pais", "FechaCreacion")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150, anchor="center")
tree.grid(row=5, column=0, columnspan=4, padx=10, pady=20)

tree.bind("<<TreeviewSelect>>", seleccionar_agencia)

# Inicializar mostrando los datos
mostrar_agencias()

root.mainloop()
