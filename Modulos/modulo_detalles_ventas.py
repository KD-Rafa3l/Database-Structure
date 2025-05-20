import tkinter as tk
from tkinter import ttk
from conexion import conectar

def modulo_detalles_ventas():
    ventana = tk.Toplevel()
    ventana.title("Detalles de Ventas")
    ventana.geometry("800x400")

    tree = ttk.Treeview(ventana, columns=("ID Detalle", "ID Venta", "ID Producto", "Cantidad", "Precio Unitario"), show="headings")
    tree.heading("ID Detalle", text="ID Detalle")
    tree.heading("ID Venta", text="ID Venta")
    tree.heading("ID Producto", text="ID Producto")
    tree.heading("Cantidad", text="Cantidad")
    tree.heading("Precio Unitario", text="Precio Unitario")
    tree.pack(fill=tk.BOTH, expand=True, pady=10)

    def cargar_detalles():
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_detalle, id_venta, id_producto, cantidad, precio_unitario FROM detalles_venta")
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)
        cursor.close()
        conexion.close()

    cargar_detalles()