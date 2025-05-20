import tkinter as tk
from tkinter import ttk
from conexion import conectar

def modulo_productos():
    ventana = tk.Toplevel()
    ventana.title("Gestión de Productos")
    ventana.geometry("600x400")

    tree = ttk.Treeview(ventana, columns=("ID", "Nombre", "Precio Venta", "Stock Mínimo"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Precio Venta", text="Precio Venta")
    tree.heading("Stock Mínimo", text="Stock Mínimo")
    tree.pack(fill=tk.BOTH, expand=True, pady=10)

    def cargar_productos():
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_producto, nombre, precio_venta, stock_minimo FROM productos")
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)
        cursor.close()
        conexion.close()

    cargar_productos()