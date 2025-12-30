import tkinter as tk
import config

import utils.grid_utils as grid_utils
import utils.canvas_utils as canvas_utils
import utils.identify_utils as identify_utils
import utils.game_state_utils as game_state_utils
import utils.window_utils as window_utils
import utils.economy_manager as economy_manager

from models.dorf import Dorf
from models.ressourcenproduktion import Ressourcenproduktion
from models.stadt import Stadt
from models.street import Street


class BuildingMenu:
    def __init__(self, parent):
        """Erstellt das Building-Menü als Toplevel-Fenster.
        Args:
            parent (tk.Tk | tk.Toplevel): Das Elternfenster,
                in dem dieses Menü geöffnet wird."""
        self.window = tk.Toplevel(parent)
        self.window.title("Building Menu")

        # Define a grid
        self.window.columnconfigure(0, minsize=100)
        self.window.columnconfigure(1, minsize=5)
        self.window.columnconfigure(2, minsize=75)
        self.window.rowconfigure(0, minsize=20, uniform="b")
        self.window.rowconfigure(1, minsize=20, uniform="b")
        self.window.rowconfigure(2, minsize=10, uniform="b")
        self.window.rowconfigure(3, minsize=10, uniform="b")
        self.window.rowconfigure(4, minsize=10, uniform="b")
        self.window.rowconfigure(5, minsize=10, uniform="b")
        self.window.rowconfigure(6, minsize=20, uniform="b")

        # Speichere referenzierte Widgets, die dynamisch erstellt werden
        self.dynamic_widgets = []

        # Widgets hinzufügen
        label = tk.Label(
            self.window, text="Bau Optionen",
            font=config.Design.Fonts.HEADING_2
        )
        label.grid(row=0, column=0, columnspan=3, sticky="nswe")

        self.canvas = tk.Canvas(
            self.window,
            width=config.BuildingMenu.BuildingMenuCanvas.CANVAS_WIDTH,
            height=config.BuildingMenu.BuildingMenuCanvas.CANVAS_HEIGHT,
            bg=config.BuildingMenu.BuildingMenuCanvas.CANVAS_BACKGROUND
        )
        self.canvas.grid(row=1, column=0, columnspan=3)
        self.canvas.bind("<Button-1>", self.on_click)

        self.create_grid()

        button3 = tk.Button(
            self.window, text="Close", command=self.destroy_window,
            bg=config.Design.Colors.PRIMARY,
            font=config.Design.Fonts.BUTTON_TEXT
        )
        button3.grid(row=6, column=2, padx=10, pady=10)
        window_utils.resize_window(self.window)

    def create_grid(self, rows=config.BuildingMenu.BuildingMenuGrid.GRID_ROWS,
                    cols=config.BuildingMenu.BuildingMenuGrid.GRID_COLS,
                    grid_size=config.GameGrid.GRID_SIZE):
        """Erzeugt das Auswahl-Raster

        Args:
            rows (int, optional): Anzahl der Zeilen.
                Defaults to `config.BuildingMenu.BuildingMenuGrid.GRID_ROWS`.
            cols (int, optional): Anzahl der Spalten.
                Defaults to `config.BuildingMenu.BuildingMenuGrid.GRID_COLS`.
            grid_size (int, optional): Größe der Felder.
                Defaults to `config.GameGrid.GRID_SIZE`."""
        # Hintergrundfarbe des Fensters
        window_bg_color = self.window["bg"]
        # config.BuildingMenu.BuildingMenuCanvas.CANVAS_BACKGROUND
        canvas_bg_color = None

        # Verfügbare Ressourcen des Spielers
        ressources = game_state_utils.get_player_ressources()

        # Farben für die Gebäude
        color_ressourcenproduktion = game_state_utils.get_building_availability_color(
            config.Building.BuildingID.RESSOURCENPRODUKTION, ressources,
            canvas_bg_color
        )
        color_dorf = game_state_utils.get_building_availability_color(
            config.Building.BuildingID.DORF, ressources, canvas_bg_color
        )
        color_stadt = game_state_utils.get_building_availability_color(
            config.Building.BuildingID.STADT, ressources, canvas_bg_color
        )
        color_street = game_state_utils.get_building_availability_color(
            config.Building.BuildingID.STREET, ressources, canvas_bg_color
        )

        for row in range(rows):
            for col in range(cols):
                # Berechne die Koordinaten für jedes Feld
                x1, y1 = col * grid_size + 2, row * grid_size + 2
                x2, y2 = x1 + grid_size, y1 + grid_size

                x = (x1 + x2) / 2
                y = (y1 + y2) / 2

                if col % 2 == 0:  # Gebäude in geraden Spalten
                    # Erstelle das Rechteck für das Feld
                    rect_id = self.canvas.create_rectangle(x1, y1, x2, y2, outline="black")
                    # Speichere die Feldinformationen
                    config.BuildingMenu.BuildingMenuGrid.fields[(col, row)] = {
                        "rect_id": rect_id,
                        "building": None,
                        "too_expensive": True,
                        "spacing_field": False
                    }
                    if (col + 1) == 7:
                        canvas_utils.draw.draw_dorf(self.canvas, x, y)
                        building_id = config.Building.BuildingID.STREET
                        config.BuildingMenu.BuildingMenuGrid.fields[(col, row)]["building"] = building_id
                        config.BuildingMenu.BuildingMenuGrid.fields[(col, row)]["too_expensive"] = game_state_utils.is_building_too_expensive(building_id, ressources)
                        canvas_utils.highlight_field(self.canvas, color=color_street, fields=config.BuildingMenu.BuildingMenuGrid.fields, field_coords=(col, row))

                else:  # Abstand in ungeraden Spalten
                    # Erstelle ein unsichtbares Rechteck mit Fensterhintergrundfarbe
                    rect_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=window_bg_color, outline=window_bg_color)
                    # Optional: Speicher Abstandsfelder auch, um künftige Klicks darauf zu ignorieren
                    config.BuildingMenu.BuildingMenuGrid.fields[(col, row)] = {
                        "rect_id": rect_id,
                        "building": None,  # Kein Gebäude
                        "too_expensive": True,
                        "spacing_field": True
                    }
                    col_1= col-1
                    x1, y1 = col_1 * grid_size + 2, row * grid_size + 2
                    x2, y2 = x1 + grid_size, y1 + grid_size
                    x = (x1 + x2) / 2
                    y = (y1 + y2) / 2
                    # Neu zeichnen der Outline
                    config.BuildingMenu.BuildingMenuGrid.fields[(col - 1, row)]["rect_id"] = self.canvas.create_rectangle(x1, y1, x2, y2, outline="black")
                    # Zeichnen der Gebäude
                    if (col) == 1:
                        canvas_utils.draw.draw_dorf(self.canvas, x, y)
                        building_id = config.Building.BuildingID.DORF
                        config.BuildingMenu.BuildingMenuGrid.fields[(col_1, row)]["building"] = building_id
                        config.BuildingMenu.BuildingMenuGrid.fields[(col_1, row)]["too_expensive"] = game_state_utils.is_building_too_expensive(building_id, ressources)
                        canvas_utils.highlight_field(self.canvas,color=color_dorf, fields=config.BuildingMenu.BuildingMenuGrid.fields, field_coords=(col_1, row))
                    if (col) == 3:
                        canvas_utils.draw.draw_ressourcenproduktion(self.canvas, x, y)
                        building_id = config.Building.BuildingID.RESSOURCENPRODUKTION
                        config.BuildingMenu.BuildingMenuGrid.fields[(col_1, row)]["building"] = building_id
                        config.BuildingMenu.BuildingMenuGrid.fields[(col_1, row)]["too_expensive"] = game_state_utils.is_building_too_expensive(building_id, ressources)
                        canvas_utils.highlight_field(self.canvas,color=color_ressourcenproduktion, fields=config.BuildingMenu.BuildingMenuGrid.fields, field_coords=(col_1, row))
                    if (col) == 5:
                        canvas_utils.draw.draw_stadt(self.canvas, x, y)
                        building_id = config.Building.BuildingID.STADT
                        config.BuildingMenu.BuildingMenuGrid.fields[(col_1, row)]["building"] = building_id
                        config.BuildingMenu.BuildingMenuGrid.fields[(col_1, row)]["too_expensive"] = game_state_utils.is_building_too_expensive(building_id, ressources)
                        canvas_utils.highlight_field(self.canvas,color=color_stadt, fields=config.BuildingMenu.BuildingMenuGrid.fields, field_coords=(col_1, row))
    
    def destroy_window(self):
        col, row = config.GameCanvas.selected_field
        self.window.destroy()
        config.GameCanvas.is_field_selected = False
        canvas_utils.clear_field(config.GameCanvas.canvas, col=col, row=row)

    def on_click(self, event):
        """Behandelt Mausklicks auf dem Canvas.
        Wandelt Pixel-Koordinaten in Grid-Koordinaten um.
        """
        # Pixelkoordinaten des Klicks
        x, y = event.x, event.y

        # Berechne die Grid-Koordinaten
        result = grid_utils.get_grid_coordinates(x, y, config.GameGrid.GRID_SIZE, 1, config.BuildingMenu.BuildingMenuGrid.GRID_COLS)

        if result:
            col, row = result
            if not config.BuildingMenu.BuildingMenuGrid.fields[(col, row)]["spacing_field"]:
                if not config.BuildingMenu.BuildingMenuGrid.fields[(col, row)]["too_expensive"]:
                    if not config.BuildingMenu.is_field_selected:
                        config.BuildingMenu.is_field_selected = True
                    elif config.BuildingMenu.is_field_selected:
                        canvas_utils.clear_field(self.canvas,fields=config.BuildingMenu.BuildingMenuGrid.fields, field_coords=config.BuildingMenu.selected_field)
                    config.BuildingMenu.selected_field = (col, row)
                    canvas_utils.highlight_field(self.canvas, fields=config.BuildingMenu.BuildingMenuGrid.fields, field_coords=config.BuildingMenu.selected_field)
                    building_id = grid_utils.get_building_id(config.BuildingMenu.selected_field, config.BuildingMenu.BuildingMenuGrid.fields)
                    self.show_information(building_id)

    def clear_dynamic_widgets(self):
        """Löscht alle Widgets in `self.dynamic_widgets` und leert die Liste."""
        for widget in self.dynamic_widgets:
            widget.destroy()
        self.dynamic_widgets = []

    def show_information(self, building_id):
        """Zeigt die Informationen eines Gebäudes an. Löscht vorher existierende Labels."""
        # Lösche vorhandene Widgets
        self.clear_dynamic_widgets()

        # Variablen
        building_designation = game_state_utils.get_building(building_id).BUILDING_DESIGNATION
        config.BuildingMenu.building_costs = economy_manager.calculate_building_cost(building_id)
        config.BuildingMenu.building_duration = 0
        self.selected_action = None  # Zur Sicherheit initialisieren

        # Neue Labels erstellen
        # Reihe 3
        label_building_designation = tk.Label(self.window, text=building_designation, font=config.Design.Fonts.HEADING_3)
        label_building_designation.grid(row=2, column=0, columnspan=3)
        self.dynamic_widgets.append(label_building_designation)

        # Reihe 4
        label_name_1 = tk.Label(self.window, text="Kosten", font=config.Design.Fonts.PARAGRAPH_1)
        label_name_1.grid(row=3, column=0, sticky="w")
        self.dynamic_widgets.append(label_name_1)

        label_value_1 = tk.Label(self.window, text=config.BuildingMenu.building_costs, font=config.Design.Fonts.PARAGRAPH_2)
        label_value_1.grid(row=3, column=1, sticky="e")
        self.dynamic_widgets.append(label_value_1)

        label_unit_1 = tk.Label(self.window, text="Rohstoffe", font=config.Design.Fonts.PARAGRAPH_2)
        label_unit_1.grid(row=3, column=2, sticky="w")
        self.dynamic_widgets.append(label_unit_1)

        # Reihe 5
        label_name_2 = tk.Label(self.window, text="Bauzeit", font=config.Design.Fonts.PARAGRAPH_1)
        label_name_2.grid(row=4, column=0, sticky="w")
        self.dynamic_widgets.append(label_name_2)

        label_value_2 = tk.Label(self.window, text=config.BuildingMenu.building_duration, font=config.Design.Fonts.PARAGRAPH_2)
        label_value_2.grid(row=4, column=1, sticky="e")
        self.dynamic_widgets.append(label_value_2)

        label_unit_2 = tk.Label(self.window, text="Runden", font=config.Design.Fonts.PARAGRAPH_2)
        label_unit_2.grid(row=4, column=2, sticky="w")
        self.dynamic_widgets.append(label_unit_2)

        # Reihe 6
        self.select_field(building_id)

        button2 = tk.Button(self.window, text="Bestätigen", command=self.execute_action, bg=config.Design.Colors.PRIMARY, font=config.Design.Fonts.BUTTON_TEXT)
        button2.grid(row=6, column=0, padx=10, pady=10)
        self.dynamic_widgets.append(button2)

        # Fenstergröße aktualisieren
        window_utils.resize_window(self.window)

    def execute_action(self):
        """Führt die gespeicherte Aktion aus, falls vorhanden."""
        if self.selected_action:
            self.selected_action()
        else:
            print("Keine Aktion ausgewählt.")
    ##################################################
    ##################################################
    # Terminal
    ##################################################
    ##################################################

    def select_field(self, building_id):
        """Setzt die Aktion, die beim Bestätigen ausgeführt werden soll."""
        self.selected_action = lambda: identify_utils.execute_function_by_building_id(
            building_id, self.build_dorf, self.build_ressourcenproduktion, self.build_stadt, self.build_street
        )

    def build_dorf(self):
        self.window.destroy()
        Dorf.build_dorf()
        window_utils.update_widgets(config.GameWindow.labels)

    def build_ressourcenproduktion(self):
        self.window.destroy()
        Ressourcenproduktion.build_ressourcenproduktion()
        window_utils.update_widgets(config.GameWindow.labels)

    def build_stadt(self):
        self.window.destroy()
        Stadt.build_stadt()
        window_utils.update_widgets(config.GameWindow.labels)

    def build_street(self):
        self.window.destroy()
        Street.start_street_placing_mode()
