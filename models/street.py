import config

import utils.canvas_utils as canvas_utils
import utils.economy_manager as economy_manager
import utils.game_state_utils as game_state_utils   

class Street:
    @staticmethod
    def occupy_area(previewed_streets):
        for ((start_coords, end_coords), (outline_id, line_id)) in previewed_streets:
            occupation_radius = config.Building.Street.OCCUPATION_RADIUS
            fields = config.GameGrid.fields
            for (col, row) in (start_coords, end_coords):
                for col1 in range(col - occupation_radius, col + (occupation_radius + 1)):
                    for row1 in range(row - occupation_radius, row + (occupation_radius + 1)):
                        if (col1, row1) in fields:
                            game_state_utils.occupy_field(col1, row1)

    @staticmethod
    def update_connections(col, row, connected_col, connected_row):
        """Aktualisiert die Straßenverbindungen in den Feldern."""
        direction_map = {
            (0, -1): "N",   # Nach Norden
            (1, -1): "NE",  # Nach Nord-Osten
            (1, 0): "E",    # Nach Osten
            (1, 1): "SE",   # Nach Süd-Osten
            (0, 1): "S",    # Nach Süden
            (-1, 1): "SW",  # Nach Süd-Westen
            (-1, 0): "W",   # Nach Westen
            (-1, -1):"NW"   # Nord-Westen
        }
        
        delta_col = connected_col - col
        delta_row = connected_row - row

        if (delta_col, delta_row) in direction_map:
            direction = direction_map[(delta_col, delta_row)]
            config.GameGrid.fields[(col, row)]["connections"][direction] = True

    @classmethod
    def place_street(cls, col=None, row=None, replace=False):
        if col is None or row is None:
            col, row = config.GameCanvas.selected_field
        for connected_col in range(col - 1, col + 2):
            for connected_row in range(row - 1, row + 2):
                if config.GameGrid.fields[(connected_col, connected_row)]["connect_to"] == (config.Game.current_turn + 1):
                    # Zeichne die Straße
                    canvas_utils.draw.draw_road(config.GameCanvas.canvas, start_coords=(col, row), end_coords=(connected_col, connected_row))
                    # Aktualisiere Verbindungen
                    cls.update_connections(col, row, connected_col, connected_row)

                    # Aktualisiere Gebäude
                    building_id = config.GameGrid.fields[(connected_col, connected_row)]["building"]
                    if building_id == config.Building.BuildingID.DORF:
                        canvas_utils.draw.draw_dorf(config.GameCanvas.canvas, col=connected_col, row=connected_row)
                    elif building_id == config.Building.BuildingID.RESSOURCENPRODUKTION:
                        canvas_utils.draw.draw_ressourcenproduktion(config.GameCanvas.canvas, col=connected_col, row=connected_row)
                    elif building_id == config.Building.BuildingID.STADT:
                        canvas_utils.draw.draw_stadt(config.GameCanvas.canvas, col=connected_col, row=connected_row)
                    # elif building_id == config.Building.BuildingID.STREET and replace:
                    #     cls.update_street(connected_col, connected_row)

    @classmethod
    def build_street(cls, replace=False, col=None, row=None):
        """Baut(Zeichnet) Dorf auf dem GameCanvas-Canvas."""
        cls.place_street(col=col, row=row, replace=replace)
        config.GameCanvas.is_field_selected = False
        config.GameGrid.fields[(col, row)]["building"] = config.Building.BuildingID.STREET
        config.GameGrid.fields[(col, row)]["player"] = config.Game.current_turn + 1
        canvas_utils.clear_field(config.GameCanvas.canvas, col=col, row=row)
        economy_manager.pay_building(config.Building.BuildingID.STREET)
        game_state_utils.get_player().number_of_streets += 1
        cls.occupy_area(col, row)

    @classmethod
    def start_street_placing_mode(cls):
        config.Building.Street.street_placing_mode = True
        config.Building.Street.street_start_field = config.GameCanvas.selected_field

        config.GameWindow.buttons.create_street_placing_mode_buttons(on_cancel=cls.cancel_street_placing_mode, on_confirm=cls.end_street_placing_mode)

    @staticmethod
    def build_preview_street():
        street_id = canvas_utils.draw.draw_road(config.GameCanvas.canvas, start_coords=config.Building.Street.street_start_field, end_coords=config.Building.Street.street_end_field)
        config.Building.Street.preview_streets.append(((config.Building.Street.street_start_field, config.Building.Street.street_end_field), street_id))
    
    @staticmethod
    def cancel_street_placing_mode():
        """Bricht den Straßenbau-Modus ab und löscht alle Vorschau-Straßen."""
        # Alle Vorschau-Straßen löschen
        for ((start_coords, end_coords), (outline_id, line_id)) in config.Building.Street.preview_streets:
            config.GameCanvas.canvas.delete(outline_id)
            config.GameCanvas.canvas.delete(line_id)

        # Daten zurücksetzen
        config.Building.Street.preview_streets.clear()
        config.Building.Street.street_start_field = None
        config.Building.Street.street_end_field = None
        config.Building.Street.street_placing_mode = False

        # Buttons und UI anpassen (z. B. Buttons für den Straßenbau-Modus entfernen)
        config.GameWindow.buttons.remove_street_placing_mode_buttons()

        config.GameCanvas.is_field_selected = False
        canvas_utils.clear_field(config.GameCanvas.canvas, field_coords=config.GameCanvas.selected_field)
        config.GameCanvas.selected_field = None

    @classmethod
    def end_street_placing_mode(cls):
        """Beendet den Straßenbau-Modus und speicher alle Vorschau-Straßen."""
        number_of_streets = len(config.Building.Street.preview_streets)
        economy_manager.pay_building(config.Building.BuildingID.STREET, number=number_of_streets)
        cls.occupy_area(config.Building.Street.preview_streets)
        for street_form_id in config.Building.Street.preview_streets:
            game_state_utils.get_player().streets.append(street_form_id)

        # Buttons und UI anpassen (z. B. Buttons für den Straßenbau-Modus entfernen)
        config.GameWindow.buttons.remove_street_placing_mode_buttons()

        config.GameCanvas.is_field_selected = False
        col, row = config.GameCanvas.selected_field
        canvas_utils.clear_field(config.GameCanvas.canvas, col, row)
        config.GameCanvas.selected_field = None
        config.Building.Street.street_placing_mode = False
