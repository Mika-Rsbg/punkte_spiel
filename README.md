# Ordnerstruktur

```
StrategieSpiel/
│
├── controllers/                    # Logik für die Spielsteuerung und -verwaltung
│   ├── attack_logic.py                 # Logic für Angriffe
│   ├── computer_ai.py                  # Logik für Computeraktionen
│   ├── resource_manager.py             # Klasse für Ressourcen Management
│   └── spiel.py                        # Hauptlogik und Verwaltung des Spiels
│
├── gui/                            # GUI-Module für die Benutzeroberfläche
│   ├── menues/                         # GUI-Module für die Menues
│   │   ├── attack_menu.py                  # GUI-Komponente für das attack_menu
│   │   ├── building_menu.py                # GUI-Komponente für das building_menu
│   │   ├── dorf_menu.py                    # GUI-Komponente für das building_menu
│   │   ├── ressourcenproduktion_menu.py    # GUI-Komponente für das ressourcenproduktion_menu
│   │   └── stadt_menu.py                   # GUI-Komponente für das stadt_menu
│   ├── buttons.py                      # GUI-Komponenten für Buttons
│   ├── game_canvas.py                  # GUI-Komponente für das Spielfeld (Canvas)
│   ├── gui_elements.py                 # GUI-Komponente für übrige GUI-Elemente
│   └── labels.py                       # GUI-Komponenten für Labels und Anzeigen 
│
├── models/                         # Enthält alle Spiel-Modelle (z.B., Dorf, Stadt, Einheit)
│   ├── dorf.py                         # Dorf Klase
│   ├── einheit.py                      # Einheiten Klasse
│   ├── ressourcenproduktion.py         # Ressourcenproduktion Klasse
│   ├── stadt.py                        # Stadt Klasse
│   └── street.py                       # Street Klasse
│
├── utils/                          # Utils des Spiels
│   ├── canvas_utils.py
│   ├── economy_manager.py
│   ├── game_state_utils.py
│   ├── grid_utils.py                   # Utils zum erkennen von Feldern auf dem Spielfeld
│   ├── identify_utils.py
│   ├── layout_manager.py
│   └── window_utils.py
│
├── config.py                       # Konfigurationswerte und Spielkonstanten
├── main.py                         # Hauptdatei zum Starten des Spiels
└── README.md                       # Projektbeschreibung und Anleitung
```
