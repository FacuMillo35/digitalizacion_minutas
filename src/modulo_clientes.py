import mysql.connector

def guardar_cliente(ventana):
    nombre = ventana.txt_nombre.text().strip()
    apellido = ventana.txt_apellido.text().strip()
    dni = ventana.txt_dni.text().strip()
    domicilio = ventana.txt_domicilio.text().strip()
    
    if not hasattr(ventana, 'datos_conyuge_temp'):
        ventana.datos_conyuge_temp = {"nombre": None, "nupcias": None, "dni": None}
    
    nupcias = ventana.datos_conyuge_temp.get("nupcias")
    if nupcias == "-" or nupcias == "":
        nupcias = None
        
    conyuge = ventana.datos_conyuge_temp.get("nombre")
    if conyuge == "":
        conyuge = None
        
    # --- NUEVO: Capturamos el DNI del cónyuge ---
    dni_conyuge = ventana.datos_conyuge_temp.get("dni")
    if dni_conyuge == "":
        dni_conyuge = None
    
    estado_civil = ventana.cmb_estado_civil.currentText().strip()
    
    if not nombre or not apellido or not dni:
        print("Error: Nombre, Apellido y DNI son obligatorios.")
        return

    conexion = None
    try:
        conexion = mysql.connector.connect(host="localhost", user="root", password="admin123", database="proyecto_final_bd")
        cursor = conexion.cursor()
        
        # Agregamos dni_conyuge al INSERT
        query = """INSERT INTO personas 
                   (nombre, apellido, dni, domicilio, estado_civil, nombre_conyuge, nupcias, dni_conyuge) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        valores = (nombre, apellido, dni, domicilio, estado_civil, conyuge, nupcias, dni_conyuge)
        
        cursor.execute(query, valores)
        conexion.commit()
        print(f"¡Cliente {nombre} {apellido} guardado con éxito!")
        
        ventana.txt_nombre.clear()
        ventana.txt_apellido.clear()
        ventana.txt_dni.clear()
        ventana.txt_domicilio.clear()
        ventana.cmb_estado_civil.setCurrentIndex(0)
        
        # Limpiamos todo al final
        ventana.datos_conyuge_temp = {"nombre": None, "nupcias": None, "dni": None}
        # refrescamos la lista de clientes en la ventana de minutas
        ventana.cargar_combos_minutas()
        
    except mysql.connector.Error as error:
        print(f"Error al guardar cliente: {error}")
    finally:
        if conexion and conexion.is_connected():
            cursor.close()
            conexion.close()