import tkinter as tk
from tkinter import ttk
from conexion import conectar

def modulo_proveedores():
    ventana = tk.Toplevel()
    ventana.title("Proveedores")
    ventana.geometry("600x400")

    tree = ttk.Treeview(ventana, columns=("ID", "Nombre", "Teléfono", "Email", "Contacto"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Teléfono", text="Teléfono")
    tree.heading("Email", text="Email")
    tree.heading("Contacto", text="Contacto")
    tree.pack(fill=tk.BOTH, expand=True, pady=10)

    def cargar_proveedores():
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_proveedor, nombre, telefono, email, contacto FROM proveedores")
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)
        cursor.close()
        conexion.close()

    cargar_proveedores()