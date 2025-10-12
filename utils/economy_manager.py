import config

import utils.game_state_utils as game_state_utils

def calculate_building_cost(building_id):
    """Berechnet die Baukosten unter Berücksichtigung der Anzahl bestehender Gebäude und der Inflation.
    Args:
        building_id (int): GebäudeID
    Returns:
        int: Kosten für den Bau des Gebäude"""
    num_existing_buildings = game_state_utils.get_number_of_buildings(building_id)
    init_building_price = game_state_utils.get_building(building_id).INIT_BUILDING_PRICE
    adjustment_factor = game_state_utils.get_building(building_id).BUILDING_PRICE_ADJUSTMENT_FACTOR

    round_number = config.Game.round_number
    inflation_rate = config.Game.inflation_rate
    
    scaling_cost = init_building_price * (1 + num_existing_buildings / adjustment_factor)
    inflation_cost = scaling_cost * (1 + round_number * inflation_rate)
    cost = round(inflation_cost)
    return cost

def calculate_street_building_cost(number):
    """_summary_

    Args:
        number (_type_): _description_
    """
    cost_float = number * 0.1 + config.Building.Street.INIT_BUILDING_PRICE
    cost = round(cost_float)
    return cost

###################################################################
###################################################################
# Dokumentation
###################################################################
###################################################################

def calculate_maintenance_cost(building_id):
    """Berechnet die laufenden Unterhaltskosten eines Gebäudes.
    Args:
        building_id (int): GebäudeID
    Returns:
        int: Unterhalt pro Runde"""
    round_number = config.Game.round_number
    return game_state_utils.get_building(building_id).BASE_MAINTENANCE * (1 + round_number * 0.01)

def calculate_upgrade_cost(building_id, num_upgrades):
    """Berechnet die Kosten für ein Upgrade.
    Args:
        building_id (int): GebäudeID
        num_upgrades (int): Nummer des Uprgrades
    Returns:
        int: Kosten für den Bau des Gebäude"""
    round_number = config.Game.round_number
    upgrade_cost = game_state_utils.get_building(building_id).INIT_UPGRADE_PRICE * (1 + num_upgrades * 0.5) * (1 + round_number * 0.02)
    return upgrade_cost

def set_init_ressources():
    """Gibt jedem spieler seine Init Ressources."""
    config.Player.Player1.ressources = config.Player.Player1.INIT_RESSOURCES
    config.Player.Player2.ressources = config.Player.Player2.INIT_RESSOURCES

def increase_resources_per_round(amount, player_id=None):
    """Erhöht die Menge an Ressourcen, die ein Spieler pro Runde bekommt."""
    if player_id is None:
        player_id = config.Game.current_turn + 1
    
    if player_id == config.Player.PlayerID.PLAYER_1:
        config.Player.Player1.ressources_per_round += amount
    if player_id == config.Player.PlayerID.PLAYER_2:
        config.Player.Player2.ressources_per_round += amount

def add_ressources():
    """Gibt den Spielern die Ressourcen, die sie pro Runde kriegen."""
    config.Player.Player1.ressources += config.Player.Player1.ressources_per_round
    config.Player.Player2.ressources += config.Player.Player2.ressources_per_round

def pay_building(building_id, number=None, player_id=None):
    """Zieht dem Spieler der dran ist die Kosten für ein bestimmtes Gebäude ab."""
    if player_id is None:
        player_id = config.Game.current_turn + 1

    if building_id == config.Building.BuildingID.STREET and number is not None:
        cost = calculate_street_building_cost(number)
    else:
        cost = calculate_building_cost(building_id)
    
    if player_id == config.Player.PlayerID.PLAYER_1:
        config.Player.Player1.ressources -= cost
    if player_id == config.Player.PlayerID.PLAYER_2:
        config.Player.Player2.ressources -= cost

