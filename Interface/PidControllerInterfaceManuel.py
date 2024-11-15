from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QPushButton, QLabel, QDoubleSpinBox, QCheckBox, QSlider, QGroupBox)
from PySide6.QtCore import Qt, QTimer
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np


class PIDControlApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PID Controller Interface")
        self.setGeometry(100, 100, 800, 600)

        # Layout principal
        main_layout = QHBoxLayout()

        # Création du panneau de contrôle
        control_panel = QWidget()
        control_layout = QVBoxLayout(control_panel)

        # Boutons Start/Stop
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
        control_layout.addWidget(self.start_button)
        control_layout.addWidget(self.stop_button)

        # Zone de saisie de la vitesse de consigne
        self.set_point_label = QLabel("Speed set point (RPM)")
        self.set_point_slider = QSlider(Qt.Horizontal)
        self.set_point_slider.setMinimum(0)
        self.set_point_slider.setMaximum(7000)
        self.set_point_slider.setValue(30)
        self.set_point_value = QLabel("30")
        self.set_point_slider.valueChanged.connect(self.update_set_point)

        control_layout.addWidget(self.set_point_label)
        control_layout.addWidget(self.set_point_slider)
        control_layout.addWidget(self.set_point_value)

        # Zone d'affichage de la vitesse mesurée
        self.actual_speed_label = QLabel("Actual Speed (RPM):")
        self.actual_speed_display = QLabel("0.0")
        control_layout.addWidget(self.actual_speed_label)
        control_layout.addWidget(self.actual_speed_display)

        # Paramètres PID
        pid_group = QGroupBox("PID Parameters")
        pid_layout = QVBoxLayout(pid_group)
        self.proportional_checkbox = QCheckBox("Proportionnelle")
        self.integral_checkbox = QCheckBox("Intégrale")
        self.derivative_checkbox = QCheckBox("Dérivée")

        self.proportional_input = QDoubleSpinBox()
        self.integral_input = QDoubleSpinBox()
        self.derivative_input = QDoubleSpinBox()

        pid_layout.addWidget(self.proportional_checkbox)
        pid_layout.addWidget(self.proportional_input)
        pid_layout.addWidget(self.integral_checkbox)
        pid_layout.addWidget(self.integral_input)
        pid_layout.addWidget(self.derivative_checkbox)
        pid_layout.addWidget(self.derivative_input)

        control_layout.addWidget(pid_group)

        # Bouton de mise à jour du graphique
        self.update_chart_button = QPushButton("Update Chart")
        control_layout.addWidget(self.update_chart_button)

        # Ajouter le panneau de contrôle au layout principal
        main_layout.addWidget(control_panel)

        # Graphique
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        main_layout.addWidget(self.canvas)

        # Création du widget central et configuration
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Connexions des boutons
        self.start_button.clicked.connect(self.start_motor)
        self.stop_button.clicked.connect(self.stop_motor)
        self.update_chart_button.clicked.connect(self.update_chart)

        # Données fictives pour le graphique
        self.time_data = []  # On va commencer sans données
        self.speed_data = []  # Liste vide pour stocker les vitesses

        # Paramètres de la sinusoïdale
        self.amplitude = 1000  # Amplitude de la sinusoïdale (valeur max de la vitesse)
        self.frequency = 0.1  # Fréquence de la sinusoïdale (période)
        self.angle = 0 # Variable pour suivre l'angle de la sinusoïdale


        # Initialisation du QTimer pour mettre à jour le graphique toutes les 1 seconde
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_chart_real_time)  # Connecte le timer à la méthode de mise à jour
        self.timer.start(100)  # Intervalle de 100 ms (0.1 seconde)


    def update_set_point(self, value):
        """Met à jour la valeur de consigne affichée."""
        self.set_point_value.setText(str(value))

    def start_motor(self):
        """Logique pour démarrer le moteur."""
        print("Moteur démarré")
        # Logique pour lancer le moteur (exemple)

    def stop_motor(self):
        """Logique pour arrêter le moteur."""
        print("Moteur arrêté")
        # Logique pour stopper le moteur (exemple)

    def update_chart(self):
        """Met à jour le graphique avec des données fictives (manuelle)."""
        self.ax.clear()
        x = np.arange(100)
        y = np.sin(x / 10) * 1000  # Données fictives sinusoidales
        self.ax.plot(x, y, label="Speed")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("RPM")
        self.ax.legend()
        self.canvas.draw()

    def update_chart_real_time(self):
        """Met à jour le graphique en temps réel avec des données fictives."""
        # Exemple de données fictives générées avec un bruit
        new_speed = self.amplitude * np.sin(self.angle)
        # Incrémenter l'angle pour faire avancer la sinusoïdale
        self.angle += self.frequency  # Ajouter l'offset de fréquence pour une évolution continue

        # Ajouter les nouvelles données à la liste
        self.time_data.append(self.time_data[-1] + 1 if self.time_data else 0)  # Temps qui augmente à chaque itération
        self.speed_data.append(new_speed)

        # Limiter la taille des tableaux pour ne pas saturer la mémoire
        if len(self.time_data) > 100:
            self.time_data = self.time_data[1:]
            self.speed_data = self.speed_data[1:]

        # Mise à jour du graphique
        self.ax.clear()
        self.ax.plot(self.time_data, self.speed_data, label="Speed")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("RPM")
        self.ax.set_ylim(min(self.speed_data) - 100, max(self.speed_data) + 100)  # Ajuster l'échelle Y
        self.ax.legend()
        self.canvas.draw()

