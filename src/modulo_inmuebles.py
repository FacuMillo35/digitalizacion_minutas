import mysql.connector

def guardar_inmueble(ventana):
    partida = ventana.txt_partida.text().strip()
    n_circ = ventana.txt_nom_circunscripcion.text().strip()
    n_sec = ventana.txt_nom_seccion.text().strip()
    n_manz = ventana.txt_nom_manzana.text().strip()
    n_parc = ventana.txt_nom_parcela.text().strip()
    domicilio = ventana.txt_domicilio_inm.text().strip()
    superficie = ventana.txt_superficie_inm.text().strip()
    depto = ventana.txt_depto.text().strip()
    localidad = ventana.txt_localidad_inm.text().strip()
    registro = ventana.txt_registro.text().strip()
    folio_real = ventana.txt_folio_real.text().strip()
    tomo_numero = ventana.txt_tomo_numero.text().strip()
    anio = ventana.txt_anio.text().strip()
    
    entre_calles = ventana.txt_inmueble_entre_calles.text().strip()
    lote = ventana.txt_inmueble_lote.text().strip()
    manzana = ventana.txt_inmueble_manzana.text().strip()
    
    tipo_prop = ventana.cmb_tipo_propiedad.currentText().strip()
    
    # Datos de PH
    if "Horizontal" in tipo_prop:
        ph_unidad = ventana.ventana_secundaria_ph.datos_temporales.get("unidad")
        ph_polig = ventana.ventana_secundaria_ph.datos_temporales.get("poligono")
        ph_porcent = ventana.ventana_secundaria_ph.datos_temporales.get("porcentaje")
    else:
        ph_unidad = None
        ph_polig = None
        ph_porcent = None
    
    if not partida: 
        print("Error: La partida inmobiliaria es obligatoria.")
        return
    
    # Limpieza de nulos
    domicilio = domicilio if domicilio else None
    superficie = superficie if superficie else None
    depto = depto if depto else None
    localidad = localidad if localidad else None
    registro = registro if registro else None
    folio_real = folio_real if folio_real else None
    tomo_numero = tomo_numero if tomo_numero else None
    anio = anio if anio else None

    conexion = None
    try:
        conexion = mysql.connector.connect(host="localhost", user="root", password="admin123", database="proyecto_final_bd")
        cursor = conexion.cursor()
        
        query = """INSERT INTO inmuebles 
               (partida_inmobiliaria, nom_circunscripcion, nom_seccion, nom_manzana, nom_parcela, 
                domicilio_inmueble, entre_calles, lote, manzana, superficie, 
                departamento, localidad, registro_propiedad, folio_real, tomo_numero, anio_inscripcion,
                tipo_propiedad, ph_unidad_funcional, ph_poligono, ph_porcentaje) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        
        valores = (partida, n_circ, n_sec, n_manz, n_parc, 
                   domicilio, entre_calles, lote, manzana, superficie, 
                   depto, localidad, registro, folio_real, tomo_numero, anio,
                   tipo_prop, ph_unidad, ph_polig, ph_porcent)
        
        cursor.execute(query, valores)
        conexion.commit()
        
        texto_exito = domicilio if domicilio else f"con Partida {partida}"
        print(f"¡Inmueble ({tipo_prop}) {texto_exito} registrado con éxito!")
        
        # Limpieza general
        ventana.txt_partida.clear(); ventana.txt_domicilio_inm.clear(); ventana.txt_superficie_inm.clear()
        ventana.txt_depto.clear(); ventana.txt_localidad_inm.clear(); ventana.txt_registro.clear(); ventana.txt_folio_real.clear()
        ventana.txt_tomo_numero.clear(); ventana.txt_anio.clear()
        ventana.txt_inmueble_entre_calles.clear(); ventana.txt_inmueble_lote.clear(); ventana.txt_inmueble_manzana.clear()
        ventana.txt_nom_circunscripcion.clear(); ventana.txt_nom_seccion.clear(); ventana.txt_nom_manzana.clear(); ventana.txt_nom_parcela.clear()
        
        if hasattr(ventana, 'ventana_secundaria_ph'):
            ventana.ventana_secundaria_ph.limpiar_campos()
        
    except mysql.connector.Error as error: 
        print(f"Error al guardar inmueble: {error}")
    finally:
        if conexion and conexion.is_connected(): 
            cursor.close()
            conexion.close()