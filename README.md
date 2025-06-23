# Flota Aut Manager

Prosty system do zarządzania flotą samochodową, który:
1. Przechowuje informacje o autach, badaniach technicznych i ubezpieczeniach OC
2. Sprawdza, którym samochodom kończą się badania techniczne
3. Sprawdza, którym samochodom kończy się ubezpieczenie OC
4. Wysyła powiadomienia do wskazanych osób na miesiąc, 7 dni i 3 dni przed wygaśnięciem

## Struktura projektu
- `db_setup.sql` - skrypt tworzący bazę danych
- `app.py` - główny skrypt aplikacji
- `config.py` - plik konfiguracyjny z danymi testowymi

## Jak uruchomić
1. Skonfiguruj bazę danych używając `db_setup.sql`
2. Dostosuj dane w `config.py`
3. Uruchom `app.py`

## Technologie
- Python
- SQLite
