# modulo_clientes.py
import mysql.connector

# Fijate que en vez de 'self', le pasamos 'ventana'
def guardar_cliente(ventana):
    nombre = ventana.txt_nombre.text().strip()
    apellido = ventana.txt_apellido.text().strip()
    dni = ventana.txt_dni.text().strip()
    domicilio = ventana.txt_domicilio.text().strip()
    
    nupcias = ventana.cmb_nupcias.currentText()
    if nupcias == "-":
        nupcias = None
    
    estado_civil = ventana.cmb_estado_civil.currentText().strip()
    conyuge = ventana.txt_nombre_conyuge.text().strip() if ventana.txt_nombre_conyuge.isEnabled() else None
    
    if not nombre or not apellido or not dni:
        print("Error: Nombre, Apellido y DNI son obligatorios.")
        return

    conexion = None
    try:
        conexion = mysql.connector.connect(host="localhost", user="root", password="admin123", database="proyecto_final_bd")
        cursor = conexion.cursor()
        
        query = """INSERT INTO personas 
                   (nombre, apellido, dni, domicilio, estado_civil, nombre_conyuge, nupcias) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        valores = (nombre, apellido, dni, domicilio, estado_civil, conyuge, nupcias)
        
        cursor.execute(query, valores)
        conexion.commit()
        print(f"¡Cliente {nombre} {apellido} guardado con éxito!")
        
        # Limpiamos usando 'ventana'
        ventana.txt_nombre.clear()
        ventana.txt_apellido.clear()
        ventana.txt_dni.clear()
        ventana.txt_domicilio.clear()
        ventana.txt_nombre_conyuge.clear()
        ventana.cmb_estado_civil.setCurrentIndex(0)
        ventana.cmb_nupcias.setCurrentIndex(0)
        
    except mysql.connector.Error as error:
        print(f"Error al guardar cliente: {error}")
    finally:
        if conexion and conexion.is_connected():
            cursor.close()
            conexion.close()