import os
import sys
import mysql.connector
from PyQt6 import uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QMainWindow, QApplication, QDialog


# --- NUEVA CLASE PARA LA VENTANA PH ---
class VentanaPH(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Cargamos el diseño de la ventanita
        ruta_script = os.path.dirname(__file__) 
        ruta_ui_ph = os.path.abspath(os.path.join(ruta_script, "..", "ui", "ventana_ph.ui"))
        uic.loadUi(ruta_ui_ph, self)
        
        # Diccionario para guardar los datos temporalmente
        self.datos_temporales = {
            "unidad": None,
            "poligono": None,
            "porcentaje": None
        }
        
        # Conectamos el botón aceptar
        self.btn_aceptar_ph.clicked.connect(self.guardar_y_cerrar)
        
    def guardar_y_cerrar(self):
        # Guardamos lo que escribió el escribano en nuestro diccionario
        self.datos_temporales["unidad"] = self.txt_ph_unidad.text().strip()
        self.datos_temporales["poligono"] = self.txt_ph_poligono.text().strip()
        self.datos_temporales["porcentaje"] = self.txt_ph_porcentaje.text().strip()
        
        # Cerramos la ventanita (vuelve a la principal)
        self.accept()
        
    def limpiar_campos(self):
        # Función para limpiar la ventanita después de guardar todo el inmueble
        self.txt_ph_unidad.clear()
        self.txt_ph_poligono.clear()
        self.txt_ph_porcentaje.clear()
        self.datos_temporales = {"unidad": None, "poligono": None, "porcentaje": None}
class MainWindow(QMainWindow):
    def guardar_perfil(self):
        nombre = self.txt_perfil_nombre.text().strip()
        matricula = self.txt_perfil_matricula.text().strip()
        registro = self.txt_perfil_registro.text().strip()
        
        try:
            conexion = mysql.connector.connect(host="localhost", user="root", password="admin123", database="proyecto_final_bd")
            cursor = conexion.cursor()
            
            # Actualizamos siempre la fila 1
            query = "UPDATE perfil_escribano SET nombre_completo=%s, matricula=%s, numero_registro=%s WHERE id=1"
            cursor.execute(query, (nombre, matricula, registro))
            conexion.commit()
            print("¡Perfil del escribano actualizado con éxito!")
            
        except mysql.connector.Error as error:
            print(f"Error al guardar el perfil: {error}")
        finally:
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close(); conexion.close()

    def cargar_perfil(self):
        try:
            conexion = mysql.connector.connect(host="localhost", user="root", password="admin123", database="proyecto_final_bd")
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT * FROM perfil_escribano WHERE id=1")
            perfil = cursor.fetchone()
            
            if perfil:
                self.txt_perfil_nombre.setText(perfil['nombre_completo'])
                self.txt_perfil_matricula.setText(perfil['matricula'])
                self.txt_perfil_registro.setText(perfil.get('numero_registro') or "")
                
        except mysql.connector.Error as error:
            print(f"Error al cargar el perfil: {error}")
        finally:
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close(); conexion.close()
    def __init__(self, datos_usuario):
        super().__init__()
        
        # Buscamos la ruta absoluta basada en donde está guardado este script
        ruta_script = os.path.dirname(__file__) 
        ruta_ui = os.path.abspath(os.path.join(ruta_script, "..", "ui", "menu.ui"))
        
        print("\n--- ¡ATENCIÓN! ESTOY LEYENDO ESTE ARCHIVO UI: ---")
        print(ruta_ui)
        print("------------------------------------------------\n")
        
        # Cargamos la interfaz usando la ruta absoluta segura
        uic.loadUi(ruta_ui, self)
        self.ventana_secundaria_ph = VentanaPH(self)
        self.usuario = datos_usuario
        self.configurar_interfaz()
        
        # Cargamos los datos de las minutas en las listas y combos al arrancar
        self.cargar_combos_minutas()
        
    def configurar_interfaz(self):
        # El saludo de bienvenida
        if hasattr(self, 'lbl_bienvenida'):
            self.lbl_bienvenida.setText(f"Bienvenido, {self.usuario['usuario']}")
            
        # --- NAVEGACIÓN POR ÍNDICES ---
        self.btn_home.clicked.connect(lambda: self.contenedor_paginas.setCurrentIndex(0))
        self.btn_clientes.clicked.connect(lambda: self.contenedor_paginas.setCurrentIndex(1))
        self.btn_inmuebles.clicked.connect(lambda: self.contenedor_paginas.setCurrentIndex(2))
        self.btn_minutas.clicked.connect(lambda: self.contenedor_paginas.setCurrentIndex(3))
        self.btn_configuracion.clicked.connect(lambda: self.contenedor_paginas.setCurrentIndex(4))

        
        # --- CONEXIONES DE BOTONES DE GUARDADO ---
        self.btn_guardar_cliente.clicked.connect(self.guardar_cliente)
        self.btn_guardar_inmueble.clicked.connect(self.guardar_inmueble)
        self.btn_guardar_minuta.clicked.connect(self.guardar_minuta)
        # --- NUEVO: Conectamos el botón para abrir la ventanita PH ---
        self.btn_datos_ph.clicked.connect(self.abrir_ventana_ph)
        # Conectar botón de guardado
        self.btn_guardar_perfil.clicked.connect(self.guardar_perfil)
        # Cargar los datos ni bien arranca la app
        self.cargar_perfil()
        # --- NUEVO: Conectamos el combo para habilitar/deshabilitar el botón PH ---
        self.cmb_tipo_propiedad.currentTextChanged.connect(self.alternar_boton_ph)
        # Lo llamamos una vez al inicio para que el botón arranque bloqueado si dice "Vertical"
        self.alternar_boton_ph(self.cmb_tipo_propiedad.currentText())
        # --- NUEVO: Conectamos el combo de estado civil ---
        self.cmb_estado_civil.currentTextChanged.connect(self.alternar_conyuge)
        self.alternar_conyuge(self.cmb_estado_civil.currentText()) # Estado inicial
        # --- Buscadores en tiempo real ---
        self.txt_buscar_vendedor.textChanged.connect(self.filtrar_vendedores)
        self.txt_buscar_comprador.textChanged.connect(self.filtrar_compradores)
        # Conexión del buscador de inmuebles (esto ya lo tenías)
        self.txt_buscar_inmueble.textChanged.connect(self.filtrar_inmuebles)

    def alternar_monto(self, texto):
        if "Donación" in texto:
            self.txt_monto.clear()
            self.txt_monto.setEnabled(False)
        else:
            self.txt_monto.setEnabled(True)
    def abrir_ventana_ph(self):
        # Usamos exec() para que sea modal (no deje clickear atrás hasta que se cierre)
        self.ventana_secundaria_ph.exec()
    # --- NUEVO: Función para prender/apagar el botón según el combo ---
    def alternar_boton_ph(self, texto):
        if "Horizontal" in texto:
            self.btn_datos_ph.setEnabled(True)
        else:
            self.btn_datos_ph.setEnabled(False)
    def cargar_combos_minutas(self):
        """Llena las listas de vendedores/compradores y el combo de inmueble desde la BD"""
        conexion = None
        try:
            conexion = mysql.connector.connect(
                host="localhost", user="root", password="admin123", database="proyecto_final_bd"
            )
            cursor = conexion.cursor()
            
            # 1. Poblar Listas de Personas (Vendedores y Compradores) usando los nombres del Designer
            cursor.execute("SELECT id_persona, nombre, apellido, dni FROM personas")
            personas = cursor.fetchall()
            
            self.list_vendedores.clear()
            self.list_compradores.clear()
            
            for p in personas:
                id_p, nom, ape, dni = p
                texto_mostrar = f"{ape}, {nom} (DNI: {dni})"
                
                # Agregamos a vendedores y guardamos el ID oculto
                self.list_vendedores.addItem(texto_mostrar)
                self.list_vendedores.item(self.list_vendedores.count() - 1).setData(32, id_p)
                
                # Agregamos a compradores y guardamos el ID oculto
                self.list_compradores.addItem(texto_mostrar)
                self.list_compradores.item(self.list_compradores.count() - 1).setData(32, id_p)
                
            # Habilitamos la selección múltiple en los QListWidget
            self.list_vendedores.setSelectionMode(self.list_vendedores.SelectionMode.MultiSelection)
            self.list_compradores.setSelectionMode(self.list_compradores.SelectionMode.MultiSelection)

           # 2. Poblar Combo de Inmuebles (CAMBIO: Ahora usa las 4 columnas nuevas)
            cursor.execute("""
             SELECT id_inmueble, 
                   nom_circunscripcion, nom_seccion, nom_manzana, nom_parcela, 
                   domicilio_inmueble 
                FROM inmuebles
                """)
            inmuebles = cursor.fetchall()
        
            self.cmb_inmueble.clear()
        
            for fila in inmuebles:
                id_inm = fila[0]
                circ = fila[1] or "-"
                sec = fila[2] or "-"
                manz = fila[3] or "-"
                parc = fila[4] or "-"
                dom = fila[5] or "S/D"
            
                texto_combo = f"Nom: C:{circ} S:{sec} Mz:{manz} P:{parc} | {dom}"
            
                self.cmb_inmueble.addItem(texto_combo, id_inm)
                
            print("🔄 Listas de Minutas sincronizadas con las tablas reales.")
        except mysql.connector.Error as error:
            print(f"Error al cargar datos de minutas: {error}")
        finally:
            if conexion and conexion.is_connected():
                cursor.close(); conexion.close()

    def guardar_minuta(self):
        monto = self.txt_monto.text().strip()
        observaciones = self.txt_observaciones.toPlainText().strip()
        id_inmueble = self.cmb_inmueble.currentData()
        tipo_acto = self.txt_especie_derechos.text().strip()
        id_usuario = 1  # ID por defecto para el escribano

        # Recuperamos las IDs de las personas
        vendedores_seleccionados = [
            self.list_vendedores.item(i).data(32)
            for i in range(self.list_vendedores.count())
            if self.list_vendedores.item(i).isSelected()
        ]
        compradores_seleccionados = [
            self.list_compradores.item(i).data(32)
            for i in range(self.list_compradores.count())
            if self.list_compradores.item(i).isSelected()
        ]

        # --- VALIDACIONES ---
        # 1. Inmueble e Intervinientes (Obligatorio siempre)
        if not id_inmueble or not vendedores_seleccionados or not compradores_seleccionados:
            print("Error: Falta completar inmueble o intervinientes.")
            return

        # 2. Asignación automática: si es donación y está vacío, le mandamos "NO CORRESPONDE" a la BD
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
            # Usamos un cursor de diccionario para facilitar el paso de datos al PDF
            cursor_dict = conexion.cursor(dictionary=True)
            
           # Traer los datos completos del inmueble
            cursor_dict.execute("""
            SELECT domicilio_inmueble as domicilio,
                   entre_calles,
                   lote,
                   manzana,
                   superficie,
                   tipo_propiedad,
                   ph_unidad_funcional as ph_unidad,
                   ph_poligono,
                   ph_porcentaje,
                   tomo_numero,
                   folio_real,
                   anio_inscripcion,
                   nom_circunscripcion,
                   nom_seccion,
                   nom_manzana,
                   nom_parcela
            FROM inmuebles WHERE id_inmueble = %s
        """, (id_inmueble,))
            datos_inmueble = cursor_dict.fetchone()

            # Traer los datos completos de los vendedores
            # Traer los datos completos de los vendedores (AGREGAMOS ESTADO CIVIL Y CÓNYUGE)
            datos_vendedores = []
            for id_v in vendedores_seleccionados:
                cursor_dict.execute("SELECT nombre, apellido, dni, domicilio, estado_civil, nombre_conyuge FROM personas WHERE id_persona = %s", (id_v,))
                datos_vendedores.append(cursor_dict.fetchone())

            # Traer los datos completos de los compradores (AGREGAMOS ESTADO CIVIL Y CÓNYUGE)
            datos_compradores = []
            for id_c in compradores_seleccionados:
                cursor_dict.execute("SELECT nombre, apellido, dni, domicilio, estado_civil, nombre_conyuge FROM personas WHERE id_persona = %s", (id_c,))
                datos_compradores.append(cursor_dict.fetchone())

            # --- 3. GENERACIÓN AUTOMÁTICA DEL PDF ---
            from datetime import date
            fecha_hoy = date.today().strftime("%d/%m/%Y")
            
            # --- NUEVO: Traer datos del escribano ---
            cursor_dict.execute("SELECT * FROM perfil_escribano WHERE id=1")
            datos_escribano = cursor_dict.fetchone()

            # Llamamos a la nueva función oficial (AGREGAMOS datos_escribano AL FINAL)
            self.generar_pdf_minuta_oficial(
                id_minuta_generada, monto, fecha_hoy, observaciones, 
                datos_inmueble, datos_vendedores, datos_compradores, tipo_acto, datos_escribano
            )
            
            # --- 4. LIMPIEZA DE LA INTERFAZ ---
            self.txt_monto.clear()
            self.txt_observaciones.clear()
            self.list_vendedores.clearSelection()
            self.list_compradores.clearSelection()
            
        except mysql.connector.Error as error:
            print(f"Error en MySQL al guardar la minuta: {error}")
        finally:
            if conexion and conexion.is_connected():
                cursor.close()
                if 'cursor_dict' in locals():
                    cursor_dict.close()
                conexion.close()
    def generar_pdf_minuta_oficial(self, id_minuta, monto, fecha_impresion, observaciones, inmueble, vendedores, compradores, tipo_acto, datos_escribano):
        """Genera el PDF emulando los casilleros de la Minuta C real de La Rioja"""
    
        try:
            from reportlab.lib.pagesizes import legal
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib import colors
            import os

            os.makedirs("pdf_minutas", exist_ok=True)
            nombre_archivo = f"pdf_minutas/minuta_c_{id_minuta}.pdf"

            doc = SimpleDocTemplate(nombre_archivo, pagesize=legal, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
            story = []
            styles = getSampleStyleSheet()
            
            st_titulo = ParagraphStyle('Titulo', parent=styles['Heading2'], fontSize=12, alignment=1, spaceAfter=10)
            st_box_title = ParagraphStyle('BoxTitle', fontSize=8, fontName='Helvetica-Bold', textColor=colors.black)
            st_box_text = ParagraphStyle('BoxText', fontSize=9, fontName='Helvetica', leading=12)

           # --- Lógica del Monto ---
            # Si el escribano lo dejó vacío o el sistema le asignó "0", ponemos "NO CORRESPONDE"
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
            
            # Armamos el texto de ubicación concatenando los datos que existan
            texto_ubicacion = f"{domicilio_inm}"
            if entre_c:
                texto_ubicacion += f" (entre {entre_c})"
            if manz_inm:
                texto_ubicacion += f" - Mz: {manz_inm}"
            if lote_inm:
                texto_ubicacion += f" - Lote: {lote_inm}"

            # Si también querés sumar Localidad y Departamento que tenés en la interfaz:
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
                conyuge_c = comp.get('nombre_conyuge')
                texto_conyuge_c = f" - <b>Cónyuge:</b> {conyuge_c}" if conyuge_c else ""
                
                texto_comp = f"<b>Nombre y Apellido:</b> {comp.get('nombre')} {comp.get('apellido')} - <b>DNI:</b> {comp.get('dni')}<br/><b>Estado Civil:</b> {est_civil_c}{texto_conyuge_c}<br/><b>Domicilio:</b> {dom_c}"
                t_comp = Table([[Paragraph(texto_comp, st_box_text)]], colWidths=[540])
                t_comp.setStyle(estilo_grilla)
                story.append(t_comp)
            story.append(Spacer(1, 5))

            # --- 7. TRANSMITENTES (VENDEDORES) ---
            story.append(Paragraph("<b>7 - TRANSMITENTE (Causante - Cedente / Vendedores)</b>", st_box_title))
            for vend in vendedores:
                dom_v = vend.get('domicilio') or 'S/D'
                est_civil_v = vend.get('estado_civil') or 'S/D'
                conyuge_v = vend.get('nombre_conyuge')
                texto_conyuge_v = f" - <b>Cónyuge:</b> {conyuge_v}" if conyuge_v else ""
                
                texto_vend = f"<b>Nombre y Apellido:</b> {vend.get('nombre')} {vend.get('apellido')} - <b>DNI:</b> {vend.get('dni')}<br/><b>Estado Civil:</b> {est_civil_v}{texto_conyuge_v}<br/><b>Domicilio:</b> {dom_v}"
                t_vend = Table([[Paragraph(texto_vend, st_box_text)]], colWidths=[540])
                t_vend.setStyle(estilo_grilla)
                story.append(t_vend)
            story.append(Spacer(1, 5))

           # --- Datos del Escribano ---
            nombre_escribano = datos_escribano.get('nombre_completo') or "S/D"
            matricula_esc = datos_escribano.get('matricula') or "S/D"
            registro_esc = datos_escribano.get('numero_registro')
            
            texto_registro = f" - Registro N° {registro_esc}" if registro_esc else ""

            # --- 8 AL 14. OTORGAMIENTO Y OBSERVACIONES ---
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
                [Paragraph(f"__________________________<br/><b>{nombre_escribano}</b><br/>Mat. {matricula_esc}<br/>FIRMA Y SELLO ESCRIBANO", ParagraphStyle('C', alignment=1, fontSize=8)), 
                 Paragraph("__________________________<br/>FIRMA Y SELLO DEL REGISTRADOR", ParagraphStyle('C', alignment=1, fontSize=8))]
            ]
            t_firmas = Table(datos_firmas, colWidths=[270, 270])
            story.append(t_firmas)

            doc.build(story)
            print(f"📄 ¡PDF Oficial Minuta C generado con éxito!")
            os.startfile(os.path.abspath(nombre_archivo))

        except Exception as e:
            print(f"Error al generar el documento PDF oficial: {e}")
            doc.build(story)
            print(f"📄 ¡PDF Oficial Minuta C generado con éxito!")
            os.startfile(os.path.abspath(nombre_archivo))
    # --- TABLA CLIENTES ---
    def guardar_cliente(self):
        nombre = self.txt_nombre.text().strip()
        apellido = self.txt_apellido.text().strip()
        dni = self.txt_dni.text().strip()
        domicilio = self.txt_domicilio.text().strip()
        
        # --- NUEVO: Capturamos el estado civil y el cónyuge ---
        estado_civil = self.cmb_estado_civil.currentText().strip()
        # Solo guardamos el cónyuge si el campo está habilitado (es decir, si está casado)
        conyuge = self.txt_nombre_conyuge.text().strip() if self.txt_nombre_conyuge.isEnabled() else None
        
        if not nombre or not apellido or not dni:
            print("Error: Nombre, Apellido y DNI son obligatorios.")
            return

        conexion = None
        try:
            conexion = mysql.connector.connect(host="localhost", user="root", password="admin123", database="proyecto_final_bd")
            cursor = conexion.cursor()
            
            # --- NUEVO: Query actualizada con las nuevas columnas ---
            query = """INSERT INTO inmuebles 
           (partida_inmobiliaria, domicilio_inmueble, entre_calles, lote, manzana, superficie, tipo_propiedad, 
            nom_circunscripcion, nom_seccion, nom_manzana, nom_parcela) 
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            valores = (nombre, apellido, dni, domicilio, estado_civil, conyuge)
            
            cursor.execute(query, valores)
            conexion.commit()
            print(f"¡Cliente {nombre} {apellido} guardado con éxito!")
            
            # Limpiamos los campos
            self.txt_nombre.clear()
            self.txt_apellido.clear()
            self.txt_dni.clear()
            self.txt_domicilio.clear()
            self.cmb_estado_civil.setCurrentIndex(0) # Vuelve a Soltero/a
            
        except mysql.connector.Error as error:
            print(f"Error al guardar cliente: {error}")
        finally:
            if conexion and conexion.is_connected():
                cursor.close(); conexion.close()
   # --- TABLA INMUEBLES ---
    def guardar_inmueble(self):
        partida = self.txt_partida.text().strip()
        n_circ = self.txt_nom_circunscripcion.text().strip()
        n_sec = self.txt_nom_seccion.text().strip()
        n_manz = self.txt_nom_manzana.text().strip()
        n_parc = self.txt_nom_parcela.text().strip()
        domicilio = self.txt_domicilio_inm.text().strip()
        superficie = self.txt_superficie_inm.text().strip()
        depto = self.txt_depto.text().strip()
        localidad = self.txt_localidad_inm.text().strip()
        registro = self.txt_registro.text().strip()
        folio_real = self.txt_folio_real.text().strip()
        tomo_numero = self.txt_tomo_numero.text().strip()
        anio = self.txt_anio.text().strip()
        
        
        # --- NUEVO: Capturar datos de PH ---
        tipo_prop = self.cmb_tipo_propiedad.currentText().strip()
        
        # Si es PH, traemos los datos de la ventanita. Si no, mandamos vacío (None)
        if "Horizontal" in tipo_prop:
            ph_unidad = self.ventana_secundaria_ph.datos_temporales["unidad"]
            ph_polig = self.ventana_secundaria_ph.datos_temporales["poligono"]
            ph_porcent = self.ventana_secundaria_ph.datos_temporales["porcentaje"]
        else:
            ph_unidad = None
            ph_polig = None
            ph_porcent = None
        
        if not partida: 
            print("Error: La partida inmobiliaria es obligatoria.")
            return
        
        domicilio = domicilio if domicilio else None
        superficie = superficie if superficie else None
        depto = depto if depto else None
        localidad = localidad if localidad else None
        registro = registro if registro else None
        folio_real = folio_real if folio_real else None
        tomo_numero = tomo_numero if tomo_numero else None
        anio = anio if anio else None
        entre_calles = self.txt_inmueble_entre_calles.text().strip()
        lote = self.txt_inmueble_lote.text().strip()
        manzana = self.txt_inmueble_manzana.text().strip()

        conexion = None
        try:
            conexion = mysql.connector.connect(host="localhost", user="root", password="admin123", database="proyecto_final_bd")
            cursor = conexion.cursor()
            
            # --- NUEVO: Query actualizada con TODAS las columnas (20 en total) ---
            query = """INSERT INTO inmuebles 
                   (partida_inmobiliaria, nom_circunscripcion, nom_seccion, nom_manzana, nom_parcela, 
                    domicilio_inmueble, entre_calles, lote, manzana, superficie, 
                    departamento, localidad, registro_propiedad, folio_real, tomo_numero, anio_inscripcion,
                    tipo_propiedad, ph_unidad_funcional, ph_poligono, ph_porcentaje) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            
            # Asegurate de que el orden acá sea EXACTAMENTE igual al de arriba
            valores = (partida, n_circ, n_sec, n_manz, n_parc, 
                       domicilio, entre_calles, lote, manzana, superficie, 
                       depto, localidad, registro, folio_real, tomo_numero, anio,
                       tipo_prop, ph_unidad, ph_polig, ph_porcent)
            
            cursor.execute(query, valores)
            conexion.commit()    
            texto_exito = domicilio if domicilio else f"con Partida {partida}"
            print(f"¡Inmueble ({tipo_prop}) {texto_exito} registrado con éxito!")
            
            # Limpieza general
            self.txt_partida.clear(); self.txt_domicilio_inm.clear(); self.txt_superficie_inm.clear()
            self.txt_depto.clear(); self.txt_localidad_inm.clear(); self.txt_registro.clear(); self.txt_folio_real.clear()
            self.txt_tomo_numero.clear(); self.txt_anio.clear()
            
            # --- NUEVO: Limpiar la ventanita PH para el próximo inmueble ---
            self.ventana_secundaria_ph.limpiar_campos()
            
        except mysql.connector.Error as error: 
            print(error)
        finally:
            if conexion and conexion.is_connected(): cursor.close(); conexion.close()
    # --- NUEVO: Función para prender/apagar el campo del cónyuge ---
    def alternar_conyuge(self, texto):
        if "Casado" in texto:
            self.txt_nombre_conyuge.setEnabled(True)
        else:
            self.txt_nombre_conyuge.clear() # Limpiamos por si había escrito algo
            self.txt_nombre_conyuge.setEnabled(False)
    def filtrar_vendedores(self, texto):
        """Oculta los vendedores que no coinciden con la búsqueda."""
        for i in range(self.list_vendedores.count()):
            item = self.list_vendedores.item(i)
            # Comparamos todo en minúsculas para que no haya problemas con las mayúsculas
            if texto.lower() in item.text().lower():
                item.setHidden(False)
           pip else:
                item.setHidden(True)

    def filtrar_compradores(self, texto):
        """Oculta los compradores que no coinciden con la búsqueda."""
        for i in range(self.list_compradores.count()):
            item = self.list_compradores.item(i)
            if texto.lower() in item.text().lower():
                item.setHidden(False)
            else:
                item.setHidden(True)
    def filtrar_inmuebles(self, texto):
        """Filtra los inmuebles recargando el ComboBox desde un respaldo en memoria."""
        
        # 1. Hacemos una copia de seguridad la primera vez que se escribe algo
        if not hasattr(self, 'respaldo_inmuebles') or len(self.respaldo_inmuebles) == 0:
            if self.cmb_inmueble.count() > 0:
                self.respaldo_inmuebles = []
                for i in range(self.cmb_inmueble.count()):
                    self.respaldo_inmuebles.append({
                        "texto": self.cmb_inmueble.itemText(i),
                        "data": self.cmb_inmueble.itemData(i)
                    })
            else:
                return # Si todavía no cargaron los inmuebles, no hacemos nada
                
        # 2. Limpiamos el Desplegable visualmente
        self.cmb_inmueble.clear()
        
        # 3. Lo volvemos a rellenar solo con los que coinciden con el texto
        for inm in self.respaldo_inmuebles:
            if texto.lower() in inm["texto"].lower():
                self.cmb_inmueble.addItem(inm["texto"], inm["data"])
if __name__ == "__main__":
    app = QApplication(sys.argv)
    user_test = {'usuario': 'facundo_rojo', 'rol': 'Escribano'}
    ventana = MainWindow(user_test)
    ventana.show()
    sys.exit(app.exec())