import customtkinter as ctk
from pages import video_page, db_page, collision_page

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("System Monitorowania")
        self.geometry("1000x700")
        ctk.set_appearance_mode("dark")

        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.pack(side="left", fill="y")

        self.container = ctk.CTkFrame(self)
        self.container.pack(side="right", fill="both", expand=True)

        self.pages = {
            "Podgląd wideo": video_page.VideoPage,
            "Baza danych": db_page.DBPage,
            "Wykrywanie kolizji": collision_page.CollisionPage,

        }

        for name in self.pages:
            button = ctk.CTkButton(self.sidebar, text=name, command=lambda n=name: self.show_page(n))
            button.pack(pady=10, padx=10)

        self.current_page = None
        self.show_page("Podgląd wideo")

    def show_page(self, page_name):
        if self.current_page is not None:
            self.current_page.destroy()

        PageClass = self.pages[page_name]
        self.current_page = PageClass(self.container)
        self.current_page.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()
