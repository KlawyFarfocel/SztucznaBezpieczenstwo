import customtkinter as ctk
import duckdb
import os

db_path = os.getenv("DATABASE_PATH1")
class DBPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        label = ctk.CTkLabel(self, text="Baza danych", font=("Arial", 20))
        label.pack(pady=10)
        self.start_button = ctk.CTkButton(self, text="Open DuckDB UI", command=self.open_duckdb)
        self.start_button.pack(pady=10)

    def open_duckdb(self):
        db_path = os.getenv("DATABASE_PATH1")
        conn = duckdb.connect(db_path)
        conn.sql("CALL start_ui()")

