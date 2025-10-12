import config

def execute_function_by_building_id(building_id, dorf_function, ressourcenproduktion_function, stadt_function, street_function):
    """Identifiziert ein Gebäude anhand der GebäudeID und führt entsprechende Funktionen aus.
    Args:
        building_id (int): GebäudeID des Gebäudes.
        dorf_function (function): Funktion, die bei einem Dorf ausgeführt wird.
        ressourcenproduktion_function (function): Funktion, die bei einer Ressourcenproduktion ausgeführt wird.
        stadt_function (function): Funktion, die bei einer Stadt ausgeführt wird.
        street_function (function): Funktion, die bei einer Straße ausgeführt wird.
    Returns:
        str | None: Die Bezeichnung des Gebäudes, falls keine Funktionen übergeben wurden, oder None.
    """
    if building_id == config.Building.BuildingID.DORF:
        return dorf_function()

    if building_id == config.Building.BuildingID.RESSOURCENPRODUKTION:
        return ressourcenproduktion_function()

    if building_id == config.Building.BuildingID.STADT:
        return stadt_function()

    if building_id == config.Building.BuildingID.STREET:
        return street_function()
    
    # Fallback, wenn building_number ungültig ist
    raise ValueError(f"Ungültige GebäudeID: {building_id}")

def execute_function_from_fields(fields, col, row, dorf_function, ressourcenproduktion_function, stadt_function, street_function):
    """Identifiziert ein Gebäude anhand der Felddaten und führt entsprechende Funktionen aus.
    Args:
        fields (dict): Dictionary mit Felddaten.
        col (int): Spaltenindex des Feldes.
        row (int): Zeilenindex des Feldes.
        dorf_function (function): Funktion, die bei einem Dorf ausgeführt wird.
        ressourcenproduktion_function (function): Funktion, die bei einer Ressourcenproduktion ausgeführt wird.
        stadt_function (function): Funktion, die bei einer Stadt ausgeführt wird.
        street_function (function): Funktion, die bei einer Straße ausgeführt wird.
    Returns:
        str | None: Die Bezeichnung des Gebäudes, falls keine Funktionen übergeben wurden, oder None.
    """
    try:
        building_id = fields[(col, row)]["building"]
        if building_id == config.Building.BuildingID.DORF:
            return dorf_function()

        if building_id == config.Building.BuildingID.RESSOURCENPRODUKTION:
            return ressourcenproduktion_function()

        if building_id == config.Building.BuildingID.STADT:
            return stadt_function()

        if building_id == config.Building.BuildingID.STREET:
            return street_function()

        # Fallback, wenn building_number ungültig ist
        raise ValueError(f"Ungültige GebäudeID: {building_id}")
    except KeyError:
        raise ValueError(f"Ungültige Felddaten: Kein Gebäude bei Koordinaten ({col}, {row}) gefunden.")

def get_neighbor_coordinates(col, row, direction):
    """Berechnet die Koordinaten des Nachbarn basierend auf der aktuellen Zelle und einer Richtung.

    Args:
        col (int): Die Spalte der aktuellen Zelle.
        row (int): Die Zeile der aktuellen Zelle.
        direction (str): Die Richtung, in die der Nachbar liegt.<br>
                         Zulässige Werte: `"N", "NE", "E", "SE", "S", "SW", "W", "NW"`.

    Returns:
        tuple ([int, int]): Die Spalte und Zeile des Nachbarn.
    """
    direction_map = {
        "N": (0, -1),   # Norden: Gleiche Spalte, eine Zeile nach oben
        "NE": (1, -1),  # Nord-Osten: Eine Spalte nach rechts, eine Zeile nach oben
        "E": (1, 0),    # Osten: Eine Spalte nach rechts, gleiche Zeile
        "SE": (1, 1),   # Süd-Osten: Eine Spalte nach rechts, eine Zeile nach unten
        "S": (0, 1),    # Süden: Gleiche Spalte, eine Zeile nach unten
        "SW": (-1, 1),  # Süd-Westen: Eine Spalte nach links, eine Zeile nach unten
        "W": (-1, 0),   # Westen: Eine Spalte nach links, gleiche Zeile
        "NW": (-1, -1)  # Nord-Westen: Eine Spalte nach links, eine Zeile nach oben
    }

    if direction not in direction_map:
        raise ValueError(f"Ungültige Richtung: {direction}")

    d_col, d_row = direction_map[direction]
    return col + d_col, row + d_row

def is_neighbour(center_field, check_field):
    """Überprüft, ob ein Feld ein Nachbarfeld eines zentralen Feldes ist.

    Args:
        center_field (tuple): Die Koordinaten des zentralen Feldes als (Spalte, Zeile).
        check_field (tuple): Die Koordinaten des zu überprüfenden Feldes als (Spalte, Zeile).

    Returns:
        bool: True, wenn `check_field` ein Nachbarfeld von `center_field` ist, andernfalls False.
    """
    center_col, center_row = center_field
    check_col, check_row = check_field

    # Die Differenz zwischen den Spalten- und Zeilenwerten berechnen
    col_diff = abs(center_col - check_col)
    row_diff = abs(center_row - check_row)

    # Ein Feld ist ein Nachbarfeld, wenn es maximal 1 Feld entfernt ist
    return col_diff <= 1 and row_diff <= 1 and (col_diff != 0 or row_diff != 0)
    