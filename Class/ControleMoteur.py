from telemetrix import telemetrix
import time

# Configuration des broches
MOTOR_PWM_PIN = 3      # Broche PWM pour contrôler la vitesse du moteur
MOTOR_DIR_PIN = 12      # Broche direction pour le sens du moteur
ENCODER_PIN_A = 2      # Broche de signal A de l'encodeur
ENCODER_PIN_B = 7     # Broche de signal B de l'encodeur

# Variables globales pour le comptage des impulsions
encoder_count = 0

def encoder_callback(data):
    """
    Callback pour gérer les interruptions du signal A de l'encodeur.
    """
    global encoder_count
    encoder_count += 1  # Incrémenter le compteur à chaque front montant

def initialize_motor_control(board, pwm_pin, dir_pin):
    """
    Configure les broches pour le contrôle du moteur.
    """
    board.set_pin_mode_digital_output(dir_pin)
    board.set_pin_mode_analog_output(pwm_pin)
    print(f"Broches {pwm_pin} (PWM) et {dir_pin} (Direction) configurées pour le moteur.")

def initialize_encoder(board, pin_a, pin_b):
    """
    Configure les broches pour lire les signaux de l'encodeur.
    """
    board.set_pin_mode_digital_input(pin_a, callback=encoder_callback)
   # board.set_pin_mode_digital_input(pin_b)
    print(f"Broches {pin_a} et {pin_b} configurées pour l'encodeur.")

def start_motor(board, pwm_pin, dir_pin, speed=128):
    """
    Allume le moteur avec une vitesse donnée (0-255).
    """
    board.digital_write(dir_pin, 1)  # Sens du moteur
    board.analog_write(pwm_pin, speed)  # Commande PWM
    print("Moteur démarré à vitesse :", speed)

def stop_motor(board, pwm_pin, dir_pin):
    """
    Éteint le moteur.
    """
    board.analog_write(pwm_pin, 0)
    board.digital_write(dir_pin, 0)
    print("Moteur arrêté.")

def calculate_speed(count, time_interval, ticks_per_revolution=100, wheel_diameter=0.1):
    """
    Calcule la vitesse du moteur.
    - count: nombre d'impulsions
    - time_interval: intervalle de temps en secondes
    - ticks_per_revolution: nombre d'impulsions par tour complet
    - wheel_diameter: diamètre de la roue en mètres (si applicable)
    """
    # Tours par seconde
    revolutions_per_second = count / (ticks_per_revolution * time_interval)
    # Vitesse linéaire (m/s)
    speed = revolutions_per_second * (3.14159 * wheel_diameter)
    return speed

def main():
    """
    Programme principal pour contrôler le moteur et lire les impulsions.
    """
    global encoder_count

    # Initialise la connexion à l'Arduino
    print("Connexion à l'Arduino...")
    board = telemetrix.Telemetrix()

    try:
        # Initialisation des broches
        initialize_motor_control(board, MOTOR_PWM_PIN, MOTOR_DIR_PIN)
        initialize_encoder(board, ENCODER_PIN_A, ENCODER_PIN_B)

        # Commandes utilisateur
        while True:
            command = input("Entrez 'start', 'stop', 'speed', ou 'quit' : ").strip().lower()
            if command == 'start':
                encoder_count = 0  # Réinitialise le compteur
                start_motor(board, MOTOR_PWM_PIN, MOTOR_DIR_PIN, speed=150)
            elif command == 'stop':
                stop_motor(board, MOTOR_PWM_PIN, MOTOR_DIR_PIN)
            elif command == 'speed':
                # Mesure de la vitesse pendant une période
                encoder_count = 0  # Réinitialise le compteur
                time_interval = 1  # Intervalle de mesure (secondes)
                print("Mesure de la vitesse en cours...")
                time.sleep(time_interval)
                speed = calculate_speed(encoder_count, time_interval)
                print(f"Vitesse du moteur : {speed:.2f} m/s")
            elif command == 'quit':
                print("Arrêt du programme.")
                break
            else:
                print("Commande non reconnue. Essayez 'start', 'stop', 'speed', ou 'quit'.")
    finally:
        # Nettoyage et déconnexion
        board.shutdown()
        print("Connexion à l'Arduino terminée.")

if __name__ == "__main__":
    main()