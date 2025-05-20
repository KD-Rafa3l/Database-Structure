
import tkinter as tk
from tkinter import ttk, messagebox
from conexion import conectar

def modulo_inventario():
    ventana = tk.Toplevel()
    ventana.title("Inventario")
    ventana.geometry("600x400")

    tree = ttk.Treeview(ventana, columns=("ID", "Nombre", "Precio", "Stock"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Producto")
    tree.heading("Precio", text="Precio")
    tree.heading("Stock", text="Stock")
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
    