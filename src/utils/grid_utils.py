from typing import Tuple
import config

def get_grid_coordinates(x, y, grid_size=config.GameGrid.GRID_SIZE, rows=config.GameGrid.GRID_ROWS, cols=config.GameGrid.GRID_COLS) -> Tuple[int, int] | None:
    """Berechnet die Spalten- und Zeilenposition im Raster basierend auf Pixelkoordinaten.
    Args:
        x (int): X-Koordinate in Pixeln.
        y (int): Y-Koordinate in Pixeln.
        grid_size (int, optional): Größe eines Rasters in Pixeln. Defaults to `config.Grid.GRID_SIZE`.
        rows (int, optional): Anzahl der Zeilen. Defaults to `config.Grid.GRID_ROWS`.
        cols (int, optional): Anzahl der Spalten. Defaults to `config.Grid.GRID_COLS`.
    Returns:
        tuple: (Spalte, Zeile) im Raster, oder None, wenn die Koordinaten außerhalb des Rasters liegen."""
    # Berechne die Spalte und Zeile basierend auf den Pixelkoordinaten
    col = int(x / grid_size)
    row = int(y / grid_size)

    # Prüfe, ob die Koordinaten innerhalb des gültigen Bereichs liegen
    if 0 <= col < cols and 0 <= row < rows:
        return col, row
    else:
        return None  # Außerhalb des Grids

def get_building_id(field_coords, fields=config.GameGrid.fields):
    """Liefert die GebäudeID des Feldes bei den angegebenen Koordinaten.
    Args:
        field_coords (tuple): Die Koordinaten des Feldes als (Spalte, Zeile).
        fields (dict, optional): Dictionary in dem die Felder eines Grids gespeichert sind. Defaults to `config.Grid.fields`
    Returns:
        int: Der GebäudeID des Feldes:
            - 0 = kein Gebäude
            - 1 = Dorf
            - etc."""
    return fields.get(field_coords, {}).get("building", 0)

def check_sorounding(col=None, row=None, field_coords=None, fields=None):
    if fields is None:
        fields = config.GameGrid.fields
    if col is None or row is None:
        col, row = field_coords
    
    rows = [row -1, row, row + 1]
    colums = [col - 1, col, col +1]

    for row_1 in rows:
        for col_1 in colums:
            if fields[field_coords]["connect_to"] == config.Game.current_turn + 1:
                config.Building.Street.fields_to_connect.append((col, row))
###############################################################
###############################################################
# Documetation
###############################################################
###############################################################

def home_can_be_placed(col=None, row=None, field_coords=None):
    """Überprüft, ob ein Gebäude (z. B. 'Home') an einer bestimmten Position platziert werden kann.

    Args:
        col (int, optional): Spaltenkoordinate des Feldes. Defaults to None.
        row (int, optional): Zeilenkoordinate des Feldes. Defaults to None.
        field_coords (tuple, optional): Tuple mit (Spalte, Zeile). Defaults to None.

    Returns:
        bool: True, wenn das Gebäude platziert werden kann, andernfalls False."""
    # Wenn `field_coords` angegeben ist, extrahiere `col` und `row`
    if field_coords is not None:
        col, row = field_coords

    # Sicherstellen, dass `col` und `row` angegeben sind
    if col is None or row is None:
        raise ValueError("Spalten- und Zeilenkoordinaten ('col', 'row') müssen angegeben werden.")

    # Erlaubte Bereiche berechnen
    left_bound = config.Building.Home.rows_for_placement  # Linke Platzierungsgrenze
    right_bound = config.GameGrid.GRID_COLS - config.Building.Home.rows_for_placement  # Rechte Platzierungsgrenze

    # Prüfen, ob beide Seiten frei sind
    if config.Building.Home.left_player == 0 and config.Building.Home.right_player == 0:
        return col < left_bound or col >= right_bound

    # Prüfen, ob nur die linke Seite frei ist
    if config.Building.Home.left_player == 0 and config.Building.Home.right_player != 0:
        return col < left_bound

    # Prüfen, ob nur die rechte Seite frei ist
    if config.Building.Home.left_player != 0 and config.Building.Home.right_player == 0:
        return col >= right_bound

    # Wenn beide Seiten besetzt sind, ist keine Platzierung möglich
    return False
