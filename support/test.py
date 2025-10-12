import tkinter as tk

# Funktion, um Fenstergröße neu anzupassen
def anpassen(root):
    root.update_idletasks()  # Aktualisiert die Layout-Berechnungen
    neue_breite = root.winfo_reqwidth()
    neue_hoehe = root.winfo_reqheight()
    root.geometry(f"{neue_breite}x{neue_hoehe}")

# Hauptfenster erstellen
root = tk.Tk()

# Define a grid
root.columnconfigure(0, minsize=100)  # Mindestbreite
root.columnconfigure(1, minsize=15)
root.columnconfigure(2, minsize=75)
root.rowconfigure(0, minsize=20, uniform="b")
root.rowconfigure(1, minsize=20, uniform="b")
root.rowconfigure(2, minsize=10, uniform="b")
root.rowconfigure(3, minsize=10, uniform="b")
root.rowconfigure(4, minsize=10, uniform="b")
root.rowconfigure(5, minsize=10, uniform="b")
root.rowconfigure(6, minsize=20, uniform="b")

# Inhalt hinzufügen
label = tk.Label(root, text="Bau Optionen", font=("Arial", 12))
label.grid(row=0, column=0, columnspan=3, sticky="nswe")

# Button zum Hinzufügen neuer Inhalte
def inhalt_hinzufuegen():
    neuer_text = tk.Label(root, text="Neuer Inhalt hinzugefügt!", font=("Arial", 12))
    neuer_text.grid(row=2, column=0, columnspan=3)

    costs = 15
    building_duration = 4
    # Reihe 4
    label_name_1 = tk.Label(root, text="Kosten", font=("Arial", 12))
    label_name_1.grid(row=3, column=0, sticky="w") # sticky="nswe")
    label_value_1 = tk.Label(root, text=costs, font=("Arial", 12))
    label_value_1.grid(row=3, column=1, sticky="e")
    label_unit_1 = tk.Label(root, text="Rohstoffe", font=("Arial", 12))
    label_unit_1.grid(row=3, column=2, sticky="w")
    # Reihe 5
    label_name_2 = tk.Label(root, text="Bau Dauer", font=("Arial", 12))
    label_name_2.grid(row=4, column=0, sticky="e") # sticky="nswe")
    label_value_2 = tk.Label(root, text=building_duration, font=("Arial", 12))
    label_value_2.grid(row=4, column=1, sticky="w")
    label_unit_2 = tk.Label(root, text="Runden", font=("Arial", 12))
    label_unit_2.grid(row=4, column=2, sticky="e")
    # Reihe 5
    label_name_2 = tk.Label(root, text="Bau Dauer", font=("Arial", 12))
    label_name_2.grid(row=5, column=0,sticky="nswe")
    
    button2 = tk.Button(root, text="Close", command=root.destroy, font=("Arial", 12))
    button2.grid(row=6, column=0, padx=10, pady=10)
    anpassen(root)  # Fenstergröße anpassen

button = tk.Button(root, text="Inhalt hinzufügen", command=inhalt_hinzufuegen)
button.grid(row=6, column=2, padx=10, pady=10)

x = 10
y = 20
z = 20
y -= x
z =- x

print(y)
print(z)

# Haupt-Eventloop starten
root.mainloop()
