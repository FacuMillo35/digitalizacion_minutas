import sys
import os

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox

from conexion_db import obtener_conexion


class LoginWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Ruta absoluta al archivo .ui
        ruta_ui = os.path.join(
            os.path.dirname(__file__),
            "..",
            "ui",
            "login.ui"
        )

        ruta_ui = os.path.abspath(ruta_ui)

        # Cargar interfaz
        try:
            uic.loadUi(ruta_ui, self)

        except Exception as e:
            print(f"Error al cargar el archivo .ui: {e}")
            return

        # Conectar botón
        self.btn_ingresar.clicked.connect(self.intentar_logueo)

    def intentar_logueo(self):

        usuario_txt = self.txt_usuario.text()
        password_txt = self.txt_password.text()

        # Validación básica
        if not usuario_txt or not password_txt:

            QMessageBox.warning(
                self,
                "Campos vacíos",
                "Por favor complete todos los campos."
            )

            return

        # Obtener conexión desde conexion_db.py
        db = obtener_conexion()

        if not db:

            QMessageBox.critical(
                self,
                "Error",
                "No se pudo conectar a la base de datos."
            )

            return

        try:

            cursor = db.cursor(dictionary=True)

            query = """
                SELECT usuario, password, rol
                FROM usuarios
                WHERE usuario = %s
                AND password = %s
            """

            cursor.execute(query, (usuario_txt, password_txt))

            resultado = cursor.fetchone()

            if resultado:

                rol = resultado["rol"]

                QMessageBox.information(
                    self,
                    "Login correcto",
                    f"Bienvenido {usuario_txt}\nRol: {rol}"
                )

                # Más adelante:
                # abrir ventana principal

            else:

                QMessageBox.warning(
                    self,
                    "Acceso denegado",
                    "Usuario o contraseña incorrectos."
                )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error SQL",
                str(e)
            )

        finally:

            cursor.close()
            db.close()


if __name__ == "__main__":

    app = QApplication(sys.argv)

    ventana = LoginWindow()
    ventana.show()

    sys.exit(app.exec())