
import tkinter as tk
from tkinter import ttk
from conexion import conectar

def modulo_rrhh():
    ventana = tk.Toplevel()
    ventana.title("RRHH - Empleados")
    ventana.geometry("600x400")

    tree = ttk.Treeview(ventana, columns=("ID", "Nombre", "Puesto", "Salario"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Puesto", text="Puesto")
    tree.heading("Salario", text="Salario")
    tree.pack(fill=tk.BOTH, expand=True, pady=10)

    def cargar_empleados():
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_empleado, CONCAT(nombre, ' ', apellidos), puesto, salario FROM empleados")
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)
        cursor.close()
        conexion.close()

    cargar_empleados()
    