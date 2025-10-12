import tkinter as tk
from tkinter import messagebox
import random

class Ressourcenproduktion:
    def __init__(self, canvas, x, y, is_computer):
        self.canvas = canvas
        self.x = x
        self.y = y
        if is_computer:
            self.id = self.canvas.create_rectangle(x - 10, y - 10, x + 10, y + 10, fill="yellow", tags="ressource")
        else:
            self.id = self.canvas.create_rectangle(x - 10, y - 10, x + 10, y + 10, fill="blue", tags="ressource")

class Dorf:
    def __init__(self, canvas, x, y, name, is_computer=False):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.name = name
        self.radius = 10
        self.color = "yellow" if is_computer else "blue"
        self.angreifen = False
        self.is_computer = is_computer
        self.einheiten = []  # Liste für die Einheiten im Dorf
        
        # Zeichne das Dorf als Kreis auf dem Spielfeld
        self.id = self.canvas.create_oval(x - self.radius, y - self.radius,
                                          x + self.radius, y + self.radius,
                                          fill=self.color, tags="dorf")
        self.canvas.tag_bind(self.id, "<Button-1>", self.on_click)

    def on_click(self, event=None):
        if spiel.kampfmodus_aktiviert.get():
            for einheit in self.einheiten:
                einheit.verschieben(spiel.ziel_dorf)  # Einheiten ins Ziel-Dorf verschieben
                break
        if not self.is_computer:  # Spielerdorf wird angreifendes Dorf
            spiel.angriffs_dorf = self
        else:  # Computerdorf wird Ziel-Dorf
            spiel.ziel_dorf = self
        # Färbt das ausgewählte Dorf ein, um anzuzeigen, dass es markiert wurde
        if not self.angreifen:
            self.angreifen = True
            self.canvas.itemconfig(self.id, outline="yellow", width=2)
        else:
            self.angreifen = False
            self.canvas.itemconfig(self.id, outline="black", width=1)
        
        # Angriff auslösen, wenn beide Dörfer gewählt sind
        if spiel.angriffs_dorf and spiel.ziel_dorf:
            spiel.dorf_angreifen(spiel.angriffs_dorf, spiel.ziel_dorf)
            spiel.angriffs_dorf = None
            spiel.ziel_dorf = None

    def reset(self):
        self.angreifen = False
        self.canvas.itemconfig(self.id, outline="black", width=1)

class Stadt:
    def __init__(self, canvas, x, y, is_computer):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.is_computer = is_computer
        self.radius = 15  # Größer als Dörfer
        self.color = "yellow" if is_computer else "blue"

        # Zeichne die Stadt als Kreis
        self.id = self.canvas.create_oval(x - self.radius, y - self.radius,
                                          x + self.radius, y + self.radius,
                                          fill=self.color, tags="stadt")

        # Markiere den Bereich um die Stadt (1 Kästchen Radius)
        self.markiere_gebiet()

    def markiere_gebiet(self):
        # Markiert die Felder im 1-Kästchen-Radius als belegt
        for dx in range(-1, 2):  # Von -1 bis 1 für x
            for dy in range(-1, 2):  # Von -1 bis 1 für y
                # Berechne die Rasterkoordinaten
                grid_x, grid_y = int(self.canvas.coords(self.id)[0] // 40 + dx), int(self.canvas.coords(self.id)[1] // 40 + dy)
                if 0 <= grid_x < spiel.grid_cols and 0 <= grid_y < spiel.grid_rows:
                    # Färbe angrenzende Felder als markiert (lightyellow oder lightblue)
                    color = "lightyellow" if self.is_computer else "lightblue"
                    self.canvas.create_rectangle(grid_x * spiel.grid_size, grid_y * spiel.grid_size,
                                                 (grid_x + 1) * spiel.grid_size, (grid_y + 1) * spiel.grid_size,
                                                 fill=color, outline="")
                    # Markiere die Felder als Stadtgebiet
                    spiel.grid_belegt[grid_y][grid_x] = "Stadt"
    
class Einheit:
    def __init__(self, canvas, x, y, dorf, anzahl=10):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.dorf = dorf  # Das Dorf, in dem das Heer stationiert ist
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

class StrategieSpiel:
    def __init__(self, root):
        self.root = root
        self.root.title("Strategie Spiel")
        # self.canvas = tk.Canvas(root, width=800, height=600, bg="lightgreen")
        # self.canvas.pack()

        self.runde = 0

        self.stadt = None

        # Separate Rohstoffkonten für Spieler und Computer
        self.spieler_rohstoffe = 15
        self.computer_rohstoffe = 15
        self.spieler_ressourcenproduktionen = []
        self.computer_ressourcenproduktionen = []

        # Kampfmodus Toggle-Switch
        self.kampfmodus_aktiviert = tk.BooleanVar(value=False)
        self.kampfmodus_toggle = tk.Checkbutton(root, text="Kampfmodus aktivieren", variable=self.kampfmodus_aktiviert)
        self.kampfmodus_toggle.pack()

        # Initialisiere angriffs_dorf und ziel_dorf hier
        self.angriffs_dorf = None
        self.ziel_dorf = None

        # Einheiten (verschiebe) Button
        self.einheiten = []  # Liste aller Einheiten im Spiel
        self.einheiten_verschieben_button = tk.Button(root, text="Einheit verschieben", command=self.verschiebe_einheit)
        self.einheiten_verschieben_button.pack()

        # Angepasste Rohstoff-Anzeigen
        self.spieler_rohstoff_label = tk.Label(root, text=f"Spieler-Rohstoffe: {self.spieler_rohstoffe}")
        self.spieler_rohstoff_label.pack()
        self.computer_rohstoff_label = tk.Label(root, text=f"Computer-Rohstoffe: {self.computer_rohstoffe}")
        self.computer_rohstoff_label.pack()
        
        # Andere GUI Elemente
        self.runden_label = tk.Label(root, text=f"Runde: {self.runde}")
        self.runden_label.pack()

        self.baumodus = tk.StringVar(value="Dorf")
        self.baumodus_menu = tk.OptionMenu(root, self.baumodus, "Dorf", "Ressourcenproduktion", "Stadt")
        self.baumodus_menu.pack()

        self.doerfer = []
        self.ressourcenproduktionen = []
        self.computer_doerfer = []
        self.canvas.bind("<Button-1>", self.neue_bauoption)

        # Zug beenden Button hinzufügen
        self.zug_beenden_button = tk.Button(root, text="Zug beenden", command=self.zug_beenden)
        self.zug_beenden_button.pack()
        
        # Setze Zug-Indikator, um den Spieler und Computerzug in jeder Runde zu unterscheiden
        self.spieler_am_zug = True  # Neuer Indikator, ob der Spieler gerade am Zug ist

        # Grid-Einstellungen
        # self.grid_size = 40  # Größe eines Kästchens im Raster
        self.grid_rows = 15
        self.grid_cols = 20
        self.grid_belegt = [[None for _ in range(self.grid_cols)] for _ in range(self.grid_rows)]  # Belegungsstatus
        
        self.zeichne_raster()
        
        # Kosten für Dörfer, Städte und Ressourcenproduktionen
        self.dorf_kosten = 10
        self.ressourcen_kosten = 5  # Kosten für eine Ressourcenproduktion
        self.stadt_kosten = 20  # Kosten für Stadt

        # Zusätzliche Variable, um zu verhindern, dass die Warnung mehrfach erscheint
        self.warnung_gezeigt = False  # Nur eine Warnung pro Spielerzug bei zu wenigen Rohstoffen

        # Angepasste Zug-Variablen
        self.spieler_am_zug = True
        self.runde_wechseln()

    def zeichne_raster(self):
        # Zeichnet das Raster auf dem Canvas
        for i in range(0, self.grid_cols * self.grid_size, self.grid_size):
            self.canvas.create_line(i, 0, i, self.grid_rows * self.grid_size, fill="gray")
        for j in range(0, self.grid_rows * self.grid_size, self.grid_size):
            self.canvas.create_line(0, j, self.grid_cols * self.grid_size, j, fill="gray")

    def position_im_raster(self, x, y):
        # Berechnet die nächstgelegene Rasterposition
        return x // self.grid_size, y // self.grid_size

    def ist_position_frei(self, grid_x, grid_y):
        # Überprüft, ob die Position im Raster frei ist
        # Felder, die Stadtgebieten zugeordnet sind, sind nicht frei
        if 0 <= grid_x < self.grid_cols and 0 <= grid_y < self.grid_rows:
            if spiel.grid_belegt[grid_y][grid_x] in ["Stadt", "Dorf", "Ressourcenproduktion"]:
                return False  # Feld gehört zu einem Gebäude (Dorf, Stadt oder Ressourcenproduktion)
            return True  # Wenn kein Gebäude vorhanden ist
        return False
    
    def neue_einheit(self, dorf, anzahl=10):
        # Erstellt eine neue Einheit und platziert sie im Dorf
        einheit = Einheit(self.canvas, dorf.x, dorf.y, dorf, anzahl)
        self.einheiten.append(einheit)
        dorf.einheiten.append(einheit)

    def verschiebe_einheit(self):
        # Logik zum Verschieben der Einheiten zwischen den Dörfern
        if self.angriffs_dorf and self.ziel_dorf:
            for einheit in self.angriffs_dorf.einheiten:
                einheit.verschieben(self.ziel_dorf)
            messagebox.showinfo("Verschieben", "Einheiten wurden verschoben.")

    def angreifen(self, angriffs_dorf, ziel_dorf):
        # Berechnet den Angriff, wenn Einheiten im Dorf sind
        if angriffs_dorf.einheiten:
            for einheit in angriffs_dorf.einheiten:
                if ziel_dorf.is_computer:
                    messagebox.showinfo("Angriff", f"Die Einheiten greifen {ziel_dorf.name} an!")
                # Reduziere die Anzahl der Einheiten im Angriff (vereinfacht)
                einheit.anzahl -= 1
            angriffs_dorf.einheiten = [e for e in angriffs_dorf.einheiten if e.anzahl > 0]

    def neue_bauoption(self, event):
        grid_x, grid_y = self.position_im_raster(event.x, event.y)
        # Wenn Kampfmodus aktiviert ist, gehe direkt zu Kampfmodus-Logik
        if self.kampfmodus_aktiviert.get():
            if self.grid_belegt[grid_y][grid_x] == "Dorf":
                if self.spieler_am_zug:
                    for dorf in self.doerfer:
                        if dorf.x == grid_x * self.grid_size + self.grid_size // 2 and dorf.y == grid_y * self.grid_size + self.grid_size // 2:
                            spiel.angriffs_dorf = dorf
                            break
                elif not self.spieler_am_zug:
                    for dorf in self.computer_doerfer:
                        if dorf.x == grid_x * self.grid_size + self.grid_size // 2 and dorf.y == grid_y * self.grid_size + self.grid_size // 2:
                            spiel.ziel_dorf = dorf
                            break
                if spiel.angriffs_dorf and spiel.ziel_dorf:
                    self.dorf_angreifen(spiel.angriffs_dorf, spiel.ziel_dorf)
                    return
        # Verhindert Bau, falls Position besetzt ist
        elif self.ist_position_frei(grid_x, grid_y):
            if self.spieler_am_zug:
                if self.baumodus.get() == "Dorf" and self.spieler_rohstoffe >= self.dorf_kosten:
                    self.neues_dorf(grid_x * self.grid_size + self.grid_size // 2, grid_y * self.grid_size + self.grid_size // 2, False)
                    self.grid_belegt[grid_y][grid_x] = "Dorf"
                elif self.baumodus.get() == "Ressourcenproduktion" and self.spieler_rohstoffe >= self.ressourcen_kosten:
                    self.neue_ressourcenproduktion(grid_x * self.grid_size + self.grid_size // 2, grid_y * self.grid_size + self.grid_size // 2, False)
                    self.grid_belegt[grid_y][grid_x] = "Ressourcenproduktion"
                elif self.baumodus.get() == "Stadt" and self.spieler_rohstoffe >= self.stadt_kosten:
                    self.neue_stadt(grid_x * self.grid_size + self.grid_size // 2, grid_y * self.grid_size + self.grid_size // 2, False)
                    self.grid_belegt[grid_y][grid_x] = "Stadt"
                else:
                    if not self.warnung_gezeigt:
                        messagebox.showwarning("Nicht genug Rohstoffe", f"Du brauchst mehr Rohstoffe für {self.baumodus.get()}.")
                        self.warnung_gezeigt = True
        else:
            messagebox.showinfo("Belegte Position", "Dieses Kästchen ist bereits besetzt oder Teil einer Stadt!")

        grid_x, grid_y = self.position_im_raster(event.x, event.y)

    def neues_dorf(self, x, y, is_computer):
        grid_x, grid_y = self.position_im_raster(x, y)
        if self.ist_position_frei(grid_x, grid_y):
            if is_computer:
                if self.computer_rohstoffe >= self.dorf_kosten:
                    if self.ist_position_frei(grid_x, grid_y):
                        # Dorfbau für Computer
                        dorf_name = f"Computer Dorf {len(self.computer_doerfer) + 1}"
                        neues_dorf = Dorf(self.canvas, x, y, dorf_name, True)
                        self.computer_doerfer.append(neues_dorf)
                        self.computer_rohstoffe -= self.dorf_kosten
                        self.update_rohstoff_label()
            else:
                if self.spieler_rohstoffe >= self.dorf_kosten:
                        # Dorfbau für Spieler
                        dorf_name = f"Spieler Dorf {len(self.doerfer) + 1}"
                        neues_dorf = Dorf(self.canvas, x, y, dorf_name, False)
                        self.doerfer.append(neues_dorf)
                        self.spieler_rohstoffe -= self.dorf_kosten
                        self.update_rohstoff_label()
                else:
                    messagebox.showwarning("Nicht genug Rohstoffe", f"Du brauchst {self.dorf_kosten} Rohstoffe, um ein neues Dorf zu bauen.")

    def neue_ressourcenproduktion(self, x, y, is_computer):
        grid_x, grid_y = self.position_im_raster(x, y)
        if self.ist_position_frei(grid_x, grid_y):
            if is_computer:
                if self.computer_rohstoffe >= self.ressourcen_kosten:
                    neue_produktion = Ressourcenproduktion(self.canvas, x, y, True)
                    self.computer_ressourcenproduktionen.append(neue_produktion)
                    self.computer_rohstoffe -= self.ressourcen_kosten
                    self.update_rohstoff_label()
            else:
                if self.spieler_rohstoffe >= self.ressourcen_kosten:
                    neue_produktion = Ressourcenproduktion(self.canvas, x, y, False)
                    self.spieler_ressourcenproduktionen.append(neue_produktion)
                    self.spieler_rohstoffe -= self.ressourcen_kosten
                    self.update_rohstoff_label()
                else:
                    messagebox.showwarning("Nicht genug Rohstoffe", f"Du brauchst {self.ressourcen_kosten} Rohstoffe, um eine Ressourcenproduktion zu bauen.")

    def neue_stadt(self,x, y, is_computer):
        # Wählt zufällig eine Position und platziere eine Stadt
        grid_x, grid_y = self.position_im_raster(x, y)
        if self.ist_position_frei(grid_x, grid_y):
            if is_computer:
                if self.computer_rohstoffe >= self.stadt_kosten:
                    self.stadt = Stadt(self.canvas, x, y, True)
                    self.computer_rohstoffe -= self.stadt_kosten
                    self.update_rohstoff_label()
            else:
                if self.spieler_rohstoffe >= self.stadt_kosten:
                    self.stadt = Stadt(self.canvas, x, y, False)
                    self.spieler_rohstoffe -= self.stadt_kosten
                    self.update_rohstoff_label()

    def dorf_angreifen(self, angriffs_dorf, ziel_dorf):
        # Linie vom angreifenden Dorf zum Ziel-Dorf zeichnen
        x1, y1 = angriffs_dorf.x, angriffs_dorf.y
        x2, y2 = ziel_dorf.x, ziel_dorf.y
        if angriffs_dorf != ziel_dorf:  # Sicherstellen, dass das Ziel-Dorf ein anderes Dorf ist
            self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, fill="red", width=2)
            # messagebox.showinfo("Angriff", f"{angriffs_dorf.name} greift {ziel_dorf.name} an!")

        # Zurücksetzen der Dorfmarkierungen nach dem Angriff
        angriffs_dorf.reset()
        ziel_dorf.reset()
        self.angriffs_dorf = None
        self.ziel_dorf = None

    def runde_wechseln(self):
        # Erhöht die Rundenzahl nur, wenn ein kompletter Spieler-Computer-Zug abgeschlossen ist
        if self.spieler_am_zug:
            self.runde += 1
            self.update_runden_label()
            
        self.warnung_gezeigt = False  # Zurücksetzen der Warnung am Anfang der Runde
    
    def zug_beenden(self):
        # Beendet den aktuellen Zug und wechselt zum nächsten (Computer oder Spieler)
        if self.spieler_am_zug:
            print("Zug des Spielers beendet, Computer ist am Zug.")
            self.spieler_am_zug = False
            self.computer_rohstoffe += 5 + len(self.computer_ressourcenproduktionen) * 3
            self.update_rohstoff_label()
            self.computer_aktion()  # Wechsle zum Computerzug
        else:
            print("Zug des Computers beendet, Spieler ist am Zug.")
            self.spieler_am_zug = True
            self.spieler_rohstoffe += 5 + len(self.spieler_ressourcenproduktionen) * 3
            self.update_rohstoff_label()
            self.runde_wechseln()  # Wechsle zur nächsten Runde (Spielerzug beginnt wieder)

    def computer_aktion(self):
        if self.computer_rohstoffe >= self.ressourcen_kosten and random.choice([True, False]):
            # Computer platziert eine Ressourcenproduktion
            grid_x, grid_y = random.randint(0, self.grid_cols - 1), random.randint(0, self.grid_rows - 1)
            x, y = grid_x * self.grid_size + self.grid_size // 2, grid_y * self.grid_size + self.grid_size // 2
            if self.ist_position_frei(grid_x, grid_y):
                self.neue_ressourcenproduktion(x, y, True)
                self.grid_belegt[grid_y][grid_x] = "Ressourcenproduktion"
        if self.computer_rohstoffe >= self.dorf_kosten and random.choice([True, False]):
            # Computer platziert ein Dorf
            grid_x, grid_y = random.randint(0, self.grid_cols - 1), random.randint(0, self.grid_rows - 1)
            x, y = grid_x * self.grid_size + self.grid_size // 2, grid_y * self.grid_size + self.grid_size // 2
            if self.ist_position_frei(grid_x, grid_y):
                self.neues_dorf(x, y, True)
                self.grid_belegt[grid_y][grid_x] = "Dorf"
        if self.computer_rohstoffe >= self.stadt_kosten and random.choice([True, False]):
            # Computer platziert eine Stadt
            grid_x, grid_y = random.randint(0, self.grid_cols - 1), random.randint(0, self.grid_rows - 1)
            x, y = grid_x * self.grid_size + self.grid_size // 2, grid_y * self.grid_size + self.grid_size // 2
            if self.ist_position_frei(grid_x, grid_y):
                self.neue_stadt(x, y, True)
                self.grid_belegt[grid_y][grid_x] = "Stadt"
        if self.computer_doerfer and self.doerfer:
            # Computer führt einen Angriff durch, wenn Spieler- und Computerdörfer vorhanden sind
            angriffs_dorf = random.choice(self.computer_doerfer)
            ziel_dorf = random.choice(self.doerfer)
            self.dorf_angreifen(angriffs_dorf, ziel_dorf)

        # Rückgabe an den Spieler nach kurzer Wartezeit
        self.root.after(1000, self.zug_beenden)

    def update_rohstoff_label(self):
        self.spieler_rohstoff_label.config(text=f"Spieler-Rohstoffe: {self.spieler_rohstoffe}")
        self.computer_rohstoff_label.config(text=f"Computer-Rohstoffe: {self.computer_rohstoffe}")

    def update_runden_label(self):
        self.runden_label.config(text=f"Runde: {self.runde}")

if __name__ == "__main__":
    root = tk.Tk()
    spiel = StrategieSpiel(root)
    root.mainloop()
