import os

import matplotlib.pyplot as plt
import self

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

        # === Chargement de rpmmax depuis le fichier .dat ===
        self.rpmmax = self.load_rpmmax()

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

        self.slider_data = []  # Liste pour les valeurs du slider
        self.pwm_data = []  # Liste pour les valeurs de la PWM

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
        self.set_point_slider.setMaximum(int(self.rpmmax))
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
        self.proportional_input.setRange(0, 5)  # Set the range for the spin box
        self.proportional_input.setDecimals(10)  # Set precision to 10 decimals
        self.proportional_input.setSingleStep(0.01)  # Step size for increment/decrement

        self.integral_input = QDoubleSpinBox()
        self.integral_input.setRange(0, 5)
        self.integral_input.setDecimals(10)
        self.integral_input.setSingleStep(0.01)

        self.derivative_input = QDoubleSpinBox()
        self.derivative_input.setRange(0, 5)
        self.derivative_input.setDecimals(10)
        self.derivative_input.setSingleStep(0.01)

        pid_layout.addWidget(self.proportional_checkbox)
        pid_layout.addWidget(self.proportional_input)
        pid_layout.addWidget(self.integral_checkbox)
        pid_layout.addWidget(self.integral_input)
        pid_layout.addWidget(self.derivative_checkbox)
        pid_layout.addWidget(self.derivative_input)

        control_layout.addWidget(pid_group)

        # Bouton de mise à jour du graphique
        # Creating the "Update Chart" button
        self.update_chart_button = QPushButton("Update Chart")
        control_layout.addWidget(self.update_chart_button)

        # Connecting the button to the update_pid_parameters method
        self.update_chart_button.clicked.connect(self.update_pid_parameters)

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
        self.timer.start(100)  # Intervalle de 100 ms (0.1 seconde)

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

    def load_rpmmax(self):
        """Charge la valeur de rpmmax depuis le fichier .dat ou retourne une valeur par défaut."""
        try:
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            file_path = os.path.join(desktop, "rpm_average.dat")
            with open(file_path, "r") as file:
                content = file.read()
                rpmmax = float(content.split(":")[1].strip())
                #       print(f"Valeur chargée depuis {file_path} : {rpmmax:.2f}")
                return rpmmax
        except FileNotFoundError:
            #  print("Fichier rpm_average.dat introuvable. Défaut à 1500 RPM.")
            return 1600
        except Exception as e:
            print(f"Erreur lors du chargement de rpmmax : {e}")
            return 1600

    def update_motor_control(self, pwm):
        """
        Update motor control based on PID output.
        """
        try:
            # Get the desired set point from the slider
            set_point = self.set_point_slider.value()

            # Measure the actual speed of the motor
            actual_speed = self.motor.measure_speed(measurement_time=0.1)

            # Compute the PID control output
            pwm_output = self.motor.pid_control(set_point=set_point, actual_speed=actual_speed, dt=1)

            # Apply the PID output as PWM to the motor
            corrupt = pwm_output
            corrupt = max(0, min(255, corrupt))
            self.motor.start(corrupt)

            # Update the display
            self.actual_speed_display.setText(f"{actual_speed:.2f} RPM")
            self.pwm_display.setText(f"{pwm_output:.2f}")

        except Exception as e:
            pass
            # print(f"Error in motor control update: {e}")

    def update_pid_parameters(self):
        """
            Update PID parameters from the GUI and set them in the motor.
            """
        try:
            # Retrieve PID values from GUI inputs
            kp = self.proportional_input.value()
            ki = self.integral_input.value()
            kd = self.derivative_input.value()

            # Set PID parameters in the motor
            self.motor.set_pid_parameters(kp, ki, kd)
            # print(f"Updated PID parameters: Kp={kp}, Ki={ki}, Kd={kd}")

        except Exception as e:
            pass
            # print(f"Error updating PID parameters: {e}")

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
            rpmmax = self.load_rpmmax()
            measured_speed = self.motor.measure_speed(measurement_time=0.1)

            current_time = self.time_data[-1] + 0.1 if self.time_data else 0
            self.time_data.append(current_time)
            self.speed_data.append(measured_speed)

            # Ajouter la valeur du slider (vitesse de consigne) et la valeur de la PWM
            slider_value = self.set_point_slider.value()
            pwm_value = (slider_value / rpmmax) * 255  # Calcul de la PWM

            self.slider_data.append(slider_value)  # Liste pour les valeurs du slider
            self.pwm_data.append(pwm_value)  # Liste pour les valeurs de PWM

            if len(self.time_data) > 100:
                self.time_data = self.time_data[1:]
                self.speed_data = self.speed_data[1:]
                self.slider_data = self.slider_data[1:]
                self.pwm_data = self.pwm_data[1:]

            self.update_motor_speed(slider_value)

            # Ajuster dynamiquement la limite du slider
            self.set_point_slider.setMaximum(rpmmax)

            # Mise à jour du graphique
            self.ax.clear()

            # Tracer la vitesse mesurée
            self.ax.plot(self.time_data, self.speed_data, label="Measured Speed (RPM)", color="blue")

            # Tracer la valeur du slider et la PWM
            self.ax.plot(self.time_data, self.slider_data, label="Set Point (Slider)", color="orange", linestyle="--")
            self.ax.plot(self.time_data, self.pwm_data, label="PWM Value", color="green", linestyle=":")

            self.ax.set_title(f"Motor Speed Over Time (Max: {rpmmax:.2f} RPM)")
            self.ax.set_xlabel("Time (s)")
            self.ax.set_ylabel("Speed / Value")
            self.ax.set_ylim(0,
                             max(self.speed_data + self.slider_data + self.pwm_data) + 1000)  # Ajuste dynamique des limites
            self.ax.legend()
            self.canvas.draw()

            # Mise à jour de l'affichage de la vitesse mesurée
            self.actual_speed_display.setText(f"{measured_speed:.2f} RPM")
            self.pwm_display.setText(f"{pwm_value:.2f}")

        except Exception as e:
            print(f"Erreur lors de la mise à jour du graphique : {e}")

    def update_motor_speed(self, slider_value):
        """Met à jour la vitesse du moteur en fonction de la valeur du slider."""
        rpmmaxmotor = self.rpmmax

        # Vérifier si rmpmax est zéro pour éviter la division par zéro
        if rpmmaxmotor == 0:
            print("Erreur : la vitesse maximale du moteur est égale à zéro.")
            pwm = 0  # Eviter de diviser par zéro
        else:
            pwm = (slider_value / rpmmaxmotor) * 255

        # Vérifier si les paramètres PID sont définis
        if self.proportional_checkbox.isChecked() or self.integral_checkbox.isChecked() or self.derivative_checkbox.isChecked():
            # Appeler la méthode de contrôle du moteur en utilisant PID
            #  print("Utilisation du PID pour la mise à jour du contrôle du moteur.")
            print(pwm)
            self.update_motor_control(pwm)  # Passer la valeur de pwm
        else:
            # Si aucun paramètre PID n'est défini, démarrer le moteur avec la valeur PWM calculée
            # print(f"Pas de PID défini. Démarrage du moteur avec PWM: {pwm}")
            self.motor.start(pwm)

        # Mettre à jour l'affichage de la PWM
        self.pwm_display.setText(f"{pwm:.2f}")

    def closeEvent(self, event):
        print("Programme fermé")
        self.motor.stop()
        self.timer.stop()
