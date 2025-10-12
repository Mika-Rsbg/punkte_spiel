import tkinter as tk
from controllers.spiel import StrategieSpiel
import utils.layout_utils as layout_manager


def main():
    root = tk.Tk()
    root.title("StrategieSpiel")

    # Grid-Konfiguration
    layout_manager.init_grid(root)

    # Spiel starten
    StrategieSpiel(root)

    root.mainloop()


if __name__ == "__main__":
    main()
