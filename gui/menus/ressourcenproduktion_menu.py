import tkinter as tk

class RessourcenproduktionMenu:
    def __init__(self, parent):
        """Erstellt das Ressourcenproduktion-Menü als Toplevel-Fenster.
        Args:
            parent (tk.Tk | tk.Toplevel): Das Elternfenster, in dem dieses Menü geöffnet wird."""
        self.window = tk.Toplevel(parent)
        self.window.title("Ressourcenproduktion Menu")
        self.window.geometry("300x200")

        # Widgets hinzufügen
        label = tk.Label(self.window, text="Ressourcenproduktion Optionen")
        label.pack(pady=10)

        button1 = tk.Button(self.window, text="Upgrade", command=self.upgrade_dorf)
        button1.pack(pady=5)

        button2 = tk.Button(self.window, text="Close", command=self.window.destroy)
        button2.pack(pady=5)

    def upgrade_dorf(self):
        print("Ressourcenproduktion upgraden!")  # Hier kannst du Logik für Upgrades hinzufügen
