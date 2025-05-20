import tkinter as tk
from tkinter import ttk
from conexion import conectar

def modulo_categorias():
    ventana = tk.Toplevel()
    ventana.title("Categorías de Productos")
    ventana.geometry("600x400")

    tree = ttk.Treeview(ventana, columns=("ID", "Nombre", "Descripción"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Descripción", text="Descripción")
    tree.pack(fill=tk.BOTH, expand=True, pady=10)

    def cargar_categorias():
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_categoria, nombre, descripcion FROM categorias")
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)
        cursor.close()
        conexion.close()

    cargar_categorias()