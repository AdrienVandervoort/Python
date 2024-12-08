from telemetrix import telemetrix
import time
import os

max=True


class Motor:
    def __init__(self, board, pwm_pin, dir_pin, encoder_pin_a, encoder_pin_b, ticks_per_revolution=12):
        self.last_n_rpm = []
        self.board = board
        self.pwm_pin = pwm_pin
        self.dir_pin = dir_pin
        self.encoder_pin_a = encoder_pin_a
        self.encoder_pin_b = encoder_pin_b
        self.ticks_per_revolution = ticks_per_revolution
        self.encoder_count = 0

        self.board.set_pin_mode_digital_output(dir_pin)
        self.board.set_pin_mode_analog_output(pwm_pin)
        self.board.set_pin_mode_digital_input(encoder_pin_a, callback=self.encoder_callback)

        print(f"Moteur initialisé avec PWM={pwm_pin}, DIR={dir_pin}, Encoder A={encoder_pin_a}, B={encoder_pin_b}")

    def encoder_callback(self, data):
        self.encoder_count += 0.5

    def start(self, speed=255):
        if 0 <= speed <= 255:
            self.board.digital_write(self.dir_pin, 1)
            self.board.analog_write(self.pwm_pin, speed)
            print(f"Moteur démarré à vitesse : {speed}")
        else:
            print("Erreur : La vitesse doit être entre 0 et 255.")

    def stop(self):
        self.board.analog_write(self.pwm_pin, 0)
        self.board.digital_write(self.dir_pin, 0)
        print("Moteur arrêté.")

    def measure_speed(self, measurement_time=0.5):
        print(f"Mesure de la vitesse pendant {measurement_time} seconde(s)...")
        self.encoder_count = 0
        time.sleep(measurement_time)
        impulsions = self.encoder_count
        rpm = self.calculate_speed(impulsions, measurement_time)

        self.last_n_rpm.append(rpm)
        if len(self.last_n_rpm) > 10:
            self.last_n_rpm.pop(0)

        print("Dernières 10 vitesses mesurées (RPM) :")
        print(", ".join(f"{value:.2f}" for value in self.last_n_rpm))

        # Calcul de la moyenne des dernières vitesses
        moy_rpm = sum(self.last_n_rpm) / len(self.last_n_rpm)

        print(f"Nombre d'impulsions : {impulsions}")
        print(f"Vitesse moyenne : {moy_rpm:.2f} RPM")

        return rpm

    def calculate_speed(self, impulsions, time_interval):
        if time_interval <= 0 or self.ticks_per_revolution <= 0:
            print("Erreur : Intervalle de temps ou ticks par tour invalide.")
            return 0

        tours = impulsions / self.ticks_per_revolution
        rpm = (tours / time_interval) * 60
        return rpm


def main():
    print("Connexion à l'Arduino...")
    board = telemetrix.Telemetrix()

    try:
        motor = Motor(
            board=board,
            pwm_pin=3,
            dir_pin=12,
            encoder_pin_a=2,
            encoder_pin_b=7,
            ticks_per_revolution=12
        )

        speed = int(input("Entrez la vitesse du moteur (0-255) : "))
        motor.start(speed=speed)

        rpm_values = []
        start_time = time.time()

        while time.time() - start_time < 10:
            rpm = motor.measure_speed(measurement_time=1)
            rpm_values.append(rpm)
            print(f"RPM mesuré : {rpm:.2f}")

        motor.stop()

        # Calculer la moyenne des valeurs entre 2 et 8 secondes
        filtered_values = rpm_values[2:8]  # Sélectionner les éléments entre 2s et 8s
        if filtered_values:
            average_rpm = sum(filtered_values) / len(filtered_values)
            print(f"Valeurs mesurées : {rpm_values}")
            print(f"Moyenne des RPM entre 2 et 8 secondes : {average_rpm:.2f}")

            # Enregistrer la moyenne dans un fichier sur le bureau
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            file_path = os.path.join(desktop, "rpm_average.dat")
            with open(file_path, "w") as file:
                file.write(f"Moyenne des RPM entre 2 et 8 secondes : {average_rpm:.2f}\n")
            print(f"Moyenne enregistrée dans le fichier : {file_path}")

        else:
            print("Pas de données suffisantes pour calculer la moyenne.")

    finally:
        board.shutdown()
        print("Connexion à l'Arduino terminée.")


if __name__ == "__main__":
    main()
