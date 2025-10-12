import tkinter as tk
import config

class ResourceLabel:
    def __init__(self, root):
        self.label1 = tk.Label(root, text=f"Ressourcen Spieler 1: {config.Player.Player1.ressources}")
        self.label1.grid(row=1, column=2, sticky="w")
        self.label2 = tk.Label(root, text=f"Ressourcen Spieler 2: {config.Player.Player2.ressources}")
        self.label2.grid(row=2, column=2, sticky="w")

    def update(self):
        """Aktualisiert die Anzeige der Ressourcen"""
        self.label1.config(text=f"Ressourcen Spieler 1: {config.Player.Player1.ressources}")
        self.label2.config(text=f"Ressourcen Spieler 2: {config.Player.Player2.ressources}")