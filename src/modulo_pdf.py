import os
from reportlab.lib.pagesizes import legal
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generar_pdf_minuta_oficial(id_minuta, monto, fecha_impresion, observaciones, inmueble, vendedores, compradores, tipo_acto, datos_escribano):
    """Genera el PDF emulando los casilleros de la Minuta C real de La Rioja"""
    try:
        os.makedirs("pdf_minutas", exist_ok=True)
        nombre_archivo = f"pdf_minutas/minuta_c_{id_minuta}.pdf"

        doc = SimpleDocTemplate(nombre_archivo, pagesize=legal, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
        story = []
        styles = getSampleStyleSheet()
        
        st_titulo = ParagraphStyle('Titulo', parent=styles['Heading2'], fontSize=12, alignment=1, spaceAfter=10)
        st_box_title = ParagraphStyle('BoxTitle', fontSize=8, fontName='Helvetica-Bold', textColor=colors.black)
        st_box_text = ParagraphStyle('BoxText', fontSize=9, fontName='Helvetica', leading=12)

        if monto == "0" or not monto:
            texto_monto_pdf = "NO CORRESPONDE"
        else:
            texto_monto_pdf = f"${monto}"

        # --- ENCABEZADO ---
        story.append(Paragraph("<b>DIRECCIÓN GENERAL DE REGISTRO DE LA PROPIEDAD INMUEBLE</b><br/>La Rioja - República Argentina", st_titulo))
        story.append(Paragraph(f"<b>Minuta 'C' N° {id_minuta}</b> - Solicitud de Inscripción de dominio o anotaciones", ParagraphStyle('Sub', alignment=1, fontSize=10)))
        story.append(Spacer(1, 10))

        estilo_grilla = TableStyle([
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('PADDING', (0,0), (-1,-1), 4),
        ])

        # --- 1. NOMENCLATURA Y 2. ACTO ---
        n_circ = inmueble.get('nom_circunscripcion') or '-'
        n_sec = inmueble.get('nom_seccion') or '-'
        n_manz = inmueble.get('nom_manzana') or '-'
        n_parc = inmueble.get('nom_parcela') or '-'
        
        texto_nomenclatura = f"Circunscripción: {n_circ} &nbsp;&nbsp;|&nbsp;&nbsp; Sección: {n_sec}<br/>Manzana: {n_manz} &nbsp;&nbsp;|&nbsp;&nbsp; Parcela: {n_parc}"
        
        datos_sec_1_2 = [
            [Paragraph("<b>1 - Nomenclatura Catastral</b>", st_box_title), Paragraph("<b>2 - ESPECIE DE LOS DERECHOS O ACTOS</b>", st_box_title)],
            [Paragraph(texto_nomenclatura, st_box_text), Paragraph(f"{tipo_acto.upper()}<br/>Monto: {texto_monto_pdf}", st_box_text)]
        ]
        t1 = Table(datos_sec_1_2, colWidths=[270, 270])
        t1.setStyle(estilo_grilla)
        story.append(t1)
        story.append(Spacer(1, 5))

        # --- 3. INMUEBLE Y 4. PH ---
        domicilio_inm = inmueble.get('domicilio') or 'S/D'
        entre_c = inmueble.get('entre_calles')
        lote_inm = inmueble.get('lote')
        manz_inm = inmueble.get('manzana')
        
        texto_ubicacion = f"{domicilio_inm}"
        if entre_c: texto_ubicacion += f" (entre {entre_c})"
        if manz_inm: texto_ubicacion += f" - Mz: {manz_inm}"
        if lote_inm: texto_ubicacion += f" - Lote: {lote_inm}"

        localidad = inmueble.get('localidad')
        dpto = inmueble.get('departamento')
        if localidad and dpto:
            texto_ubicacion += f"<br/>Localidad: {localidad} - Dpto: {dpto}"

        superficie_inm = inmueble.get('superficie') or 'S/D'
        
        tipo_prop = inmueble.get('tipo_propiedad') or ''
        if "horizontal" in tipo_prop.lower():
            uni = inmueble.get('ph_unidad') or 'S/D'
            pol = inmueble.get('ph_poligono') or 'S/D'
            porc = inmueble.get('ph_porcentaje') or '0'
            texto_ph = f"Unidad Funcional: {uni}<br/>Polígono: {pol}<br/>Porcentaje: {porc}%"
        else:
            texto_ph = "NO CORRESPONDE"

        datos_sec_3_4 = [
            [Paragraph("<b>3 - INMUEBLE: Ubicación y Superficie</b>", st_box_title), Paragraph("<b>4 - PROPIEDAD HORIZONTAL</b>", st_box_title)],
            [Paragraph(f"Ubicación: {texto_ubicacion}<br/>Superficie: {superficie_inm}", st_box_text), Paragraph(texto_ph, st_box_text)]
        ]
        t2 = Table(datos_sec_3_4, colWidths=[270, 270])
        t2.setStyle(estilo_grilla)
        story.append(t2)
        story.append(Spacer(1, 5))

        # --- 5. ANTECEDENTES ---
        tomo_num = inmueble.get('tomo_numero') or 'S/D'
        folio_r = inmueble.get('folio_real') or 'S/D'
        anio_insc = inmueble.get('anio_inscripcion') or 'S/D'
        
        datos_sec_5 = [
            [Paragraph("<b>5 - Antecedentes de Dominio, Hipoteca y otros derechos</b>", st_box_title)],
            [Paragraph(f"Tomo y Número: {tomo_num} &nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp; Folio Real: {folio_r} &nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp; Año: {anio_insc}", st_box_text)]
        ]
        t3 = Table(datos_sec_5, colWidths=[540])
        t3.setStyle(estilo_grilla)
        story.append(t3)
        story.append(Spacer(1, 5))

        # --- 6. ADQUIRENTES (COMPRADORES) ---
        story.append(Paragraph("<b>6 - ADQUIRENTES (Beneficiarios / Compradores)</b>", st_box_title))
        for comp in compradores:
            dom_c = comp.get('domicilio') or 'S/D'
            est_civil_c = comp.get('estado_civil') or 'S/D'
            nupcias_c = comp.get('nupcias')
            if nupcias_c and nupcias_c != "-":
                texto_estado_civil_c = f"{est_civil_c} en {nupcias_c} nupcias"
            else:
                texto_estado_civil_c = est_civil_c
                
            conyuge_c = comp.get('nombre_conyuge')
            texto_conyuge_c = f" - <b>Cónyuge:</b> {conyuge_c}" if conyuge_c else ""
            
            texto_comp = f"<b>Nombre y Apellido:</b> {comp.get('nombre')} {comp.get('apellido')} - <b>DNI:</b> {comp.get('dni')}<br/><b>Estado Civil:</b> {texto_estado_civil_c}{texto_conyuge_c}<br/><b>Domicilio:</b> {dom_c}"
            t_comp = Table([[Paragraph(texto_comp, st_box_text)]], colWidths=[540])
            t_comp.setStyle(estilo_grilla)
            story.append(t_comp)
        story.append(Spacer(1, 5))

        # --- 7. TRANSMITENTES (VENDEDORES) ---
        story.append(Paragraph("<b>7 - TRANSMITENTE (Causante - Cedente / Vendedores)</b>", st_box_title))
        for vend in vendedores:
            dom_v = vend.get('domicilio') or 'S/D'
            est_civil_v = vend.get('estado_civil') or 'S/D'
            nupcias_v = vend.get('nupcias')
            if nupcias_v and nupcias_v != "-":
                texto_estado_civil_v = f"{est_civil_v} en {nupcias_v} nupcias"
            else:
                texto_estado_civil_v = est_civil_v
                
            conyuge_v = vend.get('nombre_conyuge')
            texto_conyuge_v = f" - <b>Cónyuge:</b> {conyuge_v}" if conyuge_v else ""
            
            texto_vend = f"<b>Nombre y Apellido:</b> {vend.get('nombre')} {vend.get('apellido')} - <b>DNI:</b> {vend.get('dni')}<br/><b>Estado Civil:</b> {texto_estado_civil_v}{texto_conyuge_v}<br/><b>Domicilio:</b> {dom_v}"
            t_vend = Table([[Paragraph(texto_vend, st_box_text)]], colWidths=[540])
            t_vend.setStyle(estilo_grilla)
            story.append(t_vend)
        story.append(Spacer(1, 5))

        # --- 8 AL 14. OTORGAMIENTO Y OBSERVACIONES ---
        nombre_escribano = datos_escribano.get('nombre_completo') or "S/D"
        matricula_esc = datos_escribano.get('matricula') or "S/D"
        registro_esc = datos_escribano.get('numero_registro')
        
        texto_registro = f" - Registro N° {registro_esc}" if registro_esc else ""

        datos_finales = [
            [Paragraph("<b>8 - MONTO / 10 - OTORGAMIENTO</b>", st_box_title), Paragraph("<b>OBSERVACIONES ADICIONALES</b>", st_box_title)],
            [Paragraph(f"Precio o Valuación: {texto_monto_pdf}<br/>Fecha de Emisión: {fecha_impresion}<br/>Escribano Autorizante: {nombre_escribano} - Mat. {matricula_esc}{texto_registro}", st_box_text), 
             Paragraph(observaciones if observaciones else "Sin observaciones.", st_box_text)]
        ]
        t_final = Table(datos_finales, colWidths=[270, 270])
        t_final.setStyle(estilo_grilla)
        story.append(t_final)
        story.append(Spacer(1, 30))

        # --- FIRMAS ---
        datos_firmas = [
            ["", ""], 
            [Paragraph(f"__________________________<br/><b>{nombre_escribano}</b><br/>Mat. {matricula_esc}<br/>FIRMA Y SELLO ESCRIBANO", ParagraphStyle('C', alignment=1, fontSize=8)),]
        ]
        t_firmas = Table(datos_firmas, colWidths=[270, 270])
        story.append(t_firmas)

        doc.build(story)
        print(f"📄 ¡PDF Oficial Minuta C generado con éxito!")
        os.startfile(os.path.abspath(nombre_archivo))

    except Exception as e:
        print(f"Error al generar el documento PDF oficial: {e}")