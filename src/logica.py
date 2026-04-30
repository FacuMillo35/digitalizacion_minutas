from conexion_db import obtener_conexion

def buscar_persona_por_dni(dni):
    db = obtener_conexion()
    if db:
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM personas WHERE dni = %s"
        cursor.execute(query, (dni,))
        resultado = cursor.fetchone()
        db.close()
        return resultado
    return None
    