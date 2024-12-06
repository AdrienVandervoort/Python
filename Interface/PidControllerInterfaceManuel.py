import matplotlib.pyplot as plt

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QPushButton, QLabel, QDoubleSpinBox, QCheckBox, QSlider, QGroupBox)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from telemetrix import telemetrix

from Class.ClassMotor import Motor
import pandas as pd
from datetime import datetime


class PIDControlApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PID Controller Interface")
        self.setGeometry(100, 100, 800, 600)

        # === Initialisation de la carte et du moteur ===
        print("Connexion à l'Arduino...")
        self.board = telemetrix.Telemetrix()
        self.motor = Motor(
            board=self.board,
            pwm_pin=3,
            dir_pin=12,
            encoder_pin_a=2,
            encoder_pin_b=7,
            ticks_per_revolution=12
        )

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
        self.set_point_slider.setMaximum(self.motor.maxspeed())
        self.set_point_slider.setValue(0)
        self.set_point_value = QLabel("0")
        self.set_point_slider.setEnabled(True)  # S'assurer que le slider est activé

        self.set_point_slider.valueChanged.connect(self.update_set_point)

        self.pwm_label = QLabel("PWM Value:")
        self.pwm_display = QLabel("0.0")
        control_layout.addWidget(self.pwm_label)
        control_layout.addWidget(self.pwm_display)

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
        self.update_chart_button.clicked.connect(self.update_chart_real_time)

        ###############################################################################################
        ##########################################PAS REGARGER#########################################
        ###############################################################################################
         # Paramètres de la sinusoïdale
        '''
        self.amplitude = 1000  # Amplitude de la sinusoïdale (valeur max de la vitesse)
        self.frequency = 0.1  # Fréquence de la sinusoïdale (période)
        self.angle = 0  # Variable pour suivre l'angle de la sinusoïdale
        '''

        ###############################################################################################
        ##########################################REGARGER#########################################
        ###############################################################################################
        # Initialisation du QTimer pour mettre à jour le graphique toutes les 0.1 seconde
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_chart_real_time)  # Connecte le timer à la méthode de mise à jour
        self.timer.start(100)  # Intervalle de 1000 ms (1 seconde)

        # Données fictives pour le graphique
        self.time_data = []  # On va commencer sans données
        self.speed_data = []  # Liste vide pour stocker les vitesses

    def update_set_point(self, value):
        """Met à jour la valeur de consigne affichée."""
        self.set_point_value.setText(str(value))

    def start_motor(self):
        """Logique pour démarrer le moteur."""
        try:
            self.motor.start()
            self.timer.start()
            print("Moteur démarré")
        except Exception as e:
            print(f"Erreur : {e}")

    def stop_motor(self):
        """Logique pour arrêter le moteur."""
        try:
            self.motor.stop()  # Arrête le moteur
            self.timer.stop()
            print("Moteur arrêté.")
        except Exception as e:
            print(f"Erreur : {e}")

    def update_pid_parameters(self):
        """Met à jour les paramètres PID du moteur en fonction des valeurs saisies et des cases cochées."""
        try:
            # Initialiser les valeurs PID à 0
            p_value, i_value, d_value = 0.0, 0.0, 0.0

            # Appliquer uniquement les paramètres activés par les cases à cocher
            if self.proportional_checkbox.isChecked():
                p_value = self.proportional_input.value()
            if self.integral_checkbox.isChecked():
                i_value = self.integral_input.value()
            if self.derivative_checkbox.isChecked():
                d_value = self.derivative_input.value()

            # Appliquer les valeurs au moteur
            self.motor.set_pid_parameters(p_value, i_value, d_value)
            print(f"PID mis à jour : P={p_value}, I={i_value}, D={d_value}")

        except Exception as e:
            print(f"Erreur lors de la mise à jour des paramètres PID : {e}")

    ###############################################################################################
    ##########################################PAS REGARGER#########################################
    ###############################################################################################
    '''def update_chart_real_time(self):  # TODO voir effacer
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
        self.canvas.draw()'''
    ###############################################################################################
    ##########################################REGARGER#########################################
    ###############################################################################################

    def update_chart_real_time(self):
        """Met à jour le graphique avec les données de vitesse réelle en temps réel."""
        try:
            measured_speed = self.motor.measure_speed(measurement_time=0.1)

            current_time = self.time_data[-1] + 0.1 if self.time_data else 0
            self.time_data.append(current_time)
            self.speed_data.append(measured_speed)

            if len(self.time_data) > 100:
                self.time_data = self.time_data[1:]
                self.speed_data = self.speed_data[1:]

            rmpmax = self.motor.maxspeed()
            self.update_motor_speed(self.set_point_slider.value())

            # Ajuster dynamiquement la limite du slider
            self.set_point_slider.setMaximum(rmpmax)

            self.ax.clear()
            self.ax.plot(self.time_data, self.speed_data, label="Measured Speed (RPM)", color="blue")
            self.ax.set_title(f"Motor Speed Over Time (Max: {rmpmax:.2f} RPM)")
            self.ax.set_xlabel("Time (s)")
            self.ax.set_ylabel("Speed (RPM)")
            self.ax.set_ylim(0.01, rmpmax)
            self.ax.legend()
            self.canvas.draw()

            self.actual_speed_display.setText(f"{measured_speed:.2f} RPM")

        except Exception as e:
            print(f"Erreur lors de la mise à jour du graphique : {e}")

    def update_motor_speed(self, slider_value):
        """Met à jour la vitesse du moteur en fonction de la valeur du slider."""
        rmpmax = self.motor.maxspeed()

        # Vérifier si rmpmax est zéro pour éviter la division par zéro
        if rmpmax == 0:
            print("Erreur : la vitesse maximale du moteur est égale à zéro.")
            pwm = 0  # Eviter de diviser par zéro
        else:
            pwm = (slider_value / rmpmax) * 255
            print(f"Le résultat de la PWM est {pwm}, affichage du slider : {slider_value}")

        print(f"Le résultat de la PWM est {pwm}, affichage du slider : {slider_value}")
        self.motor.start(pwm)
        self.pwm_display.setText(f"{pwm:.2f}")

    def closeEvent(self, event):
        print("Programme fermé")
        self.motor.stop()