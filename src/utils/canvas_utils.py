import tkinter as tk
from typing import Tuple, Union

import config
import utils.game_state_utils as game_state_utils

def highlight_field(canvas, col=None, row=None, color="lightgray", fields=config.GameGrid.fields, field_coords=None):
    """Markiert ein Feld mit einer Farbe, überschreibt persistente Highlights temporär.
    
    Args:
        canvas (tk.Canvas): Spiel-Canvas.
        col (int, optional): Spalten-Koordinate des Feldes. Defaults to None.
        row (int, optional): Zeilen-Koordinate des Feldes. Defaults to None.
        color (str, optional): Farbe. Defaults to "lightgray".
        fields (dict): Dictionary mit Feldinformationen.
        field_coords (tuple): Koordinaten des Feldes. Defaults to None.
    """
    # Feld-Koordinaten berechnen
    if field_coords is None:
        if col is None or row is None:
            raise ValueError("Entweder 'field_coords' oder 'col' und 'row' müssen angegeben werden.")
        field_coords = (col, row)

    rect_id = fields[field_coords]["rect_id"]
    canvas.itemconfig(rect_id, fill=color)

def clear_field(canvas, col=None, row=None, fields=config.GameGrid.fields, field_coords=None):
    """Setzt die Farbe eines spezifischen Feldes zurück.
    
    Args:
        canvas (tk.Canvas): Spiel-Canvas.
        col (int, optional): Spalten-Koordinate des Feldes. Defaults to None.
        row (int, optional): Zeilen-Koordinate des Feldes. Defaults to None.
        fields (dict): Dictionary mit Feldinformationen.
        field_coords (tuple): Koordinaten des Feldes. Defaults to None.
    """
    # Feld-Koordinaten berechnen
    if field_coords is None:
        if col is None or row is None:
            raise ValueError("Entweder 'field_coords' oder 'col' und 'row' müssen angegeben werden.")
        field_coords = (col, row)

    rect_id = fields[field_coords]["rect_id"]
    
    # Wenn eine persistente Farbe vorhanden ist, stelle diese wieder her
    persistent_color = fields[field_coords].get("persistent_color")
    if persistent_color:
        canvas.itemconfig(rect_id, fill=persistent_color)
    else:
        canvas.itemconfig(rect_id, fill=config.GameCanvas.CANVAS_BACKGROUND)

def clear_all_fields(canvas, rows=None, cols=None, fields=config.GameGrid.fields):
    """Setzt die Farbe aller Felder zurück.
    Args:
        canvas (parameter): Spiel Canvas
        rows (int, optional): Anzahl der Zeilen. Defaults to None.
        cols (int, optional): Anzahl der Spalten. Defaults to None.
        fields (dict, optional): Dictionary in dem die Felder eines Grids gespeichert sind. Defaults to `config.Grid.fields`
    """
    if rows is None and cols is None:
        rows = config.GameGrid.GRID_ROWS
        cols = config.GameGrid.GRID_COLS
    for row in range(rows):
        for col in range(cols):
            rect_id = fields[(col, row)]["rect_id"]
            # Wenn eine persistente Farbe vorhanden ist, stelle diese wieder her
            persistent_color = fields[(col, row)].get("persistent_color")
            if persistent_color:
                canvas.itemconfig(rect_id, fill=persistent_color)
            else:
                canvas.itemconfig(rect_id, fill=config.GameCanvas.CANVAS_BACKGROUND)

def persistent_highlight_field(canvas, col=None, row=None, color=None, fields=config.GameGrid.fields, field_coords=None, transparently=True, alpha=0.5):
    """Markiert ein Feld dauerhaft mit einer Farbe.
    
    Args:
        canvas (tk.Canvas): Spiel-Canvas.
        col (int, optional): Spalten-Koordinate des Feldes. Defaults to None.
        row (int, optional): Zeilen-Koordinate des Feldes. Defaults to None.
        color (str, optional): Farbe. Defaults to "lightblue".
        fields (dict): Dictionary mit Feldinformationen.
        field_coords (tuple): Koordinaten des Feldes. Defaults to None.
        transparently (bool): Soll das Feldt halbtransparent makiert werden. Defaults to `True`.
    """
    # Feld-Koordinaten berechnen
    if field_coords is None:
        if col is None or row is None:
            raise ValueError("Entweder 'field_coords' oder 'col' und 'row' müssen angegeben werden.")
        field_coords = (col, row)
    if color is None:
        if transparently:
            original_color = canvas["background"]
            color = game_state_utils.get_player_color()
            # Mischung der Farben erstellen (Transparenz simulieren)
            blended_color = blend_colors(original_color, color, alpha)
        else:
            blended_color = game_state_utils.get_player_color()

    rect_id = fields[field_coords]["rect_id"]
    
    # Markiere das Feld und speichere die persistente Farbe
    canvas.itemconfig(rect_id, fill=blended_color)
    fields[field_coords]["persistent_color"] = blended_color

def clear_persistent_highlight(canvas, field_to_remove, fields_to_remove=None, fields=config.GameGrid.fields):
    """Entfernt spezifische Felder aus der Liste der persistent hervorgehobenen Felder, falls sie enthalten sind.
    Args:
        canvas (parameter): Spiel Canvas.
        field_to_remove (tuple): Koordintaten des Feldes, das entfernt werden soll.
        fields_to_remove (list of tuple): Liste der Koordinaten der Felder, die entfernt werden sollen, z. B. [(col1, row1), (col2, row2)].
        fields (dict, optional): Dictionary mit den Feldern des Grids. Defaults to `config.GameGrid.fields`.
    """
    if fields_to_remove is None:
        fields_to_remove = [field_to_remove]
    for field_coords in fields_to_remove:
        if field_coords in fields:
            rect_id = fields[field_coords]["rect_id"] if isinstance(fields[field_coords], dict) else fields[field_coords]
            # Wenn das Feld in persistent_highlights enthalten ist, zurücksetzen und entfernen
            if not fields[field_coords]["persistent_color"] is None:
                canvas.itemconfig(rect_id, fill=config.GameCanvas.CANVAS_BACKGROUND)
                config.GameGrid.fields[field_coords]["persistent_color"] = None

def clear_all_persistent_highlights(canvas, rows=None, cols=None, fields=config.GameGrid.fields):
    """Entfernt alle persistent hervorgehobenen Felder.
    Args:
        canvas (parameter): Spiel Canvas
        rows (int, optional): Anzahl der Zeilen. Defaults to None.
        cols (int, optional): Anzahl der Spalten. Defaults to None.
        fields (dict, optional): Dictionary in dem die Felder eines Grids gespeichert sind. Defaults to `config.Grid.fields`
    """
    if rows is None and cols is None:
        rows = config.GameGrid.GRID_ROWS
        cols = config.GameGrid.GRID_COLS
    for row in range(rows):
        for col in range(cols):
            rect_id = fields[(col, row)]["rect_id"]
            # Wenn eine persistente Farbe vorhanden ist, stelle diese wieder her
            persistent_color = fields[(col, row)].get("persistent_color")
            if persistent_color:
                canvas.itemconfig(rect_id, fill=config.GameCanvas.CANVAS_BACKGROUND)

def transparently_highlight_field(canvas, col=None, row=None, color=config.Design.Colors.LIGHT, alpha=0.5, fields=config.GameGrid.fields, field_coords=None):
    """Markiert ein Feld an den angegebenen Grid-Koordinaten mit einer halbtransparenten Färbung.
    
    Args:
        canvas (tk.Canvas): Spiel-Canvas.
        col (int, optional): Spalten-Koordinate des Feldes. Defaults to None.
        row (int, optional): Zeilen-Koordinate des Feldes. Defaults to None.
        color (str, optional): Farbe im HEX-Format. Defaults to `config.Design.Colors.LIGHT` (LightGray).
        alpha (float, optional): Transparenzwert zwischen 0 (komplett transparent) und 1 (voll deckend). Defaults to 0.5.
        fields (dict, optional): Dictionary mit Feldern des Grids. Defaults to config.GameGrid.fields.
        field_coords (tuple, optional): Koordinaten des Feldes als (Spalte, Zeile). Defaults to None.
    """
    if field_coords is None:
        if col is None or row is None:
            raise ValueError("Entweder 'field_coords' oder 'col' und 'row' müssen angegeben werden.")
        field_coords = (col, row)

    # Holen der Rechteck-ID des Feldes
    rect_id = fields[field_coords]["rect_id"] if isinstance(fields[field_coords], dict) else fields[field_coords]
    
    # Ursprüngliche Füllfarbe des Rechtecks ermitteln
    original_color = canvas.itemcget(rect_id, "fill")
    if original_color == "":  # Kein ursprünglicher Füllwert (Standardfarbe)
        original_color = canvas["background"]
    
    # Mischung der Farben erstellen (Transparenz simulieren)
    blended_color = blend_colors(original_color, color, alpha)
    
    # Rechteck mit der gemischten Farbe aktualisieren
    canvas.itemconfig(rect_id, fill=blended_color)

def blend_colors(bg_color, fg_color, alpha):
    """Mischt zwei Farben basierend auf einem Alpha-Wert.
    
    Args:
        bg_color (str): Hintergrundfarbe im HEX-Format.
        fg_color (str): Vordergrundfarbe im HEX-Format.
        alpha (float): Transparenzwert (0 = vollständig durchsichtig, 1 = vollständig deckend).
    
    Returns:
        str: Gemischte Farbe im HEX-Format."""
    # HEX zu RGB konvertieren
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    # RGB zu HEX konvertieren
    def rgb_to_hex(rgb_color):
        return "#{:02x}{:02x}{:02x}".format(*rgb_color)
    
    bg_rgb = hex_to_rgb(bg_color)
    fg_rgb = hex_to_rgb(fg_color)
    
    # Farben mischen
    blended_rgb = tuple(
        int(bg_rgb[i] * (1 - alpha) + fg_rgb[i] * alpha)
        for i in range(3)
    )
    
    return rgb_to_hex(blended_rgb)


class draw:
    """Funktionen zum zeichen auf den Canvas"""
    @staticmethod
    # Fixme
    def draw_dorf(canvas, x: int, y: int, col: int, row: int,
                  field_coords: Union[Tuple[int, int], None] = None,
                  color: str = "",
                  radius: int = config.Building.Dorf.RADIUS_DORF,
                  grid_size: int = config.GameGrid.GRID_SIZE):
        """Zeichnet ein Dorf als Kreis auf dem Spielfeld-Canvas.
        Args:
            canvas (tk.Canvas): Das Tkinter Canvas-Objekt, auf dem das
                Dorf gezeichnet wird.
            x (int, optional): Die x-Koordinate des Mittelpunktes des Kreises.
                Defaults to None.
            y (int, optional): Die y-Koordinate des Mittelpunktes des Kreises.
                Defaults to None.
            col (int, optional): Die Spaltennummer des Feldes, auf dem das
                Dorf liegt. Defaults to None.
            row (int, optional): Die Zeilennummer des Feldes, auf dem das
                Dorf liegt. Defaults to None.
            field_coords (tuple): Die Koordinaten des Feldes als
                (Spalte, Zeile). Defaults to None
            color (str): Die Farbe des Kreises, z.B. "red", "green", etc.
                Defaults to None.
            radius (int, optional): Der Radius des Kreises.
                Defaults to `config.Dorf.RADIUS_DORF`.
        Returns:
            int: Die ID des gezeichneten Objekts im Canvas, die verwendet
                werden kann, um das Objekt später zu manipulieren."""
        if color == "":
            color = game_state_utils.get_player_color(config.Game.current_turn)
        if field_coords is not None:
            col, row = field_coords

        # Generiere eindeutige Tags basierend auf den Koordinaten
        tags = "dorf"

        if x is None and y is None:
            x1, y1 = col * grid_size + 2, row * grid_size + 2
            x2, y2 = x1 + grid_size, y1 + grid_size

            x = (x1 + x2) / 2
            y = (y1 + y2) / 2

        # Zeichne den Kreis
        return canvas.create_oval(
            x - radius, y - radius, x + radius, y + radius, fill=color,
            tags=tags
        )

    def draw_ressourcenproduktion(canvas, x=None, y=None, col=None, row=None, field_coords=None, color=None, grid_size=config.GameGrid.GRID_SIZE):
        """Zeichnet eine Ressourcenproduktion als Quadrat auf dem Spielfeld-Canvas.
        Args:
            canvas (tk.Canvas): Das Tkinter Canvas-Objekt, auf dem das Dorf gezeichnet wird.
            x (int, optional): Die x-Koordinate des Mittelpunktes des Quadrat. Defaults to None.
            y (int, optional): Die y-Koordinate des Mittelpunktes des Quadrat. Defaults to None.
            col (int, optional): Die Spaltennummer des Feldes, auf dem die Ressourcenproduktion liegt. Defaults to None.
            row (int, optional): Die Zeilennummer des Feldes, auf dem die Ressourcenproduktion liegt. Defaults to None.
            field_coords (tuple): Die Koordinaten des Feldes als (Spalte, Zeile). Defaults to None
            color (str): Die Farbe des Quadrat, z.B. "red", "green", etc. Defaults to None.
        Returns:
            int: Die ID des gezeichneten Objekts im Canvas, die verwendet werden kann, um das Objekt später zu manipulieren."""
        if color == None:
            color = game_state_utils.get_player_color(config.Game.current_turn)
        if not field_coords is None:
            col, row = field_coords
            
        # Generiere eindeutige Tags basierend auf den Koordinaten
        tags = "ressource"

        if x is None and y is None:
            x1, y1 = col * grid_size + 2, row * grid_size + 2
            x2, y2 = x1 + grid_size, y1 + grid_size
            
            x = (x1 + x2) / 2
            y = (y1 + y2) / 2
        
        # Zeichne das Quadrat
        return canvas.create_rectangle(x - 10, y - 10, x + 10, y + 10, fill=color, tags=tags)
    
    def draw_stadt(canvas, x=None, y=None, col=None, row=None, field_coords=None, color=None, radius=config.Building.Stadt.RADIUS_STADT, grid_size=config.GameGrid.GRID_SIZE):
        """Zeichnet eine Stadt als Kreis auf dem Spielfeld-Canvas.
        Args:
            canvas (tk.Canvas): Das Tkinter Canvas-Objekt, auf dem das Dorf gezeichnet wird.
            x (int, optional): Die x-Koordinate des Mittelpunktes des Kreises. Defaults to None.
            y (int, optional): Die y-Koordinate des Mittelpunktes des Kreises. Defaults to None.
            col (int, optional): Die Spaltennummer des Feldes, auf dem die Stadt liegt. Defaults to None.
            row (int, optional): Die Zeilennummer des Feldes, auf dem die Stadt liegt. Defaults to None.
            field_coords (tuple): Die Koordinaten des Feldes als (Spalte, Zeile). Defaults to None
            color (str): Die Farbe des Kreises, z.B. "red", "green", etc. Defaults to None.
            radius (int, optional): Der Radius des Kreises. Defaults to `config.Stadt.RADIUS_STADT`.
        Returns:
            int: Die ID des gezeichneten Objekts im Canvas, die verwendet werden kann, um das Objekt später zu manipulieren."""
        if color is None:
            color = game_state_utils.get_player_color(config.Game.current_turn)
        if not field_coords is None:
            col, row = field_coords
        # Generiere eindeutige Tags basierend auf den Koordinaten
        tags = "stadt"

        if x is None and y is None:
            x1, y1 = col * grid_size + 2, row * grid_size + 2
            x2, y2 = x1 + grid_size, y1 + grid_size
            
            x = (x1 + x2) / 2
            y = (y1 + y2) / 2

        # Zeichne den Kreis
        return canvas.create_oval(x - radius, y - radius,
                                    x + radius, y + radius,
                                    fill=color, tags=tags)
    
    def draw_road(canvas, start_coords, end_coords, thickness=8, outline_color=None, grid_size=config.GameGrid.GRID_SIZE, color=None):
        """Zeichnet eine Straße als dicken Strich von der Mitte eines Feldes zur Mitte eines benachbarten Feldes.
        
        Args:
            canvas (tk.Canvas): Das Tkinter Canvas-Objekt, auf dem die Straße gezeichnet wird.
            start_coords (tuple): Die (Spalte, Zeile) des Startfeldes.
            end_coords (tuple): Die (Spalte, Zeile) des Endfeldes.
            thickness (int): Die Dicke der Straße. Defaults to 8.
            color (str): Die Farbe der Straße. Defaults to "gray".
            grid_size (int): Die Größe eines Feldes im Raster. Defaults to `config.GameGrid.GRID_SIZE`.

        Returns:
            tuple: Die IDs der gezeichneten Objekte (Outline, Linie).
        """
        if color is None:
            color = "gray"
        if outline_color is None:
            outline_color = game_state_utils.get_player_color(config.Game.current_turn)
        start_col, start_row = start_coords
        end_col, end_row = end_coords

        # Berechnung der Mittelpunkte der Felder
        start_x_center = start_col * grid_size + grid_size / 2
        start_y_center = start_row * grid_size + grid_size / 2
        end_x_center = end_col * grid_size + grid_size / 2
        end_y_center = end_row * grid_size + grid_size / 2

        # Verschiebung basierend auf der Richtung der Linie
        if start_row == end_row:  # Horizontale Linie
            start_x = start_x_center
            end_x = end_x_center
            start_y = start_y_center + 2.25
            end_y = end_y_center + 2.25
            thickness = thickness
            outline_thickness = thickness + 4
        elif start_col == end_col:  # Vertikale Linie
            start_x = start_x_center + 2.25
            end_x = end_x_center + 2.25
            start_y = start_y_center
            end_y = end_y_center
            thickness = thickness
            outline_thickness = thickness + 4
        else:
            start_x = start_x_center + 2.25
            end_x = end_x_center + 2.25
            start_y = start_y_center + 3
            end_y = end_y_center + 3
            thickness = thickness - 1
            outline_thickness = thickness + 5

        # Zeichne die Hintergrundlinie (als "Outline")
        outline_id = None
        if outline_color:
            outline_id = canvas.create_line(
                start_x, start_y, end_x, end_y,
                fill=outline_color, width=outline_thickness, tags="road_outline"
            )

        # Zeichne die Vordergrundlinie (Straße)
        line_id = canvas.create_line(
            start_x, start_y, end_x, end_y,
            fill=color, width=thickness, tags="road"
        )

        return (outline_id, line_id)

    # def draw_road_segment(canvas, col, row, direction, thickness=8, outline_color=None, color=None):
        """Zeichnet einen Straßenabschnitt innerhalb eines Feldes basierend auf der Richtung.

        Args:
            canvas (tk.Canvas): Das Tkinter Canvas-Objekt.
            col (int): Die Spalte des Feldes.
            row (int): Die Zeile des Feldes.
            direction (str): Die Richtung der Straße (z.B. "N", "NE", etc.).
            thickness (int): Die Dicke der Straße.
            outline_color (str): Die Farbe der Straßenkontur.
            color (str): Die Farbe der Straße.

        Returns:
            tuple: Die IDs der gezeichneten Objekte (Outline, Linie).
        """
        if color is None:
            color = "gray"
        if outline_color is None:
            outline_color = game_state_utils.get_player_color(config.Game.current_turn)

        grid_size = config.GameGrid.GRID_SIZE
        
        direction_offsets = {
            "N": (0, -1),
            "NE": (1, -1),
            "E": (1, 0),
            "SE": (1, 1),
            "S": (0, 1),
            "SW": (-1, 1),
            "W": (-1, 0),
            "NW": (-1, -1)
        }
        do_col, do_row = direction_offsets[direction]
        end_col = col + do_col
        end_row = row + do_row

        # Berechnung der Mittelpunkte der Felder
        start_x_center = col * grid_size + grid_size / 2
        start_y_center = col * grid_size + grid_size / 2
        end_x_center = end_col * grid_size
        end_y_center = end_row * grid_size

        # Verschiebung basierend auf der Richtung der Linie
        if direction in ["W", "E"]:  # Horizontale Linie
            return None
            # start_x = start_x_center
            # if direction == "W":
            #     end_x = end_x_center + grid_size * 1.2
            # elif direction == "E":
            #     end_x = end_x_center - grid_size * 0.2
            # start_y = start_y_center + 2.25
            # end_y = end_y_center + 2.25
            # thickness = thickness
            # outline_thickness = thickness + 4
        elif direction in ["N", "S"]:  # Vertikale Linie
            return None
            # start_x = start_x_center + 2.25
            # end_x = end_x_center + 2.25
            # start_y = start_y_center
            # if direction == "N":
            #     end_y = end_y_center + grid_size * 1.2
            # elif direction == "S":
            #     end_y = end_y_center - grid_size * 0.2
            # thickness = thickness
            # outline_thickness = thickness + 4
        else:
            return None
            # start_x = start_x_center + 2.25
            # start_y = start_y_center + 3
            # if direction == "NE":
            #     end_x = end_x_center - grid_size * 0.2
            #     end_y = end_y_center + grid_size * 1.2
            # elif direction == "SE":
            #     end_x = end_x_center - grid_size * 0.2
            #     end_y = end_y_center - grid_size * 0.2
            # if direction == "SW":
            #     end_x = end_x_center + grid_size * 1.2
            #     end_y = end_y_center - grid_size * 0.2
            # elif direction == "NW":
            #     end_x = end_x_center + grid_size * 1.2
            #     end_y = end_y_center + grid_size * 1.2
            # thickness = thickness - 1
            # outline_thickness = thickness + 5

        # Zeichne die Hintergrundlinie (als "Outline")
        outline_id = canvas.create_line(
            start_x, start_y, end_x, end_y,
            fill=outline_color, width=outline_thickness, tags="road_outline"
        )

        # Zeichne die Vordergrundlinie (Straße)
        line_id = canvas.create_line(
            start_x, start_y, end_x, end_y,
            fill=color, width=thickness, tags="road"
        )

        return (outline_id, line_id)

    def draw_road_segment(canvas, col, row, direction, thickness=8, outline_color=None, color=None):
        """Zeichnet einen Straßenabschnitt innerhalb eines Feldes basierend auf der Richtung.

        Args:
            canvas (tk.Canvas): Das Tkinter Canvas-Objekt.
            col (int): Die Spalte des Feldes.
            row (int): Die Zeile des Feldes.
            direction (str): Die Richtung der Straße (z.B. "N", "NE", etc.).
            thickness (int): Die Dicke der Straße.
            outline_color (str): Die Farbe der Straßenkontur.
            color (str): Die Farbe der Straße.

        Returns:
            tuple: Die IDs der gezeichneten Objekte (Outline, Linie).
        """
        if color is None:
            color = "gray"
        if outline_color is None:
            outline_color = game_state_utils.get_player_color(config.Game.current_turn)

        grid_size = config.GameGrid.GRID_SIZE

        # Richtungen und ihre Verschiebungen
        direction_offsets = {
            "N": (0, -1),
            "NE": (1, -1),
            "E": (1, 0),
            "SE": (1, 1),
            "S": (0, 1),
            "SW": (-1, 1),
            "W": (-1, 0),
            "NW": (-1, -1)
        }

        # Berechnung der Endposition basierend auf der Richtung
        do_col, do_row = direction_offsets[direction]
        end_col = col + do_col
        end_row = row + do_row

        # Berechnung der Mittelpunkte des Start- und Endfeldes
        start_x_center = col * grid_size + grid_size / 2
        start_y_center = row * grid_size + grid_size / 2
        end_x_center = end_col * grid_size + grid_size / 2
        end_y_center = end_row * grid_size + grid_size / 2

        # Berechnung der Start- und Endpunkte für die Linie
        start_x = start_x_center
        start_y = start_y_center
        end_x = end_x_center
        end_y = end_y_center

        # Horizontale und vertikale Verschiebungen für die Linie
        if direction in ["W", "E"]:  # Horizontale Linie
            start_y += 2.25
            end_y += 2.25
        elif direction in ["N", "S"]:  # Vertikale Linie
            start_x += 2.25
            end_x += 2.25
        elif direction in ["NE", "SE", "SW", "NW"]:  # Diagonale Linien
            start_x += 2.25
            start_y += 3

        # Zeichne die Hintergrundlinie (als "Outline")
        outline_id = canvas.create_line(
            start_x, start_y, end_x, end_y,
            fill=outline_color, width=thickness + 4, tags="road_outline"
        )

        # Zeichne die Vordergrundlinie (Straße)
        line_id = canvas.create_line(
            start_x, start_y, end_x, end_y,
            fill=color, width=thickness, tags="road"
        )

        return (outline_id, line_id)
