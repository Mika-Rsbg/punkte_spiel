def resize_window(root):
    """Past die Größe eines Fenster auf die Größe an die benötigt wird um allen Inhalt dar zu stellen.

    Args:
        window (tk.Tk | tk.Toplevel): Fenster auf dem die Ändernungen vorgenommen werden.
    """
    root.update_idletasks()  # Aktualisiert die Layout-Berechnungen
    neu_width = root.winfo_reqwidth()
    new_height = root.winfo_reqheight()
    root.geometry(f"{neu_width}x{new_height}")

def update_widgets(labels):
    """Updated Widgets.

    Args:
        labels (object): Object auf dem die jeweilige `update()` methode ausgeführt wird."""
    labels.update()