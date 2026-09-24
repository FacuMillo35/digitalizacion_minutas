import mysql.connector
from datetime import date
import modulo_pdf
def guardar_minuta(ventana):
    monto = ventana.txt_monto.text().strip()
    observaciones = ventana.txt_observaciones.toPlainText().strip()
    id_inmueble = ventana.cmb_inmueble.currentData()
    tipo_acto = ventana.txt_especie_derechos.text().strip()
    id_usuario = 1  # ID por defecto para el escribano

    # Recuperamos las IDs de las personas
    vendedores_seleccionados = [
        ventana.list_vendedores.item(i).data(32)
        for i in range(ventana.list_vendedores.count())
        if ventana.list_vendedores.item(i).isSelected()
    ]
    compradores_seleccionados = [
        ventana.list_compradores.item(i).data(32)
        for i in range(ventana.list_compradores.count())
        if ventana.list_compradores.item(i).isSelected()
    ]

    # --- VALIDACIONES ---
    if not id_inmueble or not vendedores_seleccionados or not compradores_seleccionados:
        print("Error: Falta completar inmueble o intervinientes.")
        return

    if not monto:
        monto = "0"

    conexion = None
    try:
        conexion = mysql.connector.connect(
            host="localhost", user="root", password="admin123", database="proyecto_final_bd"
        )
        
        # --- 1. GUARDADO NORMAL EN LA BASE DE DATOS ---
        cursor = conexion.cursor()
        texto_motivo = f"Monto de Operacion: ${monto}"
        
        query_minuta = """
            INSERT INTO minuta_c_inmueble 
            (id_inmueble, id_usuario_escribano, id_usuario, motivo, observaciones, tipo_acto) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query_minuta, (id_inmueble, id_usuario, id_usuario, texto_motivo, observaciones, tipo_acto))
        id_minuta_generada = cursor.lastrowid
        
        query_intermedia = "INSERT INTO intervinientes_minuta (id_minuta, id_persona, rol) VALUES (%s, %s, %s)"
        
        for id_vendedor in vendedores_seleccionados:
            cursor.execute(query_intermedia, (id_minuta_generada, id_vendedor, 'Vendedor'))
        for id_comprador in compradores_seleccionados:
            cursor.execute(query_intermedia, (id_minuta_generada, id_comprador, 'Comprador'))
            
        conexion.commit()
        print(f"¡Excelente! Minuta N° {id_minuta_generada} registrada con éxito.")

        # --- 2. RECOLECCIÓN DE DATOS PARA EL PDF OFICIAL ---
        cursor_dict = conexion.cursor(dictionary=True)
        
        cursor_dict.execute("""
            SELECT domicilio_inmueble as domicilio, entre_calles, lote, manzana, superficie, tipo_propiedad,
                   ph_unidad_funcional as ph_unidad, ph_poligono, ph_porcentaje, tomo_numero, folio_real, anio_inscripcion,
                   nom_circunscripcion, nom_seccion, nom_manzana, nom_parcela
            FROM inmuebles WHERE id_inmueble = %s
        """, (id_inmueble,))
        datos_inmueble = cursor_dict.fetchone()

        datos_vendedores = []
        for id_v in vendedores_seleccionados:
            cursor_dict.execute("SELECT nombre, apellido, dni, domicilio, estado_civil, nombre_conyuge, nupcias FROM personas WHERE id_persona = %s", (id_v,))
            datos_vendedores.append(cursor_dict.fetchone())

        datos_compradores = []
        for id_c in compradores_seleccionados:
            cursor_dict.execute("SELECT nombre, apellido, dni, domicilio, estado_civil, nombre_conyuge, nupcias FROM personas WHERE id_persona = %s", (id_c,))
            datos_compradores.append(cursor_dict.fetchone())

        fecha_hoy = date.today().strftime("%d/%m/%Y")
        
        cursor_dict.execute("SELECT * FROM perfil_escribano WHERE id=1")
        datos_escribano = cursor_dict.fetchone()

        # --- 3. LLAMADA AL PDF (La función sigue estando en la ventana principal por ahora) ---
        modulo_pdf.generar_pdf_minuta_oficial(
            id_minuta_generada, monto, fecha_hoy, observaciones, 
            datos_inmueble, datos_vendedores, datos_compradores, tipo_acto, datos_escribano
        )
        
        # --- 4. LIMPIEZA DE LA INTERFAZ ---
        ventana.txt_monto.clear()
        ventana.txt_observaciones.clear()
        ventana.list_vendedores.clearSelection()
        ventana.list_compradores.clearSelection()
        
    except mysql.connector.Error as error:
        print(f"Error en MySQL al guardar la minuta: {error}")
    finally:
        if conexion and conexion.is_connected():
            cursor.close()
            if 'cursor_dict' in locals():
                cursor_dict.close()
            conexion.close()