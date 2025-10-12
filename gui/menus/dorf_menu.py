import tkinter as tk
import config

import utils.canvas_utils as canvas_utils

class DorfMenu:
    def __init__(self, parent):
        """
        Erstellt das Dorf-Menü als Toplevel-Fenster.
        Args:
            parent (tk.Tk | tk.Toplevel): Das Elternfenster, in dem dieses Menü geöffnet wird.
        """
        self.window = tk.Toplevel(parent)
        self.window.title("Dorf Menu")
        self.window.geometry("300x200")

        # Widgets hinzufügen
        label = tk.Label(self.window, text="Dorf Optionen")
        label.pack(pady=10)

        button1 = tk.Button(self.window, text="Upgrade", command=self.upgrade_dorf)
        button1.pack(pady=5)

        button2 = tk.Button(self.window, text="Close", command=self.close_window)
        button2.pack(pady=5)

    def upgrade_dorf(self):
        print("Dorf upgraden!")  # Hier kannst du Logik für Upgrades hinzufügen

    def close_window(self):
        self.window.destroy()
        canvas_utils.clear_field(config.GameCanvas.canvas, field_coords=config.GameCanvas.selected_field)
        config.GameCanvas.is_field_selected = False
        config.GameCanvas.selected_field = None
