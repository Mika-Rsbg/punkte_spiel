import config

import utils.canvas_utils as canvas_utils
import utils.economy_manager as economy_manager
import utils.game_state_utils as game_state_utils

class Ressourcenproduktion:
    @staticmethod
    def occupy_area(col, row):
        occupation_radius = config.Building.Ressourcenproduktion.OCCUPATION_RADIUS
        fields = config.GameGrid.fields
        for col_1 in range(col - occupation_radius, col + (occupation_radius + 1)):
            for row_1 in range(row - occupation_radius, row + (occupation_radius + 1)):
                if (col_1, row_1) in fields:
                    game_state_utils.occupy_field(col_1, row_1)

    @classmethod
    def build_ressourcenproduktion(cls):
        """Baut(Zeichnet) Ressourcenproduktion auf dem GameCanvas-Canvas."""
        col, row = config.GameCanvas.selected_field
        canvas_utils.draw.draw_ressourcenproduktion(config.GameCanvas.canvas, col=col, row=row)
        config.GameCanvas.is_field_selected = False
        config.GameGrid.fields[(col, row)]["building"] = config.Building.BuildingID.RESSOURCENPRODUKTION
        config.GameGrid.fields[(col, row)]["player"] = config.Game.current_turn + 1
        canvas_utils.clear_field(config.GameCanvas.canvas, col=col, row=row)
        economy_manager.pay_building(config.Building.BuildingID.RESSOURCENPRODUKTION)
        economy_manager.increase_resources_per_round(config.Building.Ressourcenproduktion.INCREASES_RESSOURCEPRODUKTION_BY)
        cls.occupy_area(col, row)
        game_state_utils.get_player().number_of_ressourcenproduktion += 1
