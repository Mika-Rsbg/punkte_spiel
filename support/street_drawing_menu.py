import tkinter as tk
from random import randint
import config

import utils.canvas_utils as canvas_utils
import utils.identify_utils as identify_utils
import utils.game_state_utils as game_state_utils


class StreetDrawingMenu:
    def __init__(self, parent, predefined_buildings=None):
        """Erstellt das Straßen-Manager-Menü als Toplevel-Fenster.

        Args:
            parent (tk.Tk | tk.Toplevel): Das Elternfenster.
            predefined_buildings (dict[tuple[int, int], int], optional): 
                Ein Dictionary mit vordefinierten Gebäuden, 
                z. B. {(0, 0): 1 (dorf), (1, 2): 3 (Stadt)}.
        """
        self.window = tk.Toplevel(parent)
        self.window.title("Straßen Manager")

        # Übernehme Konfigurationswerte aus der Hauptanwendung
        self.grid_size = config.GameGrid.GRID_SIZE
        self.cell_count = 5  # Mehr Zellen für detailliertere Vorschau
        self.canvas_width = self.cell_count * self.grid_size +1
        self.canvas_height = self.canvas_width

        self.fields = {}
        self.road_ids = {}  # Speichert die gezeichneten Straßenobjekte pro Feld
        # Canvas für Auswahl und Vorschau
        self.selection_canvas = tk.Canvas(self.window, width=self.canvas_width, height=self.canvas_height, bg=config.GameCanvas.CANVAS_BACKGROUND)
        self.selection_canvas.grid(row=0, column=0, padx=10, pady=10)

        self.preview_canvas = tk.Canvas(self.window, width=self.canvas_width, height=self.canvas_height, bg=config.GameCanvas.CANVAS_BACKGROUND)
        self.preview_canvas.grid(row=0, column=1, padx=10, pady=10)

        # Buttons
        self.confirm_button = tk.Button(self.window, text="Bestätigen", command=self.confirm_selection)
        self.confirm_button.grid(row=1, column=0, pady=10)

        self.close_button = tk.Button(self.window, text="Schließen", command=self.close_window)
        self.close_button.grid(row=1, column=1, pady=10)

        # Felder aus config.GameGrid.fields initialisieren
        if predefined_buildings is None:
            self.predefined_buildings = {}
            fields = config.GameGrid.fields
            radius = self.cell_count / 2 - self.cell_count % 2
            col, row = config.GameCanvas.selected_field
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    field = (col + dx, row + dy)
                    if field in fields:
                        self.predefined_buildings[field] = {
                            "building": fields[field]["building"],
                            "player": fields[field]["player"],
                            "connections": fields[field]["connections"]
                        }
        else:
            self.predefined_buildings = predefined_buildings
        # Initialisiere die Gitter und Interaktionen
        self.selected_fields = set()
        self.draw_grid(self.selection_canvas)
        self.draw_grid(self.preview_canvas)
        self.populate_predefined_buildings()
        self.selection_canvas.bind("<Button-1>", self.on_click_selection)

    def draw_grid(self, canvas):
        """Zeichnet ein Raster auf das gegebene Canvas."""
        for row in range(self.cell_count):
            for col in range(self.cell_count):
                x1, y1 = col * self.grid_size +2, row * self.grid_size +2
                x2, y2 = x1 + self.grid_size, y1 + self.grid_size
                rect_id = canvas.create_rectangle(x1, y1, x2, y2, outline="black")
                building = None
                connect_to = False
                if (col, row) in self.predefined_buildings:
                    connect_to = True
                    building = self.predefined_buildings[(col, row)]["building"]
                click_able = True
                if (col in [0, 4] or row in [0, 4]) or not connect_to:
                    click_able = False
                self.fields[(col, row)] = {
                    "rect_id": rect_id,
                    "building": building,
                    "connect_to": connect_to,
                    "click_able": click_able
                }
        self.mark_not_click_able_fields()
    
    def mark_not_click_able_fields(self):
        for row in range(self.cell_count):
            for col in range(self.cell_count):
                if not self.fields[(col, row)]["click_able"] and not (col, row) in [(2, 2)]:
                    canvas_utils.transparently_highlight_field(self.selection_canvas, col=col, row=row, color=config.Design.Colors.DARK, alpha=0.75, fields=self.fields)

    def on_click_selection(self, event):
        """Behandelt Klicks auf der Auswahlfläche."""
        col = event.x // self.grid_size
        row = event.y // self.grid_size
        field = (col, row)

        if self.fields[field]["click_able"]:
            if field in self.selected_fields:
                # Entferne Markierung
                self.selected_fields.remove(field)
                canvas_utils.clear_field(canvas=self.selection_canvas, col=col, row=row, fields=self.fields)
                if field in self.road_ids:
                    for road_id in self.road_ids[field]:
                        self.preview_canvas.delete(road_id)
                    del self.road_ids[field]
            else:
                # Füge Markierung hinzu
                self.selected_fields.add(field)
                canvas_utils.highlight_field(canvas=self.selection_canvas, col=col, row=row, fields=self.fields)
                road_ids = canvas_utils.draw.draw_road(canvas=self.preview_canvas, start_coords=(2, 2), end_coords=field)
                self.road_ids[field] = road_ids  # Speichere die Straßen-IDs

        # Aktualisiere Vorschau
        self.update_preview(field)

    # def update_street(self, canvas, col, row):
    #     """Aktualisiert die Straßenabschnitte eines Feldes basierend auf gespeicherten Verbindungen.

    #     Args:
    #         canvas (tk.Canvas): Das Tkinter Canvas-Objekt.
    #         col (int): Die Spalte des Feldes.
    #         row (int): Die Zeile des Feldes.
    #     """
    #     fields = self.predefined_buildings

    #     # Zeichne alle Straßenabschnitte basierend auf den gespeicherten Verbindungen
    #     for direction, is_connected in fields[(col, row)]["connections"].items():
    #         if is_connected:
    #             canvas_utils.draw.draw_road_segment(
    #                 canvas=canvas,
    #                 col=col,
    #                 row=row,
    #                 direction=direction,
    #                 outline_color=game_state_utils.get_player_color(fields[(col, row)]["player"]),
    #                 color="gray"
    #             )

    def place_street(self, canvas, col, row, target_col, target_row,fields):
        field = (col, row)
        if fields[(target_col, target_row)]["connect_to"]:
            canvas_utils.draw.draw_road(canvas, field, (target_col, target_row))
            building_id = fields[(target_col, target_row)]["building"]
            if building_id == config.Building.BuildingID.DORF:
                canvas_utils.draw.draw_dorf(canvas, col=target_col, row=target_row)
            elif building_id == config.Building.BuildingID.RESSOURCENPRODUKTION:
                canvas_utils.draw.draw_ressourcenproduktion(canvas, col=target_col, row=target_row)
            elif building_id == config.Building.BuildingID.STADT:
                canvas_utils.draw.draw_stadt(canvas, col=target_col, row=target_row)
            # elif building_id == config.Building.BuildingID.STREET:
            #     self.update_street(canvas, col=target_col, row=target_row)

    def populate_predefined_buildings(self):
        """Zeichnet vordefinierte Gebäude und Straßen basierend auf config.GameGrid.fields."""
        for (col, row), item_data in self.predefined_buildings.items():
            building_id = item_data["building"]
            connections = item_data["connections"]

            if building_id == config.Building.BuildingID.DORF:
                canvas_utils.draw.draw_dorf(self.selection_canvas, col=col, row=row)
                canvas_utils.draw.draw_dorf(self.preview_canvas, col=col, row=row)
            elif building_id == config.Building.BuildingID.RESSOURCENPRODUKTION:
                canvas_utils.draw.draw_ressourcenproduktion(self.selection_canvas, col=col, row=row)
                canvas_utils.draw.draw_ressourcenproduktion(self.preview_canvas, col=col, row=row)
            elif building_id == config.Building.BuildingID.STADT:
                canvas_utils.draw.draw_stadt(self.selection_canvas, col=col, row=row)
                canvas_utils.draw.draw_stadt(self.preview_canvas, col=col, row=row)
            elif building_id == config.Building.BuildingID.STREET:
                # Straßen zeichnen basierend auf Verbindungen
                for direction, connected in connections.items():
                    print(direction, connected)
                    if connected:
                        target_col, target_row = identify_utils.get_neighbor_coordinates(col, row, direction)
                        print(1)
                        if (target_col, target_row) in self.fields:
                            print(2)
                            self.place_street(canvas=self.selection_canvas, col=col, row=row, target_col=target_col, target_row=target_row, fields=self.fields)
                            self.place_street(canvas=self.preview_canvas, col=col, row=row, target_col=target_col, target_row=target_row, fields=self.fields)

    def update_preview(self, field):
        """Zeigt die aktuelle Auswahl in der Vorschau an."""
        col, row = field
        if field in self.selected_fields:
            canvas_utils.transparently_highlight_field(self.preview_canvas, col, row, color=game_state_utils.get_player_color(), fields=self.fields, alpha=0.15)
        else:
            canvas_utils.clear_field(self.preview_canvas, col, row, fields=self.fields)
        building_id = self.fields[(col, row)]["building"]
        if building_id == config.Building.BuildingID.DORF:
            canvas_utils.draw.draw_dorf(self.preview_canvas, col=col, row=row)
        elif building_id == config.Building.BuildingID.RESSOURCENPRODUKTION:
            canvas_utils.draw.draw_ressourcenproduktion(self.preview_canvas, col=col, row=row)
        elif building_id == config.Building.BuildingID.STADT:
            canvas_utils.draw.draw_stadt(self.preview_canvas, col=col, row=row)

    def confirm_selection(self):
        """Gibt die ausgewählten Teile aus und schließt das Menü."""
        print("Ausgewählte Teile:", self.selected_fields)
        self.window.destroy()

    def close_window(self):
        self.window.destroy()
        # canvas_utils.clear_field(config.GameCanvas.canvas, field_coords=config.GameCanvas.selected_field)
        # config.GameCanvas.is_field_selected = False
        # config.GameCanvas.selected_field = None
