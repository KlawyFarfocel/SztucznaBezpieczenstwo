import customtkinter as ctk
import duckdb
import os
from tkinter import ttk

db_path = os.getenv("DATABASE_PATH1")

class DBPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        ctk.CTkLabel(self, text="Baza danych pojazdów", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(10, 5))

        self.entry_plate = ctk.CTkEntry(self, placeholder_text="Numer rejestracyjny")
        self.entry_plate.pack(fill="x", padx=20)

        self.entry_brand = ctk.CTkEntry(self, placeholder_text="Marka")
        self.entry_brand.pack(fill="x", padx=20, pady=5)

        self.entry_color = ctk.CTkEntry(self, placeholder_text="Kolor")
        self.entry_color.pack(fill="x", padx=20)

        ctk.CTkButton(self, text="Filtruj", command=self.load_data).pack(pady=10)

        self.tree_frame = ctk.CTkFrame(self)
        self.tree_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        self.columns = ("id", "license_plate", "vehicle_brand", "color")
        self.tree = ttk.Treeview(self.tree_frame, columns=self.columns, show="headings")

        self.col_widths = [250, 150, 150, 150]
        self.headers = ["ID", "Numer rejestracyjny", "Marka", "Kolor"]

        for col, width, header in zip(self.columns, self.col_widths, self.headers):
            self.tree.heading(col, text=header)
            self.tree.column(col, width=width, anchor="center", stretch=False)

        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<Double-1>", self.copy_selected_to_clipboard)

        ctk.CTkButton(self, text="Kopiuj zaznaczony rekord", command=self.copy_selected_to_clipboard).pack(pady=(0, 10))

        self.copy_status_label = None

        self.load_data()

    def load_data(self):
        conn = duckdb.connect(db_path)

        for row in self.tree.get_children():
            self.tree.delete(row)

        query = "SELECT id, license_plate, vehicle_brand, color FROM vehicles WHERE 1=1"
        params = []

        if plate := self.entry_plate.get().strip():
            query += " AND UPPER(license_plate) ILIKE ?"
            params.append(f"%{plate.upper()}%")

        if brand := self.entry_brand.get().strip():
            query += " AND UPPER(vehicle_brand) = ?"
            params.append(brand.upper())

        if color := self.entry_color.get().strip():
            query += " AND UPPER(color) = ?"
            params.append(color.upper())

        rows = conn.execute(query, params).fetchall()
        for row in rows:
            self.tree.insert("", "end", values=row)

        conn.close()

    def copy_selected_to_clipboard(self, event=None):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], "values")
            formatted = "\t".join(map(str, values))
            self.clipboard_clear()
            self.clipboard_append(formatted)
            self.update()

            if self.copy_status_label:
                self.copy_status_label.destroy()

            self.copy_status_label = ctk.CTkLabel(self, text="Rekord skopiowany do schowka!", text_color="green")
            self.copy_status_label.pack()
            self.after(2000, self.copy_status_label.destroy)
