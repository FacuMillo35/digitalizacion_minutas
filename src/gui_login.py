import sys
import mysql.connector
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 1. Carga la interfaz (ajusta la ruta si tu .ui está en otra carpeta)
        try:
            uic.loadUi("../ui/login.ui", self)
        except Exception as e:
            print(f"Error al cargar el archivo .ui: {e}")

        # 2. Conectar el botón (asegúrate que en Designer se llame btn_ingresar)
        self.btn_ingresar.clicked.connect(self.intentar_logueo)

    def conectar_db(self):
        """Establece la conexión con MySQL"""
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",           # Tu usuario de MySQL
                password="admin123",  # Tu contraseña de MySQL
                database="proyecto_final_bd" # El nombre de tu esquema
            )
            return conexion
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Error de Conexión", f"No se pudo conectar a la base de datos: {err}")
            return None

    def intentar_logueo(self):
        """Valida las credenciales contra la base de datos"""
        # Obtener texto de los campos (ajusta nombres según tu Designer)
        usuario_txt = self.txt_usuario.text()
        password_txt = self.txt_password.text()

        if not usuario_txt or not password_txt:
            QMessageBox.warning(self, "Campos vacíos", "Por favor, complete todos los campos.")
            return

        db = self.conectar_db()
        if db:
            cursor = db.cursor(dictionary=True)
            # Usamos los nombres exactos de tus columnas: usuario y password
            query = "SELECT usuario, password, rol FROM usuarios WHERE usuario = %s AND password = %s"
            
            try:
                cursor.execute(query, (usuario_txt, password_txt))
                resultado = cursor.fetchone()

                if resultado:
                    rol = resultado['rol']
                    QMessageBox.information(self, "Éxito", f"Bienvenido {usuario_txt}\nRol: {rol}")
                    # AQUÍ: Más adelante llamaremos a la ventana principal
                    # self.abrir_ventana_principal()
                else:
                    QMessageBox.warning(self, "Acceso Denegado", "Usuario o contraseña incorrectos.")
            
            except mysql.connector.Error as err:
                print(f"Error en la consulta: {err}")
            finally:
                cursor.close()
                db.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = LoginWindow()
    ventana.show()
    sys.exit(app.exec())