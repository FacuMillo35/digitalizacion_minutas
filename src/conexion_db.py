import mysql.connector

def obtener_conexion():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",          # Tu usuario de MySQL Workbench
            password="admin123", # Pon aquí tu contraseña
            database="proyecto_final_bd" # El nombre que le diste en Workbench
        )
        return db
    except mysql.connector.Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None