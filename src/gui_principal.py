import os
import sys
import mysql.connector
from PyQt6 import uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QMainWindow, QApplication

class MainWindow(QMainWindow):
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
        
        # --- CONEXIONES DE BOTONES DE GUARDADO ---
        self.btn_guardar_cliente.clicked.connect(self.guardar_cliente)
        self.btn_guardar_inmueble.clicked.connect(self.guardar_inmueble)
        self.btn_guardar_minuta.clicked.connect(self.guardar_minuta)
        
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

            # 2. Poblar Combo de Inmuebles
            cursor.execute("SELECT id_inmueble, partida_inmobiliaria, domicilio_inmueble FROM inmuebles")
            inmuebles = cursor.fetchall()
            
            self.cmb_inmueble.clear()
            for inm in inmuebles:
                id_i, partida, dom = inm
                self.cmb_inmueble.addItem(f"Partida: {partida} - {dom}", id_i)
                
            print("🔄 Listas de Minutas sincronizadas con las tablas reales.")
        except mysql.connector.Error as error:
            print(f"Error al cargar datos de minutas: {error}")
        finally:
            if conexion and conexion.is_connected():
                cursor.close(); conexion.close()

    def guardar_minuta(self):
        # 1. Capturamos los campos desde la interfaz gráfica
        tipo_tramite = self.txt_tipo_tramite.text().strip()  
        monto = self.txt_monto.text().strip()
        fecha_registro = self.txt_fecha_minuta.date().toString("yyyy-MM-dd") 
        observaciones = self.txt_observaciones.toPlainText().strip() # Cambiado a toPlainText() por usar QTextEdit
        id_inmueble = self.cmb_inmueble.currentData()
        id_usuario = 1  # ID por defecto para el escribano

        # Recuperamos las IDs de las personas seleccionadas en los QListWidget
        vendedores_seleccionados = [self.list_vendedores.item(i).data(32) for i in range(self.list_vendedores.count()) if self.list_vendedores.item(i).isSelected()]
        compradores_seleccionados = [self.list_compradores.item(i).data(32) for i in range(self.list_compradores.count()) if self.list_compradores.item(i).isSelected()]

        # Validación de campos obligatorios
        if not tipo_tramite or not monto or not id_inmueble or not vendedores_seleccionados or not compradores_seleccionados:
            print("Error: Falta completar datos o seleccionar intervinientes (Vendedor/Comprador).")
            return

        conexion = None
        try:
            conexion = mysql.connector.connect(
                host="localhost", user="root", password="admin123", database="proyecto_final_bd"
            )
            cursor = conexion.cursor()
            
            # Ajustamos el monto para guardarlo de manera clara en la columna 'motivo'
            texto_motivo = f"Monto de Operacion: ${monto}"
            
            # A) Insertamos usando estrictamente las columnas reales de tu Workbench
            query_minuta = """
                INSERT INTO minuta_c_inmueble 
                (fecha, id_inmueble, id_usuario_escribano, id_usuario, tipo_tramite, motivo, observaciones) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            valores_minuta = (fecha_registro, id_inmueble, id_usuario, id_usuario, tipo_tramite, texto_motivo, observaciones)
            cursor.execute(query_minuta, valores_minuta)
            
            # Recuperamos el ID generado
            id_minuta_generada = cursor.lastrowid
            
            # B) Insertamos en la tabla intermedia: 'intervinientes_minuta'
            query_intermedia = """
                INSERT INTO intervinientes_minuta (id_minuta, id_persona, rol) 
                VALUES (%s, %s, %s)
            """
            
            # Guardamos los vendedores
            for id_vendedor in vendedores_seleccionados:
                cursor.execute(query_intermedia, (id_minuta_generada, id_vendedor, 'Vendedor'))
                
            # Guardamos los compradores
            for id_comprador in compradores_seleccionados:
                cursor.execute(query_intermedia, (id_minuta_generada, id_comprador, 'Comprador'))
                
            conexion.commit()
            print(f"¡Excelente! Minuta N° {id_minuta_generada} ({tipo_tramite}) registrada con éxito en el sistema.")
            
            # --- GENERACIÓN AUTOMÁTICA DEL PDF ---
            texto_inmueble = self.cmb_inmueble.currentText()
            nombres_vendedores = [self.list_vendedores.item(i).text() for i in range(self.list_vendedores.count()) if self.list_vendedores.item(i).isSelected()]
            nombres_compradores = [self.list_compradores.item(i).text() for i in range(self.list_compradores.count()) if self.list_compradores.item(i).isSelected()]
            
            self.generar_pdf_minuta(
                id_minuta_generada, tipo_tramite, monto, fecha_registro, 
                observaciones, texto_inmueble, nombres_vendedores, nombres_compradores
            )
            
            # Limpiamos los campos de la interfaz
            self.txt_tipo_tramite.clear()
            self.txt_monto.clear()
            self.txt_observaciones.clear()
            self.list_vendedores.clearSelection()
            self.list_compradores.clearSelection()
            self.txt_fecha_inmueble.setDate(QDate.currentDate())
            
        except mysql.connector.Error as error:
            print(f"Error en MySQL al guardar la minuta: {error}")
        finally:
            if conexion and conexion.is_connected():
                cursor.close(); conexion.close()

    def generar_pdf_minuta(self, id_minuta, tipo_tramite, monto, fecha, observaciones, inmueble_texto, vendedores, compradores):
        """Genera un archivo PDF estructurado de la minuta para impresión notarial"""
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib import colors

            os.makedirs("pdf_minutas", exist_ok=True)
            nombre_archivo = f"pdf_minutas/minuta_{id_minuta}.pdf"

            doc = SimpleDocTemplate(nombre_archivo, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
            story = []

            styles = getSampleStyleSheet()
            style_titulo = ParagraphStyle('TituloStyle', parent=styles['Heading1'], fontSize=16, leading=20, alignment=1, spaceAfter=15, textColor=colors.HexColor("#1A365D"))
            style_sub = ParagraphStyle('SubStyle', parent=styles['Heading2'], fontSize=11, leading=15, spaceBefore=8, spaceAfter=4, textColor=colors.HexColor("#2B6CB0"))
            style_texto = ParagraphStyle('TextoStyle', parent=styles['Normal'], fontSize=10, leading=14)

            story.append(Paragraph("REGISTRO GENERAL DE LA PROPIEDAD INMUEBLE", style_titulo))
            story.append(Paragraph("<b>PROVINCIA DE LA RIOJA</b> - SOLICITUD DE INSCRIPCIÓN (MINUTA C)", ParagraphStyle('Center', parent=style_texto, alignment=1)))
            story.append(Spacer(1, 15))

            datos_principales = [
                [Paragraph(f"<b>MINUTA N°:</b> {id_minuta}", style_texto), Paragraph(f"<b>FECHA:</b> {fecha}", style_texto)],
                [Paragraph(f"<b>TRÁMITE:</b> {tipo_tramite}", style_texto), Paragraph(f"<b>MONTO:</b> ${monto}", style_texto)]
            ]
            t_principal = Table(datos_principales, colWidths=[260, 260])
            t_principal.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F7FAFC")),
                ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E0")),
                ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
                ('TOPPADDING', (0,0), (-1,-1), 6),
                ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ]))
            story.append(t_principal)
            story.append(Spacer(1, 12))

            story.append(Paragraph("<b>1. UBICACIÓN Y ANTECEDENTES DEL INMUEBLE</b>", style_sub))
            story.append(Paragraph(inmueble_texto, style_texto))
            story.append(Spacer(1, 12))

            story.append(Paragraph("<b>2. TRANSMITENTES (VENDEDORES)</b>", style_sub))
            for v in vendedores:
                story.append(Paragraph(f"• {v}", style_texto))
            story.append(Spacer(1, 12))

            story.append(Paragraph("<b>3. ADQUIRENTES (COMPRADORES)</b>", style_sub))
            for c in compradores:
                story.append(Paragraph(f"• {c}", style_texto))
            story.append(Spacer(1, 12))

            story.append(Paragraph("<b>4. OBSERVACIONES / MOTIVO</b>", style_sub))
            story.append(Paragraph(observaciones if observaciones else "Sin observaciones particulares.", style_texto))
            story.append(Spacer(1, 35))

            datos_firmas = [["", ""], [Paragraph("<font size=9>__________________________<br/>FIRMA Y SELLO ESCRIBANO</font>", ParagraphStyle('C', alignment=1)), 
                                        Paragraph("<font size=9>__________________________<br/>FIRMA DEL REGISTRADOR</font>", ParagraphStyle('C', alignment=1))]]
            t_firmas = Table(datos_firmas, colWidths=[260, 260])
            story.append(t_firmas)

            doc.build(story)
            print(f"📄 ¡PDF generado con éxito en: {nombre_archivo}!")
            os.startfile(os.path.abspath(nombre_archivo))

        except Exception as e:
            print(f"Error al generar el documento PDF: {e}")

    # --- TABLA CLIENTES ---
    def guardar_cliente(self):
        dni = self.txt_dni.text().strip()
        nombre = self.txt_nombre.text().strip()
        apellido = self.txt_apellido.text().strip()
        cuil = self.txt_cuil.text().strip()
        fecha_nac = self.txt_fecha_nac.date().toString("yyyy-MM-dd") 
        domicilio = self.txt_domicilio.text().strip()
        localidad = self.txt_localidad.text().strip()
        provincia = self.txt_provincia.text().strip()
        telefono = self.txt_telefono.text().strip()
        email = self.txt_email.text().strip()
        
        if not dni or not name or not apellido: return
        domicilio = domicilio if domicilio else None
        localidad = localidad if localidad else None
        provincia = provincia if provincia else None
        telefono = telefono if telefono else None
        email = email if email else None

        conexion = None
        try:
            conexion = mysql.connector.connect(host="localhost", user="root", password="admin123", database="proyecto_final_bd")
            cursor = conexion.cursor()
            query = "INSERT INTO personas (nombre, apellido, dni, cuil, fecha_nacimiento, domicilio, localidad, provincia, telefono, email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            valores = (nombre, apellido, dni, cuil, fecha_nac, domicilio, localidad, provincia, telefono, email)
            cursor.execute(query, valores)
            conexion.commit()
            print(f"¡{nombre} {apellido} registrado con éxito!")
            
            self.txt_dni.clear(); self.txt_nombre.clear(); self.txt_apellido.clear(); self.txt_cuil.clear()
            self.txt_domicilio.clear(); self.txt_localidad.clear(); self.txt_provincia.clear(); self.txt_telefono.clear(); self.txt_email.clear()
            self.txt_fecha_nac.setDate(QDate.currentDate())
        except mysql.connector.Error as error: print(error)
        finally:
            if conexion and conexion.is_connected(): cursor.close(); conexion.close()

    # --- TABLA INMUEBLES ---
    def guardar_inmueble(self):
        partida = self.txt_partida.text().strip()
        nomenclatura = self.txt_nomenclatura.text().strip()
        domicilio = self.txt_domicilio_inm.text().strip()
        tipo = self.txt_tipo_inm.currentText().strip()
        destino = self.txt_destino.currentText().strip()
        superficie = self.txt_superficie_inm.text().strip()
        depto = self.txt_depto.text().strip()
        localidad = self.txt_localidad_inm.text().strip()
        registro = self.txt_registro.text().strip()
        folio = self.txt_folio.text().strip()
        tomo = self.txt_tomo.text().strip()
        anio = self.txt_anio.text().strip()
        
        if not partida or not domicilio: return
        nomenclatura = nomenclatura if nomenclatura else None
        tipo = tipo if tipo else None
        superficie = superficie if superficie else None
        destino = destino if destino else None
        depto = depto if depto else None
        localidad = localidad if localidad else None
        registro = registro if registro else None
        folio = folio if folio else None
        tomo = tomo if tomo else None
        anio = anio if anio else None

        conexion = None
        try:
            conexion = mysql.connector.connect(host="localhost", user="root", password="", database="proyecto_final_bd")
            cursor = conexion.cursor()
            query = "INSERT INTO inmuebles (partida_inmobiliaria, nomenclatura_catastral, domicilio_inmueble, tipo_inmueble, superficie, destino, departamento, localidad, registro_propiedad, folio, tomo, anio_inscripcion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            valores = (partida, nomenclatura, domicilio, tipo, superficie, destino, depto, localidad, registro, folio, tomo, anio)
            cursor.execute(query, valores)
            conexion.commit()
            print(f"¡Inmueble ubicado en {domicilio} registrado con éxito!")
            
            self.txt_partida.clear(); self.txt_nomenclatura.clear(); self.txt_domicilio_inm.clear(); self.txt_superficie_inm.clear()
            self.txt_depto.clear(); self.txt_localidad_inm.clear(); self.txt_registro.clear(); self.txt_folio.clear(); self.txt_tomo.clear(); self.txt_anio.clear()
        except mysql.connector.Error as error: print(error)
        finally:
            if conexion and conexion.is_connected(): cursor.close(); conexion.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    user_test = {'usuario': 'facundo_rojo', 'rol': 'Escribano'}
    ventana = MainWindow(user_test)
    ventana.show()
    sys.exit(app.exec())