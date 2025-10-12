import tkinter as tk
from street_drawing_menu import StreetDrawingMenu

if __name__ == "__main__":
    window_1 = tk.Tk()
    predefined_buildings = {
    (0, 0): {
            "building": 1,
            "player": 0,
            "connections": None
        },
    (1, 1): {
            "building": 4,
            "player": 0,
            "connections": {
                            "N": False,  # Norden
                            "NE": False, # Nord-Osten
                            "E": True,  # Osten
                            "SE": False, # Süd-Osten
                            "S": True,  # Süden
                            "SW": False, # Süd-Westen
                            "W": False,  # Westen
                            "NW": True, # Nord-Westen
                        }
        },
    (1, 2): {
            "building": 4,
            "player": 0,
            "connections": {
                            "N": True,  # Norden
                            "NE": False, # Nord-Osten
                            "E": False,  # Osten
                            "SE": True, # Süd-Osten
                            "S": False,  # Süden
                            "SW": False, # Süd-Westen
                            "W": False,  # Westen
                            "NW": False, # Nord-Westen
                        }
        },
    (1, 3): {
            "building": 0,
            "player": 0,
            "connections": {
                            "N": True,  # Norden
                            "NE": False, # Nord-Osten
                            "E": True,  # Osten
                            "SE": False, # Süd-Osten
                            "S": False,  # Süden
                            "SW": False, # Süd-Westen
                            "W": False,  # Westen
                            "NW": False, # Nord-Westen
                        }
        },
    (2, 1): {
        "building": 4,
        "player": 0,
        "connections": {
                        "N": False,  # Norden
                        "NE": False, # Nord-Osten
                        "E": True,  # Osten
                        "SE": False, # Süd-Osten
                        "S": False,  # Süden
                        "SW": False, # Süd-Westen
                        "W": True,  # Westen
                        "NW": False, # Nord-Westen
                    }
        },
    (2, 3): {
            "building": 4,
            "player": 0,
            "connections": {
                            "N": False,  # Norden
                            "NE": False, # Nord-Osten
                            "E": True,  # Osten
                            "SE": False, # Süd-Osten
                            "S": False,  # Süden
                            "SW": False, # Süd-Westen
                            "W": False,  # Westen
                            "NW": True, # Nord-Westen
                        }
        },
    (3, 1): {
            "building": 4,
            "player": 0,
            "connections": {
                            "N": False,  # Norden
                            "NE": False, # Nord-Osten
                            "E": False,  # Osten
                            "SE": False, # Süd-Osten
                            "S": True,  # Süden
                            "SW": False, # Süd-Westen
                            "W": True,  # Westen
                            "NW": False, # Nord-Westen
                        }
        },
    (3, 2): {
            "building": 4,
            "player": 0,
            "connections": {
                            "N": True,  # Norden
                            "NE": False, # Nord-Osten
                            "E": False,  # Osten
                            "SE": False, # Süd-Osten
                            "S": True,  # Süden
                            "SW": False, # Süd-Westen
                            "W": False,  # Westen
                            "NW": False, # Nord-Westen
                        }
        },
    (3, 3): {
            "building": 4,
            "player": 0,
            "connections": {
                            "N": True,  # Norden
                            "NE": False, # Nord-Osten
                            "E": False,  # Osten
                            "SE": False, # Süd-Osten
                            "S": False,  # Süden
                            "SW": False, # Süd-Westen
                            "W": True,  # Westen
                            "NW": False, # Nord-Westen
                        }
        },
    }
    street_menu = StreetDrawingMenu(window_1, predefined_buildings=predefined_buildings)
    window_1.mainloop()
