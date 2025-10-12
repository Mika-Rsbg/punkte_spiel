import tkinter as tk
import utils.grid_utils as grid_utils
import utils.canvas_utils as canvas_utils
import utils.identify_utils as identify_utils
import config

from gui.menus.building_menu import BuildingMenu
from gui.menus.dorf_menu import DorfMenu
from gui.menus.attack_menu import AttackMenu
from gui.menus.ressourcenproduktion_menu import RessourcenproduktionMenu
from gui.menus.stadt_menu import StadtMenu

from models.home import Home
from models.street import Street

class GameCanvas:
    def __init__(self, root):
        self.root = root
        config.GameCanvas.canvas = tk.Canvas(self.root, width=config.GameCanvas.CANVAS_WIDTH, height=config.GameCanvas.CANVAS_HEIGHT, bg=config.GameCanvas.CANVAS_BACKGROUND)
        config.GameCanvas.canvas.grid(row=0, column=0, columnspan=5)
        config.GameCanvas.canvas.bind("<Button-1>", self.on_click)

    @staticmethod
    def create_grid(rows=config.GameGrid.GRID_ROWS, cols=config.GameGrid.GRID_COLS, grid_size=config.GameGrid.GRID_SIZE):
        """Erzeugt das Spielfeld-Raster

        Args:
            rows (int, optional): Anzahl der Zeilen. Defaults to `config.Grid.GRID_ROWS`.
            cols (int, optional): Anzahl der Spalten. Defaults to `config.Grid.GRID_COLS`.
            grid_size (int, optional): Größe der Felder. Defaults to `config.Grid.GRID_SIZE`."""
        for row in range(rows):
            for col in range(cols):
                # Berechne die Koordinaten für jedes Feld
                x1, y1 = col * grid_size +2, row * grid_size +2
                x2, y2 = x1 + grid_size, y1 + grid_size
                
                # Erstelle das Rechteck für das Feld
                rect_id = config.GameCanvas.canvas.create_rectangle(x1, y1, x2, y2, outline="black")
                # Speichere die Feldinformationen als Dictionary
                config.GameGrid.fields[(col, row)] = {
                    "rect_id": rect_id,     # Rechteck-ID im Canvas
                    "building": config.Building.BuildingID.NO_BUILDING,     # 0=nichts, 1=Dorf, weitere Werte können hinzugefügt werden
                    "player": config.Player.PlayerID.NO_PLAYER,     # 0=nicht eingenommen, 1=player1, 2=player2 (Computer)
                    "persistent_color": None,    # Farbe für persistente Highlights
                    "connections": {             # Verbindungen zu Straßen in spezifischen Richtungen
                        "N": False,  # Norden
                        "NE": False, # Nord-Osten
                        "E": False,  # Osten
                        "SE": False, # Süd-Osten
                        "S": False,  # Süden
                        "SW": False, # Süd-Westen
                        "W": False,  # Westen
                        "NW": False, # Nord-Westen
                    }
                }

    def on_click(self, event):
        """Behandelt Mausklicks auf dem Canvas."""
        # Pixelkoordinaten des Klicks
        x, y = event.x, event.y

        # Berechne die Grid-Koordinaten
        result = grid_utils.get_grid_coordinates(x, y)

        if result:
            if config.Building.Home.place_home_mode:
                col, row = result
                if grid_utils.home_can_be_placed(col, row):
                    if not config.GameCanvas.is_field_selected:
                        config.GameCanvas.is_field_selected = True
                        config.GameCanvas.selected_field = result
                        ###############################################################
                        canvas_utils.highlight_field(config.GameCanvas.canvas, col, row)
                        ###############################################################
                    elif config.GameCanvas.is_field_selected:
                        if config.GameCanvas.selected_field == result:
                            Home.place_home()
                        else:
                            canvas_utils.clear_field(config.GameCanvas.canvas, field_coords=config.GameCanvas.selected_field)
                            config.GameCanvas.selected_field = result
                            ###############################################################
                            canvas_utils.highlight_field(config.GameCanvas.canvas, col, row)
                            ###############################################################
            elif config.Building.Street.street_placing_mode:
                if config.Building.Street.street_start_field is None:
                    config.GameCanvas.selected_field = result
                    config.Building.Street.street_start_field = result
                    canvas_utils.highlight_field(config.GameCanvas.canvas, field_coords=result)
                elif result == config.Building.Street.street_start_field:
                    config.GameCanvas.selected_field = None
                    config.Building.Street.street_start_field = None
                    canvas_utils.clear_field(config.GameCanvas.canvas, field_coords=result)
                elif identify_utils.is_neighbour(config.Building.Street.street_start_field, result):
                    config.GameCanvas.selected_field = result
                    config.Building.Street.street_end_field = result
                    canvas_utils.clear_field(config.GameCanvas.canvas, field_coords=config.Building.Street.street_start_field)
                    canvas_utils.highlight_field(config.GameCanvas.canvas, field_coords=result)
                    Street.build_preview_street()
                    config.Building.Street.street_start_field = result
                    config.Building.Street.street_end_field = None
            else:
                if not config.GameCanvas.is_field_selected:
                    config.GameCanvas.is_field_selected = True
                    config.GameCanvas.selected_field = result
                    col, row = result
                    self.select_field(col, row)

    def select_field(self, col, row, player_id=config.Game.current_turn):
        aktive_player = player_id + 1
        canvas_utils.highlight_field(config.GameCanvas.canvas, col, row)
        field = config.GameGrid.fields[(col, row)]
        building_id = grid_utils.get_building_id((col, row))
        if field["player"] == 0:
            BuildingMenu(self.root)
        elif field["player"] == aktive_player:
            if building_id == config.Building.BuildingID.NO_BUILDING:
                BuildingMenu(self.root)
            elif building_id == config.Building.BuildingID.DORF:
                DorfMenu(self.root)
            elif building_id == config.Building.BuildingID.RESSOURCENPRODUKTION:
                RessourcenproduktionMenu(self.root)
            elif building_id == config.Building.BuildingID.STADT:
                StadtMenu(self.root)
        else:
            if building_id > config.Building.BuildingID.NO_BUILDING:
                AttackMenu(self.root)
