import duckdb

# Połączenie z bazą danych (jeśli plik nie istnieje, zostanie utworzony)
conn = duckdb.connect("vehicles.db")

# Krok 1: Tworzenie tabeli
conn.execute("""
CREATE TABLE IF NOT EXISTS vehicles (
    id INTEGER PRIMARY KEY,
    license_plate TEXT,
    vehicle_type TEXT,
    color TEXT
)
""")

# Krok 2: Generowanie id i dodanie rekordu
# Pobierz najwyższe id w tabeli i zwiększ je o 1
max_id = conn.execute("SELECT COALESCE(MAX(id), 0) FROM vehicles").fetchone()[0]

# Dodanie rekordu z nowym id
conn.execute("""
INSERT INTO vehicles (id, license_plate, vehicle_type, color)
VALUES (?, ?, ?, ?)
""", (max_id + 1, 'ABC123', 'SUV', 'Czarny'))

# Krok 3: Odczyt wszystkich rekordów
rows = conn.execute("SELECT * FROM vehicles").fetchall()

# Wyświetlenie wyników
for row in rows:
    print(row)

# Zamknięcie połączenia
conn.close()
