
import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Nath@ly+22.",  # <-- CAMBIA ESTO
        database="libreria_papeleria"
    )
    