"""
Modern UI components using CustomTkinter.
"""
import customtkinter as ctk
from PIL import Image
import os
from typing import Callable, Optional

class MascotWidget(ctk.CTkLabel):
    """Weather mascot widget."""
    
    def __init__(self, master, image_path: str, size: tuple = (80, 80), **kwargs):
        if os.path.exists(image_path):
            img = Image.open(image_path)
            img = img.resize(size)
            self.ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=size)
            super().__init__(master, image=self.ctk_img, text="", **kwargs)
        else:
            # Fallback if image not found
            super().__init__(master, text="🌤️", font=("Arial", 40), **kwargs)

class ThemeSwitcher(ctk.CTkFrame):
    """Modern theme switcher using CustomTkinter themes."""
    
    def __init__(self, master, callback: Callable, **kwargs):
        super().__init__(master, **kwargs)
        self.callback = callback
        
        self.theme_var = ctk.StringVar(value="dark")
        self.theme_menu = ctk.CTkOptionMenu(
            self,
            values=["light", "dark", "system"],
            variable=self.theme_var,
            command=self.change_theme
        )
        self.theme_menu.pack(padx=10, pady=10)
    
    def change_theme(self, theme: str):
        """Change application theme."""
        ctk.set_appearance_mode(theme)
        if self.callback:
            self.callback(theme)
