#!/usr/bin/env python3
import sqlite3
import datetime
import smtplib
import os
from email.message import EmailMessage
from config import DATABASE_FILE, NOTIFICATION_DAYS, EMAIL_CONFIG, TEST_MODE

def create_database_if_not_exists():
    """Tworzy bazę danych jeśli nie istnieje i wykonuje skrypt db_setup.sql"""
    db_exists = os.path.exists(DATABASE_FILE)
    
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    if not db_exists:
        print(f"Tworzenie nowej bazy danych: {DATABASE_FILE}")
        with open('db_setup.sql', 'r') as f:
            sql_script = f.read()
            cursor.executescript(sql_script)
            conn.commit()
            print("Baza danych została utworzona i wypełniona przykładowymi danymi.")
    
    conn.close()

def check_technical_inspection():
    """Sprawdza samochody, którym kończy się badanie techniczne"""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    today = datetime.date.today()
    cars_to_notify = []
    
    for days in NOTIFICATION_DAYS:
        check_date = today + datetime.timedelta(days=days)
        
        cursor.execute("""
            SELECT * FROM cars 
            WHERE date(technical_inspection_date) = date(?)
        """, (check_date,))
        
        for car in cursor.fetchall():
            cars_to_notify.append({
                'registration_number': car['registration_number'],
                'brand': car['brand'],
                'model': car['model'],
                'days_left': days,
                'expiry_date': car['technical_inspection_date'],
                'expiry_type': 'badanie techniczne',
                'contact_person': car['contact_person'],
                'contact_email': car['contact_email']
            })
    
    conn.close()
    return cars_to_notify

def check_insurance():
    """Sprawdza samochody, którym kończy się ubezpieczenie OC"""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    today = datetime.date.today()
    cars_to_notify = []
    
    for days in NOTIFICATION_DAYS:
        check_date = today + datetime.timedelta(days=days)
        
        cursor.execute("""
            SELECT * FROM cars 
            WHERE date(insurance_date) = date(?)
        """, (check_date,))
        
        for car in cursor.fetchall():
            cars_to_notify.append({
                'registration_number': car['registration_number'],
                'brand': car['brand'],
                'model': car['model'],
                'days_left': days,
                'expiry_date': car['insurance_date'],
                'expiry_type': 'ubezpieczenie OC',
                'contact_person': car['contact_person'],
                'contact_email': car['contact_email']
            })
    
    conn.close()
    return cars_to_notify

def send_email_notification(car_info):
    """Wysyła powiadomienie email o kończącym się badaniu technicznym lub ubezpieczeniu OC"""
    if not EMAIL_CONFIG['enabled']:
        return False
    
    subject = f"POWIADOMIENIE: {car_info['expiry_type']} pojazdu {car_info['registration_number']} wygasa za {car_info['days_left']} dni"
    
    body = f"""
    Witaj {car_info['contact_person']},
    
    Informujemy, że {car_info['expiry_type']} dla pojazdu:
    - Numer rejestracyjny: {car_info['registration_number']}
    - Marka i model: {car_info['brand']} {car_info['model']}
    
    wygasa za {car_info['days_left']} dni (w dniu {car_info['expiry_date']}).
    
    Prosimy o podjęcie odpowiednich działań.
    
    Pozdrawiamy,
    System zarządzania flotą
    """
    
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_CONFIG['sender_email']
    msg['To'] = car_info['contact_email']
    
    try:
        with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
            server.starttls()
            server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Błąd podczas wysyłania emaila: {e}")
        return False

def display_console_notification(car_info):
    """Wyświetla powiadomienie w konsoli (tryb testowy)"""
    print("=" * 50)
    print(f"POWIADOMIENIE: {car_info['expiry_type']} pojazdu {car_info['registration_number']} wygasa za {car_info['days_left']} dni")
    print(f"Data wygaśnięcia: {car_info['expiry_date']}")
    print(f"Pojazd: {car_info['brand']} {car_info['model']}")
    print(f"Osoba kontaktowa: {car_info['contact_person']} ({car_info['contact_email']})")
    print("=" * 50)
    print()

def send_notifications(cars_to_notify):
    """Wysyła wszystkie powiadomienia"""
    for car_info in cars_to_notify:
        if TEST_MODE:
            display_console_notification(car_info)
        else:
            success = send_email_notification(car_info)
            if success:
                print(f"Wysłano powiadomienie do {car_info['contact_email']} o pojeździe {car_info['registration_number']}")
            else:
                print(f"Nie udało się wysłać powiadomienia do {car_info['contact_email']}")

def main():
    """Główna funkcja programu"""
    print("Uruchamianie systemu zarządzania flotą aut...")
    create_database_if_not_exists()
    
    # Sprawdzenie badań technicznych
    print("Sprawdzanie terminów badań technicznych...")
    technical_inspections = check_technical_inspection()
    
    # Sprawdzenie ubezpieczeń OC
    print("Sprawdzanie terminów ubezpieczeń OC...")
    insurances = check_insurance()
    
    # Łączenie wyników
    all_notifications = technical_inspections + insurances
    
    # Wysyłanie powiadomień
    if all_notifications:
        print(f"Znaleziono {len(all_notifications)} powiadomień do wysłania.")
        send_notifications(all_notifications)
    else:
        print("Nie znaleziono żadnych powiadomień do wysłania.")

if __name__ == "__main__":
    main()
