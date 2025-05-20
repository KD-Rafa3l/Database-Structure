
import tkinter as tk
from tkinter import ttk, messagebox
from conexion import conectar

def modulo_clientes():
    ventana = tk.Toplevel()
    ventana.title("Clientes")
    ventana.geometry("600x400")

    tree = ttk.Treeview(ventana, columns=("ID", "Nombre", "Teléfono", "Email"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Teléfono", text="Teléfono")
    tree.heading("Email", text="Email")
    tree.pack(fill=tk.BOTH, expand=True, pady=10)

    def cargar_clientes():
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_cliente, nombre, telefono, email FROM clientes")
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)
        cursor.close()
        conexion.close()

    cargar_clientes()
    