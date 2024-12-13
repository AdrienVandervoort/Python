import os
import time


class Motor:
    def __init__(self, board, pwm_pin, dir_pin, encoder_pin_a, encoder_pin_b, ticks_per_revolution):
        """
        Initialise le moteur avec les broches et les paramètres nécessaires.
        """
        self.board = board
        self.pwm_pin = pwm_pin
        self.dir_pin = dir_pin
        self.encoder_pin_a = encoder_pin_a
        self.encoder_pin_b = encoder_pin_b
        self.ticks_per_revolution = ticks_per_revolution
        self.encoder_count = 0
        self.rmpmax = 0  # Initialise la vitesse maximale enregistrée
        self.last_n_rpm = []  # Liste pour stocker les dernières vitesses mesurées
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        # Initialisation des broches
        self.board.set_pin_mode_digital_output(dir_pin)
        self.board.set_pin_mode_analog_output(pwm_pin)
        self.board.set_pin_mode_digital_input(encoder_pin_a, callback=self.encoder_callback)

        # PID parameters
        self.kp = 0.0
        self.ki = 0.0
        self.kd = 0.0

        # PID state variables
        self.previous_error = 0.0
        self.integral = 0.0

    # print(f"Moteur initialisé avec PWM={pwm_pin}, DIR={dir_pin}, Encoder A={encoder_pin_a}, B={encoder_pin_b}")

    def encoder_callback(self, data):
        """
        Callback pour gérer les interruptions du signal A de l'encodeur.
        """
        # Compte uniquement les fronts montants
        self.encoder_count += 0.5

    def start(self, speed):
        """
        Démarre le moteur avec une vitesse donnée.
        """
        if 0 <= speed <= 255:
            self.board.digital_write(self.dir_pin, 1)
            self.board.analog_write(self.pwm_pin, int(speed))
        #  print(f"Moteur démarré à vitesse : {speed}")

        else:
            print("Erreur : La vitesse doit être entre 0 et 255.")

    def stop(self):
        """
        Arrête le moteur.
        """
        self.board.analog_write(self.pwm_pin, 0)
        self.board.digital_write(self.dir_pin, 0)
        print("Moteur arrêté.")

    def set_pid_parameters(self, kp, ki, kd):
        """Set the PID coefficients."""
        self.kp = kp
        self.ki = ki
        self.kd = kd

    def pid_control(self, set_point, actual_speed, dt=1):
        """
        Perform PID control calculation.

        :param set_point: Desired speed (RPM)
        :param actual_speed: Measured speed (RPM)
        :param dt: Time difference in seconds
        :return: PWM output (0 to 255)
        """
        # Calculate error

        # error = abs(actual_speed - set_point)
        error = (set_point - actual_speed)
        print(self.previous_error, "erreur prec", error, "erreur actuelle")

        # Proportional term
        proportional = self.kp * error

        # Integral term
        self.integral += error * dt
        integral = self.ki * self.integral

        # Derivative term
        derivative = self.kd * (error - self.previous_error) / dt

        # PID output
        output = proportional + integral + derivative

        # Clamp output to valid PWM range (0 to 255)
        output = max(0, min(255, output))
        print(output, "output")

        # Save the current error for the next derivative calculation
        self.previous_error = error

        # print(f"PID Control: SetPoint={set_point}, Actual={actual_speed}, Output={output}")
        return output

    def measure_speed(self, measurement_time):
        """
        Mesure la vitesse du moteur (RPM) sur une durée donnée.
        """
        # print(f"Mesure de la vitesse pendant {measurement_time} seconde(s)...")
        self.encoder_count = 0
        time.sleep(measurement_time)
        impulsions = self.encoder_count
        rpm = self.calculate_speed(impulsions, measurement_time)

        # Ajoute la vitesse mesurée à la liste et conserve les 10 dernières valeurs
        self.last_n_rpm.append(rpm)
        if len(self.last_n_rpm) > 10:
            self.last_n_rpm.pop(0)

        # print("Dernières 10 vitesses mesurées (RPM) :")
        # print(", ".join(f"{value:.2f}" for value in self.last_n_rpm))

        # Calcul de la moyenne des dernières vitesses
        moy_rpm = sum(self.last_n_rpm) / len(self.last_n_rpm)

        #  print(f"Nombre d'impulsions : {impulsions}")
        # print(f"Vitesse moyenne : {moy_rpm:.2f} RPM")
        return moy_rpm

    def calculate_speed(self, impulsions, time_interval):
        """
        Calcule la vitesse en tours par minute (RPM).
        """
        if time_interval <= 0 or self.ticks_per_revolution <= 0:
            print("Erreur : Intervalle de temps ou ticks par tour invalide.")
            return 0

        tours = impulsions / self.ticks_per_revolution
        rpm = (tours / time_interval) * 60
        return rpm
