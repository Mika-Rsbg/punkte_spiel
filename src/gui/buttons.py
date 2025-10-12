import tkinter as tk

class ButtonPanel:
    def __init__(self, root):
        self.street_mode_confirm_btn = None
        self.street_mode_cancel_btn = None
        self.end_round_btn = None
        self.end_turn_btn = None
        self.root = root
    
    def create_buttons(self, on_end_turn, on_end_round):
        """Erstellt button-widgets und platziert sie auf der GUI.

        Args:
            on_end_turn (method): Wird ausgeführt, wenn `end_turn button` geklickt wird.
            on_end_round (method): Wird ausgeführt, wenn `end_round button` geklickt wird.
        """
        self.end_turn_btn = tk.Button(self.root, text="Zug beenden", command=on_end_turn)
        self.end_turn_btn.grid(row=1, column=0)
        self.end_round_btn = tk.Button(self.root, text="Runde beenden", command=on_end_round)
        self.end_round_btn.grid(row=1, column=1)

    def create_street_placing_mode_buttons(self, on_cancel, on_confirm):
        self.street_mode_cancel_btn = tk.Button(self.root, text="Cancel", command=on_cancel)
        self.street_mode_cancel_btn.grid(row=2, column=0)
        self.street_mode_confirm_btn = tk.Button(self.root, text="Bestätigen", command=on_confirm)
        self.street_mode_confirm_btn.grid(row=2, column=1)

    def remove_street_placing_mode_buttons(self):
        self.street_mode_cancel_btn.grid_remove()
        self.street_mode_confirm_btn.grid_remove()
