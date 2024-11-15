import sys

from PySide6.QtWidgets import QApplication
import Interface
# Exécution de l'application
from Interface.PidControllerInterfaceManuel import PIDControlApp

app = QApplication(sys.argv)
window = PIDControlApp()
window.show()
sys.exit(app.exec())
