import os
import sys
import mysql.connector
from PyQt6 import uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QMainWindow, QApplication, QDialog
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import modulo_clientes
import modulo_inmuebles
import modulo_minutas

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
        # carga de logo de escribania
        ruta_logo = r"C:\Users\facur\OneDrive\Documentos\AAA UTN\Proyecto Final Digitalizacion Minutas\logo_escribania.jpg"
        if hasattr(self, 'lbl_logo'):
            if os.path.exists(ruta_logo):
                pixmap = QPixmap(ruta_logo)
                # Escala la imagen para que encaje perfecto sin deformarse
                pixmap_escalado = pixmap.scaled(
                    self.lbl_logo.width(), 
                    self.lbl_logo.height(), 
                    Qt.AspectRatioMode.KeepAspectRatio, 
                    Qt.TransformationMode.SmoothTransformation
                )
                self.lbl_logo.setPixmap(pixmap_escalado)
                self.lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
            else:
                print("Aviso: No se encontró la imagen del logo.")
            
        # --- NAVEGACIÓN POR ÍNDICES ---
        self.btn_home.clicked.connect(lambda: self.contenedor_paginas.setCurrentIndex(0))
        self.btn_clientes.clicked.connect(lambda: self.contenedor_paginas.setCurrentIndex(1))
        self.btn_inmuebles.clicked.connect(lambda: self.contenedor_paginas.setCurrentIndex(2))
        self.btn_minutas.clicked.connect(lambda: self.contenedor_paginas.setCurrentIndex(3))
        self.btn_configuracion.clicked.connect(lambda: self.contenedor_paginas.setCurrentIndex(4))
        self.btn_cerrar_sesion.clicked.connect(self.cerrar_sesion)
        # --- CONEXIONES DE BOTONES DE GUARDADO ---
        # El 'lambda' sirve para poder enviarle 'self' (la ventana) al otro archivo
        self.btn_guardar_cliente.clicked.connect(lambda: modulo_clientes.guardar_cliente(self))
        self.btn_guardar_inmueble.clicked.connect(lambda: modulo_inmuebles.guardar_inmueble(self))
        self.btn_guardar_minuta.clicked.connect(lambda: modulo_minutas.guardar_minuta(self))
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
            else:
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
    def cerrar_sesion(self):
        """Cierra la ventana principal y vuelve a abrir el login"""
        # Importación "local" para evitar que Python se maree (importación circular)
        from gui_login import LoginWindow 
        
        # 1. Instanciamos y mostramos la ventana de Login
        self.ventana_login = LoginWindow() 
        self.ventana_login.show()
        
        # 2. Cerramos el panel principal
        self.close()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # --- NUEVO: Carga automática de estilos QSS ---
    ruta_estilos = "estilos.qss"
    if os.path.exists(ruta_estilos):
        with open(ruta_estilos, "r") as f:
            app.setStyleSheet(f.read())
    else:
        print("Aviso: No se encontró el archivo estilos.qss")