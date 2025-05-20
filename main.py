# Ejemplo para modulo_productos.py (aplicar misma estructura a todos los módulos)
import tkinter as tk
from tkinter import ttk
from conexion import conectar

def modulo_productos(ventana_anterior=None):
    ventana = tk.Toplevel()
    ventana.title("Gestión de Productos")
    ventana.geometry("800x500")
    
    # Frame superior para navegación
    nav_frame = tk.Frame(ventana, bg="#f0f0f0")
    nav_frame.pack(fill=tk.X, padx=10, pady=5)
    
    if ventana_anterior:
        btn_regresar = tk.Button(nav_frame, text="← Regresar", 
                               command=ventana_anterior.destroy)
        btn_regresar.pack(side=tk.LEFT, padx=5)
    
    btn_principal = tk.Button(nav_frame, text="🏠 Principal", 
                            command=lambda: [ventana.destroy(), ventana_principal()])
    btn_principal.pack(side=tk.RIGHT, padx=5)

    # Contenido principal
    main_frame = tk.Frame(ventana)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Treeview
    tree = ttk.Treeview(main_frame, columns=("ID", "Nombre", "Precio", "Stock"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Precio", text="Precio Venta")
    tree.heading("Stock", text="Stock Mínimo")
    tree.pack(fill=tk.BOTH, expand=True)
    
    # Botones de CRUD
    crud_frame = tk.Frame(main_frame)
    crud_frame.pack(pady=10)
    
    tk.Button(crud_frame, text="Agregar", bg="#d4edda").pack(side=tk.LEFT, padx=5)
    tk.Button(crud_frame, text="Editar", bg="#fff3cd").pack(side=tk.LEFT, padx=5)
    tk.Button(crud_frame, text="Eliminar", bg="#f8d7da").pack(side=tk.LEFT, padx=5)
    
    # Cargar datos
    def cargar_datos():
        # Tu código de conexión a BD aquí
        pass
    
    cargar_datos()
