import config

import utils.canvas_utils as canvas_utils
import utils.game_state_utils as game_state_utils

class Home:
    @staticmethod
    def mark_available_area_for_home():
        config.Building.Home.place_home_mode = True
        for row in range(config.GameGrid.GRID_ROWS):
            for col in range(config.GameGrid.GRID_COLS):
                if config.Building.Home.left_player == 0 and config.Building.Home.right_player == 0:
                    if not col < config.Building.Home.rows_for_placement:
                        canvas_utils.transparently_highlight_field(config.GameCanvas.canvas, col=col, row=row, color=config.Design.Colors.DARK, alpha=0.75)
                    if col > (config.GameGrid.GRID_COLS - config.Building.Home.rows_for_placement - 1):
                        canvas_utils.clear_field(config.GameCanvas.canvas, col=col, row=row)
                elif (not config.Building.Home.left_player == 0) and config.Building.Home.right_player == 0:
                    canvas_utils.transparently_highlight_field(config.GameCanvas.canvas, col=col, row=row, color=config.Design.Colors.DARK, alpha=0.75)
                    if col > (config.GameGrid.GRID_COLS - config.Building.Home.rows_for_placement - 1):
                        canvas_utils.clear_field(config.GameCanvas.canvas, col=col, row=row)
                elif config.Building.Home.left_player == 0 and (not config.Building.Home.right_player == 0):
                    if not col < config.Building.Home.rows_for_placement:
                        canvas_utils.transparently_highlight_field(config.GameCanvas.canvas, col=col, row=row, color=config.Design.Colors.DARK, alpha=0.75)
    ###############################################################
    ###############################################################
    # Documentation
    ###############################################################
    ###############################################################

    @staticmethod
    def occupy_area(col, row):
        occupation_radius = config.Building.Home.OCCUPATION_RADIUS
        fields = config.GameGrid.fields
        for col_1 in range(col - occupation_radius, col + (occupation_radius + 1)):
            for row_1 in range(row - occupation_radius, row + (occupation_radius + 1)):
                if (col_1, row_1) in fields:
                    game_state_utils.occupy_field(col_1, row_1)
    ###############################################################
    ###############################################################
    # Documentation
    ###############################################################
    ###############################################################

    @classmethod
    def place_home(cls):
        col, row = config.GameCanvas.selected_field
        if col >= (config.GameGrid.GRID_COLS / 2 - 1):
            config.Building.Home.right_player = config.Game.current_turn + 1
        elif col <= (config.GameGrid.GRID_COLS / 2):
            config.Building.Home.left_player = config.Game.current_turn + 1

        canvas_utils.draw.draw_stadt(config.GameCanvas.canvas, col=col, row=row)
        config.GameCanvas.is_field_selected = False
        config.GameGrid.fields[(col, row)]["building"] = config.Building.BuildingID.HOME
        config.GameGrid.fields[(col, row)]["player"] = config.Game.current_turn + 1
        cls.occupy_area(col, row)
        canvas_utils.clear_all_fields(config.GameCanvas.canvas)
        if config.Game.current_turn == 0:
            cls.mark_available_area_for_home()
        elif config.Game.current_turn == 1:
            config.Building.Home.place_home_mode = False

        game_state_utils.next_turn(False)
        config.GameCanvas.selected_field = None
    ###############################################################
    ###############################################################
    # Documentation
    ###############################################################
    ###############################################################
