import sys
from PyQt6.QtWidgets import QApplication
from gui_login import LoginWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    ventana = LoginWindow()
    ventana.show()

    sys.exit(app.exec())