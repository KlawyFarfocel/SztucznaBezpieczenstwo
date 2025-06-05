import customtkinter as ctk

class CollisionPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        label = ctk.CTkLabel(self, text="Wykrywanie kolizji", font=("Arial", 20))
        label.pack(pady=10)
        labelSm = ctk.CTkLabel(self, text="todo", font=("Arial", 10))
        labelSm.pack(pady=20)

