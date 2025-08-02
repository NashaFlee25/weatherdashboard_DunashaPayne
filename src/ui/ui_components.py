"""
Reusable UI components: theme switcher, mascot, custom widgets.
"""
import customtkinter as ctk
import ttkbootstrap as ttk
from PIL import Image, ImageTk
import os

class MascotWidget(ctk.CTkLabel):
    def __init__(self, master, image_path, **kwargs):
        img = Image.open(image_path)
        img = img.resize((80, 80))
        self.ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(80, 80))
        super().__init__(master, image=self.ctk_img, text="", **kwargs)

class ThemeSwitcher(ctk.CTkFrame):
    def __init__(self, master, callback, **kwargs):
        super().__init__(master, **kwargs)
        self.callback = callback
        self.switch = ctk.CTkSwitch(self, text="Day/Night Theme", command=self.toggle)
        self.switch.pack(padx=10, pady=10)

    def toggle(self):
        self.callback(self.switch.get())
