def init_grid(root):
    """Initialisiert das Grid-Layout für das übergebene Widget."""
    root.grid_columnconfigure(0, weight=10)
    root.grid_columnconfigure(1, weight=10)
    root.grid_columnconfigure(2, weight=10)
    root.grid_columnconfigure(3, weight=10)
    root.grid_columnconfigure(4, weight=60)
