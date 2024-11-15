from PySide6.QtWidgets import QApplication, QMainWindow
import Interface.mainwindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import sys


class PIDControlApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Interface.Ui_MainWindow()
        self.ui.setupUi(self)

        # Connexion des boutons
        self.ui.pushButton_2.clicked.connect(self.start_motor)
        self.ui.pushButton.clicked.connect(self.stop_motor)
        self.ui.pushButton_3.clicked.connect(self.update_chart)

        # Connexion du slider
        self.ui.horizontalSlider.valueChanged.connect(self.update_set_point_display)

        # Création du graphique avec Matplotlib
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        # Ajouter le canvas au widget `widget_2` (espace pour le graphique)
        self.ui.horizontalLayout_2.addWidget(self.canvas)

    def update_set_point_display(self, value):
        """Met à jour l'affichage de la consigne en fonction du slider."""
        self.ui.label_2.setText(str(value))

    def start_motor(self):
        """Logique pour démarrer le moteur (exemple)."""
        print("Moteur démarré")
        # Logique additionnelle pour lancer le moteur

    def stop_motor(self):
        """Logique pour arrêter le moteur (exemple)."""
        print("Moteur arrêté")
        # Logique additionnelle pour stopper le moteur

    def update_chart(self):
        """Met à jour le graphique avec des données fictives pour tester."""
        self.ax.clear()
        x = range(100)
        y = [i * 0.5 for i in x]  # Exemple de données
        self.ax.plot(x, y, label="Speed")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("RPM")
        self.ax.legend()
        self.canvas.draw()
