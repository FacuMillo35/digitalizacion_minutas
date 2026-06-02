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
        
    def configurar_interfaz(self):
        # El saludo de bienvenida
        if hasattr(self, 'lbl_bienvenida'):
            self.lbl_bienvenida.setText(f"Bienvenido, {self.usuario['usuario']}")
            
        # --- NAVEGACIÓN POR ÍNDICES ---
        self.btn_home.clicked.connect(lambda: self.contenedor_paginas.setCurrentIndex(0))
        self.btn_clientes.clicked.connect(lambda: self.contenedor_paginas.setCurrentIndex(1))
        self.btn_inmuebles.clicked.connect(lambda: self.contenedor_paginas.setCurrentIndex(2))
        self.btn_minutas.clicked.connect(lambda: self.contenedor_paginas.setCurrentIndex(3))
        
        # --- CONEXIÓN BOTÓN GUARDAR CLIENTE (PERSONA) ---
        self.btn_guardar_cliente.clicked.connect(self.guardar_cliente)
        
        # --- CONEXIÓN BOTÓN GUARDAR INMUEBLE ---
        self.btn_guardar_inmueble.clicked.connect(self.guardar_inmueble)
        
    def guardar_cliente(self):
        dni = self.txt_dni.text().strip()
        nombre = self.txt_nombre.text().strip()
        apellido = self.txt_apellido.text().strip()
        cuil = self.txt_cuil.text().strip()
        
        fecha_qt = self.txt_fecha_nac.date()
        fecha_nac = fecha_qt.toString("yyyy-MM-dd") 
        
        domicilio = self.txt_domicilio.text().strip()
        localidad = self.txt_localidad.text().strip()
        provincia = self.txt_provincia.text().strip()
        telefono = self.txt_telefono.text().strip()
        email = self.txt_email.text().strip()
        
        if not dni or not nombre or not apellido:
            print("Error: El DNI, Nombre y Apellido son campos obligatorios.")
            return
            
        domicilio = domicilio if domicilio else None
        localidad = localidad if localidad else None
        provincia = provincia if provincia else None
        telefono = telefono if telefono else None
        email = email if email else None

        conexion = None
        try:
            conexion = mysql.connector.connect(
                host="localhost", user="root", password="", database="proyecto_final_bd"
            )
            cursor = conexion.cursor()
            query = """
                INSERT INTO personas 
                (nombre, apellido, dni, cuil, fecha_nacimiento, domicilio, localidad, provincia, telefono, email) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            valores = (nombre, apellido, dni, cuil, fecha_nac, domicilio, localidad, provincia, telefono, email)
            cursor.execute(query, valores)
            conexion.commit()
            print(f"¡{nombre} {apellido} registrado con éxito!")
            
            self.txt_dni.clear()
            self.txt_nombre.clear()
            self.txt_apellido.clear()
            self.txt_cuil.clear()
            self.txt_domicilio.clear()
            self.txt_localidad.clear()
            self.txt_provincia.clear()
            self.txt_telefono.clear()
            self.txt_email.clear()
            self.txt_fecha_nac.setDate(QDate.currentDate())
            
        except mysql.connector.Error as error:
            print(f"Error detallado de MySQL: {error}")
        finally:
            if conexion and conexion.is_connected():
                cursor.close()
                conexion.close()

    def guardar_inmueble(self):
        # 1. Capturamos los datos de la interfaz
        partida = self.txt_partida.text().strip()
        nomenclatura = self.txt_nomenclatura.text().strip()
        domicilio = self.txt_domicilio_inm.text().strip()
        
        # --- LECTURA DE LOS COMBOBOX (Tipo y Destino) ---
        tipo = self.txt_tipo_inm.currentText().strip()
        destino = self.txt_destino.currentText().strip()
        
        superficie = self.txt_superficie_inm.text().strip()
        depto = self.txt_depto.text().strip()
        localidad = self.txt_localidad_inm.text().strip()
        registro = self.txt_registro.text().strip()
        folio = self.txt_folio.text().strip()
        tomo = self.txt_tomo.text().strip()
        anio = self.txt_anio.text().strip()
        
        # 2. Validación rápida de obligatorios
        if not partida or not domicilio:
            print("Error: La Partida Inmobiliaria y el Domicilio son obligatorios.")
            return
            
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

        # 3. Inserción en la Base de Datos
        conexion = None
        try:
            conexion = mysql.connector.connect(
                host="localhost", 
                user="root", 
                password="admin123", 
                database="proyecto_final_bd"
            )
            cursor = conexion.cursor()
            
            query = """
                INSERT INTO inmuebles 
                (partida_inmobiliaria, nomenclatura_catastral, domicilio_inmueble, tipo_inmueble, 
                 superficie, destino, departamento, localidad, registro_propiedad, folio, tomo, anio_inscripcion) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            valores = (partida, nomenclatura, domicilio, tipo, superficie, destino, depto, localidad, registro, folio, tomo, anio)
            
            cursor.execute(query, valores)
            conexion.commit()
            print(f"¡Inmueble ubicado en {domicilio} registrado con éxito!")
            
            # 4. Limpiamos campos de texto (los combo box no hace falta limpiarlos)
            self.txt_partida.clear()
            self.txt_nomenclatura.clear()
            self.txt_domicilio_inm.clear()
            self.txt_superficie_inm.clear()
            self.txt_depto.clear()
            self.txt_localidad_inm.clear()
            self.txt_registro.clear()
            self.txt_folio.clear()
            self.txt_tomo.clear()
            self.txt_anio.clear()
            
        except mysql.connector.Error as error:
            print(f"Error de MySQL al guardar inmueble: {error}")
        finally:
            if conexion and conexion.is_connected():
                cursor.close()
                conexion.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    user_test = {'usuario': 'facundo_rojo', 'rol': 'Escribano'}
    ventana = MainWindow(user_test)
    ventana.show()
    sys.exit(app.exec())