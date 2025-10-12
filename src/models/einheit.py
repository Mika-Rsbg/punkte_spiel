class Einheit:
    def __init__(self, canvas, x, y, dorf, anzahl=10):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.dorf = dorf
        self.anzahl = anzahl
        self.id = self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="green", tags="einheit")
        self.canvas.tag_bind(self.id, "<Button-1>", self.on_click)

    def on_click(self, event=None):
        # Hier können wir die Logik zum Verschieben oder Angreifen der Einheiten einfügen
        if self.dorf.is_computer:
            messagebox.showinfo("Einheit", f"Einheit aus dem {self.dorf.name} ausgewählt.")
        else:
            messagebox.showinfo("Einheit", f"Spielereinheit aus {self.dorf.name} ausgewählt.")

    def verschieben(self, neues_dorf):
        # Verschiebt das Heer von einem Dorf zu einem anderen
        self.dorf = neues_dorf
        self.x = neues_dorf.x
        self.y = neues_dorf.y
        self.canvas.coords(self.id, self.x - 10, self.y - 10, self.x + 10, self.y + 10)