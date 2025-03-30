import os
import duckdb
from dotenv import load_dotenv

load_dotenv()
db_path = os.getenv("DATABASE_PATH")

if db_path is None:
    raise ValueError("Brak wartości DATABASE_PATH w pliku .env!")

# Tworzymy katalog, jeśli nie istnieje
db_dir = os.path.dirname(db_path)
if not os.path.exists(db_dir):
    os.makedirs(db_dir)
    print(f"Utworzono katalog: {db_dir}")

print(f"Ścieżka do bazy danych: {db_path}")

# Usuwamy plik, jeśli istnieje
#if os.path.exists(db_path):
#    os.remove(db_path)
#   print("Usunięto uszkodzony plik.")

# Tworzymy nową bazę
conn = duckdb.connect(db_path)
# Krok 3: Odczyt wszystkich rekordów
conn.execute("""
CREATE TABLE IF NOT EXISTS vehicles (
    id TEXT PRIMARY KEY,
    license_plate TEXT,
    vehicle_type TEXT,
    vehicle_brand TEXT,
    color TEXT
)
""")

rows = conn.execute("SELECT * FROM vehicles").fetchall()

# Wyświetlenie wyników
for row in rows:
    print(row)

# Zamknięcie połączenia

conn.close()
print("Baza danych została ponownie utworzona.")
