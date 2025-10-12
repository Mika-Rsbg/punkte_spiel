import config

import utils.economy_manager as economy_manager
import utils.canvas_utils as canvas_utils

from models.home import Home

def next_turn(count_round=True):
    if config.Game.current_turn == 0:
        config.Game.current_turn = 1
    elif config.Game.current_turn == 1:
        config.Game.current_turn = 0
        if count_round:
            config.Game.round_number += 1
###############################################################
###############################################################
# Documetation
###############################################################
###############################################################

def get_player_color(current_turn=None):
    if current_turn is None:
        current_turn = config.Game.current_turn
    if current_turn == 0:
        return config.Player.Player1.COLOR
    elif current_turn == 1:
        return config.Player.Player2.COLOR
###############################################################
###############################################################
# Documetation
###############################################################
###############################################################
    
def get_number_of_buildings(building_id, player=None):
    """Wie viele Gebäude hat der Spieler gebaut.
    Args:
        building_typ (int): GebäudeID des Gebäude-Typen
        player (int, optional): PlayerID des Players. Defaults to None.
    Returns:
        int: Anzahl der Gebäude die ein Spieler von einem Typen gebaut hat."""
    if player is None:
        player_id = config.Game.current_turn + 1
    if player is not None and (player == config.Player.PlayerID.PLAYER_1 or player == config.Player.PlayerID.PLAYER_2):
        player_id = player
    
    if building_id == config.Building.BuildingID.DORF:
        if player_id == 1:
            return config.Player.Player1.number_of_dorfer
        if player_id == 2:
            return config.Player.Player2.number_of_dorfer
    elif building_id == config.Building.BuildingID.RESSOURCENPRODUKTION:
        if player_id == 1:
            return config.Player.Player1.number_of_ressourcenproduktion
        if player_id == 2:
            return config.Player.Player2.number_of_ressourcenproduktion
    elif building_id == config.Building.BuildingID.STADT:
        if player_id == 1:
            return config.Player.Player1.number_of_stadte
        if player_id == 2:
            return config.Player.Player2.number_of_stadte
    elif building_id == config.Building.BuildingID.STREET:
        if player_id == 1:
            return config.Player.Player1.number_of_streets
        if player_id == 2:
            return config.Player.Player2.number_of_streets


def get_building(building_id):
    if building_id == config.Building.BuildingID.DORF:
        return config.Building.Dorf
    elif building_id == config.Building.BuildingID.RESSOURCENPRODUKTION:
        return config.Building.Ressourcenproduktion
    elif building_id == config.Building.BuildingID.STADT:
        return config.Building.Stadt
    elif building_id == config.Building.BuildingID.STREET:
        return config.Building.Street
###############################################################
###############################################################
# Documetation
###############################################################
###############################################################

def get_player(player_id=None):
    if player_id is None:
        player_id = config.Game.current_turn + 1
    if player_id == config.Player.PlayerID.PLAYER_1:
        return config.Player.Player1
    if player_id == config.Player.PlayerID.PLAYER_2:
        return config.Player.Player2
###############################################################
###############################################################
# Documetation
###############################################################
###############################################################

def get_player_ressources(player_id=None):
    if player_id is None:
        player_id = config.Game.current_turn + 1
    
    if player_id == 1:
        return config.Player.Player1.ressources
    elif player_id == 2:
        return config.Player.Player2.ressources
###############################################################
###############################################################
# Documetation
###############################################################
###############################################################

def get_building_availability_color(building_id, ressources, default_color, unavailable_color="red"):
    """Gibt die Hintergrundfarbe für ein Gebäude basierend auf den Ressourcen zurück.

    Args:
        building_id (str): ID des Gebäudes (z. B. Dorf, Stadt).
        ressources (int): Verfügbare Ressourcen des Spielers.
        default_color (str): Standardfarbe (z. B. Fensterhintergrund).
        unavailable_color (str, optional): Farbe, wenn das Gebäude zu teuer ist. Defaults to "red".

    Returns:
        str: Farbe für das Gebäude."""
    cost = economy_manager.calculate_building_cost(building_id)
    return default_color if ressources >= cost else unavailable_color

def is_building_too_expensive(building_id, ressources):
    """Gibt zurück ob ein Gebäude für einen Spieler zu teuer ist.

    Args:
        building_id (int): GebäudeID
        ressources (int): Für den Spieler Verfügbare Ressourcen.

    Returns:
        Boolean: `True`: ist zu teuer, `False`: ist nicht zu teuer."""
    cost = economy_manager.calculate_building_cost(building_id)
    return True if cost > ressources else False

def occupy_field(col=None, row=None, field=None):
    if col is None or row is None:
        if field is None:
            col, row = config.GameCanvas.selected_field
        else:
            col, row = field
    canvas_utils.persistent_highlight_field(config.GameCanvas.canvas, col=col, row=row, alpha=0.15)
###############################################################
###############################################################
# Documetation
###############################################################
###############################################################

def test():
    Home.mark_available_area_for_home()
###############################################################
###############################################################
# Position, Useless???
###############################################################
###############################################################
