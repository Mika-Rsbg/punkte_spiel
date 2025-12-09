import tkinter as tk
from typing import Tuple, Union

from gui.buttons import ButtonPanel
from gui.labels import ResourceLabel


class Game:
    """Informationen über das Spiel"""
    round_number = 0
    current_turn = 0
    inflation_rate = 0


class GameWindow:
    """Informationen über das Hauptfenster und den Inhalt vom Hauptfenster."""
    buttons: ButtonPanel
    labels: ResourceLabel


class GameGrid:
    """Informationen über das Spielfeld-Raster."""
    GRID_SIZE = 40  # Größe eines Feldes (in Pixel)
    GRID_ROWS = 15  # Anzahl der Zeilen
    GRID_COLS = 40  # Anzahl der Spalten´

    fields = {}  # Speichert die Rechteck-IDs für jedes Feld
    """
        Das Dictionary `fields`, verwalltet die Daten aller Spielfelder.<br>
        Jedes Feld wird durch seine (Spalte, Zeile)-Koordinaten als Schlüssel
        identifiziert<br>
        und enthält folgende Attribute:

        - `rect_id` (int): Die ID des Rechtecks im Canvas, um das Feld
        grafisch darzustellen.
        - `building` (int): Der Gebäudestatus des Feldes
        (0 = nichts, 1 = Dorf, etc.).
        - `team` (int): Der Besitzstatus des Feldes (0 = neutral, 1 = Team 1,
        2 = Team 2).
        <br>
        Beispielzugriff:
        ```# Feld bei Spalte 3, Zeile 2
            field = fields[(3, 2)]
            print(field["building"])  # Gebäudestatus ausgeben
            print(field["team"])      # Besitzstatus ausgeben

        Beispieländerung:
        ```# Feld bei Spalte 3, Zeile 2
            fields[(3, 2)]["building"] = 1  # Setzt ein Dorf auf das Feld
            fields[(3, 2)]["team"] = 1      # Feld gehört jetzt Team 1
    """


class GameCanvas:
    """Canvas-Informationen für das Spielfeld."""
    CANVAS_WIDTH = GameGrid.GRID_SIZE * GameGrid.GRID_COLS + 1
    CANVAS_HEIGHT = GameGrid.GRID_SIZE * GameGrid.GRID_ROWS + 1
    CANVAS_BACKGROUND = "#70ff74"
    canvas: tk.Canvas
    is_field_selected = False
    selected_field: Union[Tuple[int, int], None]
    persistent_highlights = set()  # Speichert persistent hervorgehobene Felder


class Player:
    class PlayerID:
        """Player-IDs für Spieler und Computer."""
        NO_PLAYER = 0  # Kein Player
        PLAYER_1 = 1   # Player 1 (Spieler)
        PLAYER_2 = 2   # Player 2 (Computer)

    class Player1:
        """Informationen über Spieler 1."""
        COLOR = "#0000ff"  # "blue"         "yellow"#ffff00
        """Blau"""
        INIT_RESSOURCES = 1500

        ressources = 0
        ressources_per_round = 5

        number_of_dorfer = 0
        number_of_ressourcenproduktion = 0
        number_of_stadte = 0
        number_of_streets = 0
        streets = []

    class Player2:
        """Informationen über Spieler 2."""
        COLOR = "#ff0000"  # "red"
        """Rot"""
        INIT_RESSOURCES = 15

        ressources = 0
        ressources_per_round = 5

        number_of_dorfer = 0
        number_of_ressourcenproduktion = 0
        number_of_stadte = 0
        number_of_streets = 0
        streets = []


class Building:
    """Informationen zu Gebäuden."""
    class BuildingID:
        """IDs für verschiedene Gebäudetypen."""
        NO_BUILDING = 0
        DORF = 1
        RESSOURCENPRODUKTION = 2
        STADT = 3
        STREET = 4

        HOME = 100

    NUMBER_OF_BUILDING_TYPES = 4
    """Anzahl der platzierbaren Gebäudetypen"""

    class Dorf:
        """Informationen über Dörfer."""
        BUILDING_DESIGNATION = "Dorf"
        RADIUS_DORF = 10
        INIT_BUILDING_PRICE = 10
        INIT_UPGRADE_PRICE = 10
        BUILDING_PRICE_ADJUSTMENT_FACTOR = 0.7
        BASE_MAINTENANCE = 1
        OCCUPATION_RADIUS = 1

    class Ressourcenproduktion:
        """Informationen über Ressourcenproduktionen"""
        BUILDING_DESIGNATION = "Ressourcenproduktion"
        INIT_BUILDING_PRICE = 5
        INIT_UPGRADE_PRICE = 5
        BUILDING_PRICE_ADJUSTMENT_FACTOR = 0.7
        BASE_MAINTENANCE = 1
        INCREASES_RESSOURCEPRODUKTION_BY = 3
        OCCUPATION_RADIUS = 0

    class Stadt:
        """Informationen über Städte."""
        BUILDING_DESIGNATION = "Stadt"
        RADIUS_STADT = 15
        INIT_BUILDING_PRICE = 20
        INIT_UPGRADE_PRICE = 20
        BUILDING_PRICE_ADJUSTMENT_FACTOR = 0.7
        BASE_MAINTENANCE = 1
        OCCUPATION_RADIUS = 2

    class Street:
        """Informationen über Straßen."""
        BUILDING_DESIGNATION = "Straße"
        INIT_BUILDING_PRICE = 1
        INIT_UPGRADE_PRICE = 1
        BUILDING_PRICE_ADJUSTMENT_FACTOR = 1
        BASE_MAINTENANCE = 1
        OCCUPATION_RADIUS = 0

        street_placing_mode = False
        street_start_field: Union[Tuple[int, int], None]
        street_end_field: Union[Tuple[int, int], None]

        preview_streets = []

    class Home:
        """Informationen über Home."""
        OCCUPATION_RADIUS = 3
        place_home_mode = False
        rows_for_placement = 10
        left_player = Player.PlayerID.NO_PLAYER
        right_player = Player.PlayerID.NO_PLAYER


class BuildingMenu:
    """Informationen über das BuildingMenu"""
    class BuildingMenuCanvas:
        """Canvas-Informationen für das Gebäudemenü."""
        # CANVAS_WIDTH = (Grid.GRID_SIZE * Building.NUMBER_OF_BUILDING_TYPES)
        # * 2  + 1 - Grid.GRID_ROWS * 2
        SPACING = GameGrid.GRID_SIZE
        CANVAS_WIDTH = (GameGrid.GRID_SIZE * Building.NUMBER_OF_BUILDING_TYPES
                        + 1 + (Building.NUMBER_OF_BUILDING_TYPES - 1) *
                        SPACING)
        CANVAS_HEIGHT = GameGrid.GRID_SIZE + 1
        CANVAS_BACKGROUND = GameCanvas.CANVAS_BACKGROUND

    class BuildingMenuGrid:
        """Informationen über das Grid des BuildingMenuCanvas"""
        # Anzahl der Zeilen
        GRID_ROWS = 1
        # Anzahl der Spalten
        GRID_COLS = Building.NUMBER_OF_BUILDING_TYPES * 2 - 1

        fields = {}  # Speichert die Rechteck-IDs für jedes Feld
        """
            Das Dictionary `fields`, verwalltet die Daten aller
            Spielfelder.<br>
            Jedes Feld wird durch seine (Spalte, Zeile)-Koordinaten als
            Schlüssel identifiziert<br>
            und enthält folgende Attribute:

            - `rect_id` (int): Die ID des Rechtecks im Canvas, um das Feld
            grafisch darzustellen.
            - `building` (int): Der Gebäudestatus des Feldes (0 = nichts,
            1 = Dorf, etc.).
            - `team` (int): Der Besitzstatus des Feldes (0 = neutral,
            1 = Team 1, 2 = Team 2).
            <br>
            Beispielzugriff:
            ```# Feld bei Spalte 3, Zeile 2
                field = fields[(3, 2)]
                print(field["building"])  # Gebäudestatus ausgeben
                print(field["team"])      # Besitzstatus ausgeben

            Beispieländerung:
            ```# Feld bei Spalte 3, Zeile 2
                fields[(3, 2)]["building"] = 1  # Setzt ein Dorf auf das Feld
                fields[(3, 2)]["team"] = 1      # Feld gehört jetzt Team 1
        """

    is_field_selected = False
    selected_field = ()
    building_costs = 0
    building_duration = 0


class Design:
    class Fonts:
        """Font-Presets"""
        HEADING_1 = ("Arial", 24, "bold")
        HEADING_2 = ("Arial", 20, "bold")
        HEADING_3 = ("Arial", 16, "bold")
        PARAGRAPH_1 = ("Arial", 14)
        PARAGRAPH_2 = ("Arial", 12)
        PARAGRAPH_3 = ("Arial", 10, "italic")
        BUTTON_TEXT = ("Arial", 12, "bold")
        INPUT_TEXT = ("Courier", 12)

    class Colors:
        """Farb-Presets"""
        PRIMARY = "#40bb45"
        """Grün"""
        SECONDARY = "#2196F3"
        """Blau"""
        DANGER = "#ff0000"
        """Rot"""
        WARNING = "#FFC107"
        """Gelb"""
        INFO = "#00d0ef"
        """Türkis"""
        LIGHT = "#d8dee3"
        """Hellgrau"""
        DARK = "#43494e"
        """Dunkelgrau"""
        TEXT_PRIMARY = "#000000"
        """Standardtextfarbe (Schwarz)"""
        TEXT_SECONDARY = "#6C757D"
        """Sekundärtextfarbe (Grau)"""

    # class MenuLabels:
    #     # Design-Presets für Labels
    #     HEADING_1 = {"font": Fonts.HEADING_1, "fg": Colors.TEXT_PRIMARY}
    #     HEADING_2 = {"font": Fonts.HEADING_2, "fg": Colors.TEXT_PRIMARY}
    #     HEADING_3 = {"font": Fonts.HEADING_3, "fg": Colors.TEXT_SECONDARY}
    #     PARAGRAPH_1 = {"font": Fonts.PARAGRAPH_1, "fg": Colors.TEXT_PRIMARY}
        # PARAGRAPH_2 = {"font": Fonts.PARAGRAPH_2,
        #                "fg": Colors.TEXT_SECONDARY}
        # PARAGRAPH_3 = {"font": Fonts.PARAGRAPH_3,
        #                "fg": Colors.TEXT_SECONDARY}

    # class Buttons:
    #     # Design-Presets für Buttons
        # PRIMARY = {"font": Fonts.BUTTON_TEXT, "bg": Colors.PRIMARY,
        #            "fg": "white"}
        # SECONDARY = {"font": Fonts.BUTTON_TEXT, "bg": Colors.SECONDARY,
        #              "fg": "white"}
        # DANGER = {"font": Fonts.BUTTON_TEXT, "bg": Colors.DANGER,
        #           "fg": "white"}
        # WARNING = {"font": Fonts.BUTTON_TEXT, "bg": Colors.WARNING,
        #            "fg": "black"}
        # INFO = {"font": Fonts.BUTTON_TEXT, "bg": Colors.INFO,
        #         "fg": "white"}

    # class Entries:
    #     # Design-Presets für Entry-Felder
        # DEFAULT = {"font": Fonts.INPUT_TEXT, "bg": Colors.LIGHT,
        #            "fg": Colors.TEXT_PRIMARY, "highlightthickness": 1,
        #            "highlightbackground": Colors.DARK}

    # class Frames:
    #     # Design-Presets für Frames
    #     DEFAULT = {"bg": Colors.LIGHT, "bd": 2, "relief": "solid"}
    #     PRIMARY = {"bg": Colors.PRIMARY, "bd": 2, "relief": "ridge"}
    #     SECONDARY = {"bg": Colors.SECONDARY, "bd": 2, "relief": "groove"}

###############################################################
###############################################################
###############################################################
###############################################################
# Einheitliche Bennenung der felder in fields
###############################################################
###############################################################
###############################################################
###############################################################
