import config

from gui.game_canvas import GameCanvas
from gui.buttons import ButtonPanel
from gui.labels import ResourceLabel
from controllers.ressource_manager import ResourceManager

import utils.economy_manager as economy_manager
import utils.game_state_utils as game_state_utils
import utils.window_utils as window_utils


class StrategieSpiel:
    """Hauptklasse des Spiels."""
    def __init__(self, root):
        self.canvas = GameCanvas(root)
        config.GameWindow.buttons = ButtonPanel(root)
        config.GameWindow.buttons.create_buttons(self.end_turn, self.end_round)
        config.GameWindow.labels = ResourceLabel(root)
        self.resource_manager = ResourceManager()

        self.init_game()

    def init_game(self):
        economy_manager.set_init_ressources()
        self.canvas.create_grid()
        window_utils.update_widgets(config.GameWindow.labels)
        game_state_utils.test()

    def end_turn(self):
        # Zug beenden
        if config.Game.current_turn == 0:
            game_state_utils.next_turn()
            window_utils.update_widgets(config.GameWindow.labels)
        elif config.Game.current_turn == 1:
            self.end_round()

    def end_round(self):
        # Runde beenden und Ressourcen aktualisieren
        game_state_utils.next_turn()
        economy_manager.add_ressources()
        window_utils.update_widgets(config.GameWindow.labels)
