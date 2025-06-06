import os
import duckdb
from dotenv import load_dotenv

# Załaduj zmienne środowiskowe
load_dotenv()
db_path = os.getenv("DATABASE_PATH1")

if db_path is None:
    raise ValueError("Brak wartości DATABASE_PATH w pliku .env!")

# Tworzenie katalogu, jeśli nie istnieje
db_dir = os.path.dirname(db_path)
if not os.path.exists(db_dir):
    os.makedirs(db_dir)
    print(f"Utworzono katalog: {db_dir}")

print(f"Ścieżka do bazy danych: {db_path}")

# Połączenie z bazą danych
conn = duckdb.connect(db_path)

# Tworzenie tabeli, jeśli nie istnieje
conn.execute("""
CREATE TABLE IF NOT EXISTS vehicles (
    id TEXT PRIMARY KEY,
    license_plate TEXT,
    vehicle_brand TEXT,
    color TEXT
)
""")

# =====================
# FUNKCJE OPERACYJNE
# =====================
def filter_records_flexible():
    print("Zostaw puste pole, jeśli nie chcesz filtrować po danej wartości.")
    license_plate = input("Numer rejestracyjny: ").strip().upper()
    vehicle_brand = input("Marka pojazdu: ").strip().upper()
    color = input("Kolor pojazdu: ").strip().upper()

    query = "SELECT * FROM vehicles WHERE 1=1"
    params = []

    if license_plate:
        query += " AND UPPER(license_plate) ILIKE ?"
        params.append(f"%{license_plate}%")
    if vehicle_brand:
        query += " AND UPPER(vehicle_brand) = ?"
        params.append(vehicle_brand)
    if color:
        query += " AND UPPER(color) = ?"
        params.append(color)

    rows = conn.execute(query, params).fetchall()

    print("\n--- Wyniki wyszukiwania ---")
    if rows:
        for row in rows:
            print(row)
    else:
        print("Brak pasujących rekordów.")
def show_records_segmented(limit=5, offset=0):
    rows = conn.execute("SELECT * FROM vehicles LIMIT ? OFFSET ?", (limit, offset)).fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("Brak kolejnych rekordów.")

def filter_records_by_color(color):
    rows = conn.execute("SELECT * FROM vehicles WHERE color = ?", (color,)).fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print(f"Brak pojazdów w kolorze {color}.")

def delete_record_by_id(record_id):
    conn.execute("DELETE FROM vehicles WHERE id = ?", (record_id,))
    print(f"Usunięto rekord o ID: {record_id}")

# =====================
# MENU
# =====================

def menu():
    while True:
        print("\n--- MENU ---")
        print("1. Wyświetl rekordy (segmentowane)")
        print("2. Filtruj rekordy")
        print("3. Usuń rekord po ID")
        print("4. Wyjście")
        choice = input("Wybierz opcję: ")

        if choice == "1":
            try:
                limit = int(input("Ile rekordów na stronę? "))
                offset = int(input("Offset (początkowy rekord)? "))
                show_records_segmented(limit, offset)
            except ValueError:
                print("Błąd: podano nieprawidłowe wartości liczbowe.")
        elif choice == "2":
            filter_records_flexible()
        elif choice == "3":
            record_id = input("Podaj ID rekordu do usunięcia: ")
            delete_record_by_id(record_id)
        elif choice == "4":
            break
        else:
            print("Nieprawidłowy wybór.")

# Uruchom menu
menu()

# Zamknięcie połączenia
conn.close()
print("Zamknięto połączenie z bazą danych.")