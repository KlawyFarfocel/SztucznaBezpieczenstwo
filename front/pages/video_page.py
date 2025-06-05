import customtkinter as ctk
from customtkinter import CTkImage
import threading
from PIL import Image, ImageTk
import sys
import os
import asyncio
import nest_asyncio
nest_asyncio.apply()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from main import process_and_show



class VideoPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.max_width = 960
        self.max_height = 540

        self.video_label = ctk.CTkLabel(self, text="")
        self.video_label.pack(pady=10)

        self.status_label = ctk.CTkLabel(self, text="", font=("Arial", 14))
        self.status_label.pack(pady=5)

        self.start_button = ctk.CTkButton(self, text="Start video", command=self.start_video)
        self.start_button.pack(pady=10)

        self.loop = asyncio.new_event_loop()
        self.thread = None
        self.running = False

    def start_video(self):
        if self.thread and self.thread.is_alive():
            return

        self.status_label.configure(text="Wczytywanie wideo...")
        self.running = True
        self.thread = threading.Thread(target=self.run_async_loop, daemon=True)
        self.thread.start()

    def run_async_loop(self):
        asyncio.set_event_loop(self.loop)
        try:
            self.loop.run_until_complete(self.controlled_process_and_show())
        except Exception as e:
            self.after(0, self.status_label.configure, {"text": f"Błąd: {e}"})
        finally:
            self.thread = None 

    async def controlled_process_and_show(self):
        await process_and_show(self.receive_frame, should_continue=lambda: self.running)
        self.after(0, self.on_stream_end)

    def receive_frame(self, frame_rgb):
        if not self.running:
            return

        img = Image.fromarray(frame_rgb)
        img.thumbnail((self.max_width, self.max_height), Image.LANCZOS)
        self.after(0, self.update_image, img)

    def update_image(self, imgtk):
        ctk_img = CTkImage(light_image=imgtk, size=imgtk.size)
        self.video_label.configure(image=ctk_img)
        self.video_label.image = ctk_img
        self.status_label.configure(text="") 
    def on_stream_end(self):
        if self.running:
            self.status_label.configure(text="Wideo zakończone lub brak sygnału.")
        self.running = False
        self.thread = None

    def destroy(self):
        self.running = False
        super().destroy()
