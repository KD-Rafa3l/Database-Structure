
import tkinter as tk
from tkinter import ttk, messagebox
from conexion import conectar

def modulo_ventas():
    ventana = tk.Toplevel()
    ventana.title("Ventas")
    ventana.geometry("400x300")

    label = tk.Label(ventana, text="Módulo de ventas en desarrollo.")
    label.pack(pady=30)
    