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
            
        # --- NAVEGACIÓN POR ÍNDICES CORREGIDA ---
        self.btn_home.clicked.connect(lambda: self.contenedor_paginas.setCurrentIndex(0))
        self.btn_clientes.clicked.connect(lambda: self.contenedor_paginas.setCurrentIndex(1))
        self.btn_inmuebles.clicked.connect(lambda: self.contenedor_paginas.setCurrentIndex(2))
        self.btn_minutas.clicked.connect(lambda: self.contenedor_paginas.setCurrentIndex(3))
        
        # --- CONEXIÓN DEL BOTÓN GUARDAR (Nombre corregido sin errores de tipeo) ---
        self.btn_guardar_cliente.clicked.connect(self.guardar_cliente)
        
    def guardar_cliente(self):
        # 1. Traemos los datos básicos de los QLineEdit
        dni = self.txt_dni.text().strip()
        nombre = self.txt_nombre.text().strip()
        apellido = self.txt_apellido.text().strip()
        cuil = self.txt_cuil.text().strip()
        
        # 2. CAPTURA DE FECHA DESDE QDateEdit
        # Convertimos la fecha al formato string "AAAA-MM-DD" que exige MySQL
        fecha_qt = self.txt_fecha_nac.date()
        fecha_nac = fecha_qt.toString("yyyy-MM-dd") 
        
        # 3. Traemos el resto de los campos de texto agregados
        domicilio = self.txt_domicilio.text().strip()
        localidad = self.txt_localidad.text().strip()
        provincia = self.txt_provincia.text().strip()
        telefono = self.txt_telefono.text().strip()
        email = self.txt_email.text().strip()
        
        # Validación rápida de obligatorios antes de enviar a la BD
        if not dni or not nombre or not apellido:
            print("Error: El DNI, Nombre y Apellido son campos obligatorios.")
            return
            
        # Si los campos opcionales están vacíos, los pasamos como None (NULL en MySQL)
        domicilio = domicilio if domicilio else None
        localidad = localidad if localidad else None
        provincia = provincia if provincia else None
        telefono = telefono if telefono else None
        email = email if email else None

        # 4. Conexión e inserción física en MySQL
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
                INSERT INTO personas 
                (nombre, apellido, dni, cuil, fecha_nacimiento, domicilio, localidad, provincia, telefono, email) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            valores = (
                nombre, apellido, dni, cuil, fecha_nac,
                domicilio, localidad, provincia, telefono, email
            )
            
            cursor.execute(query, valores)
            conexion.commit()
            
            print(f"¡{nombre} {apellido} registrado con éxito con todos sus datos!")
            
            # 5. Limpiamos todos los campos del formulario para la próxima carga
            self.txt_dni.clear()
            self.txt_nombre.clear()
            self.txt_apellido.clear()
            self.txt_cuil.clear()
            self.txt_domicilio.clear()
            self.txt_localidad.clear()
            self.txt_provincia.clear()
            self.txt_telefono.clear()
            self.txt_email.clear()
            self.txt_fecha_nac.setDate(QDate.currentDate()) # Resetea la fecha a hoy
            
        except mysql.connector.Error as error:
            print(f"Error detallado de MySQL: {error}")
            
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