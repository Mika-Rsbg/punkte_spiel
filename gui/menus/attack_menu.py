import tkinter as tk

class AttackMenu:
    def __init__(self, parent):
        """Erstellt das Attack-Menu als Toplevel-Fenster.
        Args:
            parent (tk.Tk | tk.Toplevel): Das Elternfenster, in dem dieses Menü geöffnet wird."""
        self.window = tk.Toplevel(parent)
        self.window.title("Attack Menu")
        self.window.geometry("300x200")

        # Widgets hinzufügen
        label = tk.Label(self.window, text="Attack Options")
        label.pack(pady=10)

        button1 = tk.Button(self.window, text="Build Dorf", command=self.build_dorf)
        button1.pack(pady=5)

        button2 = tk.Button(self.window, text="Close", command=self.window.destroy)
        button2.pack(pady=5)

    def build_dorf(self):
        print("Dorf bauen!")  # Hier kannst du Logik für den Bau hinzufügen