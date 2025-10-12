import random

class ComputerAI:
    def __init__(self, spiel):
        self.spiel = spiel

    def zug_ausfuehren(self):
        # Logik für den Zug des Computers
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
