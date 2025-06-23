# Konfiguracja bazy danych
DATABASE_FILE = 'car_fleet.db'

# Konfiguracja terminów powiadomień (w dniach)
NOTIFICATION_DAYS = [30, 7, 3]

# Konfiguracja powiadomień email (przykładowe dane)
EMAIL_CONFIG = {
    'enabled': False,  # Zmień na True, aby włączyć wysyłanie emaili
    'smtp_server': 'smtp.example.com',
    'smtp_port': 587,
    'sender_email': 'system@example.com',
    'sender_password': 'password'
}

# Tryb testowy - wyświetla powiadomienia w konsoli zamiast wysyłania ich
TEST_MODE = True
