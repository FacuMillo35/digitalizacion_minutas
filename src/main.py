import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget

class TestVentana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UTN - Gestión de Minutas C")
        self.setFixedSize(400, 200)

        # Contenedor principal
        layout = QVBoxLayout()
        label = QLabel("¡PyQt6 funcionando perfectamente!")
        layout.addWidget(label)

        contenedor = QWidget()
        contenedor.setLayout(layout)
        self.setCentralWidget(contenedor)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = TestVentana()
    ventana.show()
    sys.exit(app.exec())