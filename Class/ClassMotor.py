from telemetrix import telemetrix
import time

class Motor:
    def __init__(self, board, pwm_pin, dir_pin, encoder_pin_a, encoder_pin_b, ticks_per_revolution=12):
        """
        Initialise le moteur avec les broches et les paramètres nécessaires.
        
        Args:
            board: Instance de Telemetrix.
            pwm_pin: Broche PWM pour la vitesse.
            dir_pin: Broche direction.
            encoder_pin_a: Broche A de l'encodeur.
            encoder_pin_b: Broche B de l'encodeur (optionnel pour ce cas).
            ticks_per_revolution: Nombre de ticks pour un tour complet.
        """
        self.board = board
        self.pwm_pin = pwm_pin
        self.dir_pin = dir_pin
        self.encoder_pin_a = encoder_pin_a
        self.encoder_pin_b = encoder_pin_b
        self.ticks_per_revolution = ticks_per_revolution
        self.encoder_count = 0

        # Initialisation des broches
        self.board.set_pin_mode_digital_output(dir_pin)
        self.board.set_pin_mode_analog_output(pwm_pin)
        self.board.set_pin_mode_digital_input(encoder_pin_a, callback=self.encoder_callback)
        
        print(f"Moteur initialisé avec PWM={pwm_pin}, DIR={dir_pin}, Encoder A={encoder_pin_a}, B={encoder_pin_b}")

    def encoder_callback(self, data):
        """
        Callback pour gérer les interruptions du signal A de l'encodeur.
        """
        self.encoder_count += 0.5  # Incrementer selon les fronts détectés , il faut uniquement compter les fronts montants donc +0.5 par front

    def start(self, speed=255):
        """
        Démarre le moteur avec une vitesse donnée.
        """
        if 0 <= speed <= 255:
            self.board.digital_write(self.dir_pin, 1)
            self.board.analog_write(self.pwm_pin, speed)
            print(f"Moteur démarré à vitesse : {speed}")
        else:
            print("Erreur : La vitesse doit être entre 0 et 255.")

    def stop(self):
        """
        Arrête le moteur.
        """
        self.board.analog_write(self.pwm_pin, 0)
        self.board.digital_write(self.dir_pin, 0)
        print("Moteur arrêté.")

    def measure_speed(self, measurement_time=1):
        """
        Mesure la vitesse du moteur (RPM) sur une durée donnée.
        
        Args:
            measurement_time: Durée de la mesure en secondes.
        
        Returns:
            La vitesse calculée en RPM.
        """
        print(f"Mesure de la vitesse pendant {measurement_time} seconde(s)...")
        self.encoder_count = 0
        time.sleep(measurement_time)
        impulsions = self.encoder_count
        rpm = self.calculate_speed(impulsions, measurement_time)
        print(f"Nombre d'impulsions : {impulsions}")
        print(f"Vitesse calculée : {rpm:.2f} RPM")
        return rpm

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