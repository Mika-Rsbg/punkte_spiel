import tkinter as tk

def aktualisiere_text():
    aktueller_text = label.cget("text")  # Aktuellen Text des Labels abrufen
    neuer_text = aktueller_text + "\nNeuer Text"  # Neuen Text hinzufügen
    label.config(text=neuer_text)  # Label aktualisieren

# Hauptfenster erstellen
root = tk.Tk()
root.title("Label aktualisieren")

# Ein Label erstellen
label = tk.Label(root, text="Starttext", font=("Arial", 14))
label.pack(pady=20)

# Ein Button zum Aktualisieren des Labels
button = tk.Button(root, text="Text hinzufügen", command=aktualisiere_text)
button.pack(pady=10)

# GUI ausführen
root.mainloop()