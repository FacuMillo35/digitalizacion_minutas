import os
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication

class MainWindow(QMainWindow):
    def __init__(self, datos_usuario):
        super().__init__()
        
        # --- EL TRUCO DEL DETECTIVE ---
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
        # Aquí usas los objectName que hayas puesto ayer en el Designer
        if hasattr(self, 'lbl_bienvenida'):
            self.lbl_bienvenida.setText(f"Bienvenido, {self.usuario['usuario']}")
            
        # Conectar tus botones del QStackedWidget que vimos antes...
        # self.btn_clientes.clicked.connect(lambda: self.contenedor_paginas.setCurrentIndex(1))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    user_test = {'usuario': 'facundo_rojo', 'rol': 'Escribano'}
    ventana = MainWindow(user_test)
    ventana.show()
    sys.exit(app.exec())
