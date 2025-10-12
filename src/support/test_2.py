import tkinter as tk
from tkinter import messagebox, ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np  # NumPy für mathematische Operationen importieren

class SocialNetworkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Soziales Netzwerk - Klasse/Schule")
        
        self.graph = nx.Graph()  # Netzwerk-Graph
        self.groups = {}  # Speichert Gruppen: {"Gruppenname": [Liste von Personen]}
        
        # Farben für Beziehungstypen
        self.relation_colors = {
            "Freundschaft": "green",
            "Romantisch": "red",
            "Hass": "black",
            "Abneigung": "orange",
            "Bekannte": "blue",
            "Beste Freunde": "purple",
        }
        self.edges_with_types = {}  # Speichert Beziehungstypen
        
        # GUI-Elemente
        self.name_label = tk.Label(root, text="Name:")
        self.name_label.grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.add_student_button = tk.Button(root, text="Schüler hinzufügen", command=self.add_student)
        self.add_student_button.grid(row=0, column=2, padx=5, pady=5)
        
        self.rel_label = tk.Label(root, text="Beziehung: Schüler1, Schüler2")
        self.rel_label.grid(row=1, column=0, padx=5, pady=5, columnspan=2)
        self.rel_entry = tk.Entry(root)
        self.rel_entry.grid(row=1, column=2, padx=5, pady=5)
        
        self.rel_type_label = tk.Label(root, text="Beziehungstyp:")
        self.rel_type_label.grid(row=2, column=0, padx=5, pady=5)
        self.rel_type_combobox = ttk.Combobox(root, values=list(self.relation_colors.keys()))
        self.rel_type_combobox.grid(row=2, column=1, padx=5, pady=5)
        self.rel_type_combobox.set("Freundschaft")
        
        self.add_relation_button = tk.Button(root, text="Beziehung hinzufügen", command=self.add_relation)
        self.add_relation_button.grid(row=2, column=2, padx=5, pady=5)
        
        self.batch_import_button = tk.Button(root, text="Batch-Import starten", command=self.open_batch_import_window)
        self.batch_import_button.grid(row=3, column=2, padx=5, pady=5)
        
        self.group_label = tk.Label(root, text="Freundesgruppe:")
        self.group_label.grid(row=4, column=0, padx=5, pady=5)
        self.group_entry = tk.Entry(root)
        self.group_entry.grid(row=4, column=1, padx=5, pady=5)
        
        self.add_group_button = tk.Button(root, text="Gruppe hinzufügen", command=self.add_group)
        self.add_group_button.grid(row=4, column=2, padx=5, pady=5)
        
        self.student_to_group_label = tk.Label(root, text="Schüler zur Gruppe hinzufügen:")
        self.student_to_group_label.grid(row=5, column=0, columnspan=3, padx=5, pady=5)
        
        self.group_combobox = ttk.Combobox(root, values=[], state="readonly")
        self.group_combobox.grid(row=6, column=0, padx=5, pady=5)
        
        self.student_combobox = ttk.Combobox(root, values=[], state="readonly")
        self.student_combobox.grid(row=6, column=1, padx=5, pady=5)
        
        self.add_to_group_button = tk.Button(root, text="Hinzufügen", command=self.add_student_to_group)
        self.add_to_group_button.grid(row=6, column=2, padx=5, pady=5)

        self.group_import_button = tk.Button(root, text="Batch-Import Gruppen", command=self.open_group_import_window)
        self.group_import_button.grid(row=5, column=2, padx=5, pady=5)

        
        self.show_network_button = tk.Button(root, text="Netzwerk anzeigen", command=self.show_network)
        self.show_network_button.grid(row=7, column=2, padx=5, pady=5)
    
    def add_student(self):
        name = self.name_entry.get().strip()
        if name:
            if name not in self.graph.nodes:
                self.graph.add_node(name)
                self.student_combobox["values"] = list(self.graph.nodes)
                messagebox.showinfo("Erfolg", f"Schüler {name} wurde hinzugefügt.")
            else:
                messagebox.showwarning("Fehler", f"Schüler {name} existiert bereits.")
        else:
            messagebox.showwarning("Fehler", "Name darf nicht leer sein.")
    
    def add_relation(self):
        relation = self.rel_entry.get().strip()
        relation_type = self.rel_type_combobox.get().strip()

        if not relation_type:
            messagebox.showwarning("Fehler", "Bitte einen Beziehungstyp auswählen.")
            return

        try:
            entity1, entity2 = map(str.strip, relation.split(","))

            # Prüfen, ob eine der Entitäten eine Gruppe ist
            if entity1 in self.groups and entity2 in self.groups:
                # Beziehung zwischen Gruppen
                for student1 in self.groups[entity1]:
                    for student2 in self.groups[entity2]:
                        self.graph.add_edge(student1, student2)
                        self.edges_with_types[(student1, student2)] = relation_type

            elif entity1 in self.groups:
                # Beziehung zwischen Gruppe und Schüler
                if entity2 in self.graph.nodes:
                    for student in self.groups[entity1]:
                        self.graph.add_edge(student, entity2)
                        self.edges_with_types[(student, entity2)] = relation_type
                else:
                    messagebox.showwarning("Fehler", f"Schüler {entity2} existiert nicht.")

            elif entity2 in self.groups:
                # Beziehung zwischen Schüler und Gruppe
                if entity1 in self.graph.nodes:
                    for student in self.groups[entity2]:
                        self.graph.add_edge(entity1, student)
                        self.edges_with_types[(entity1, student)] = relation_type
                else:
                    messagebox.showwarning("Fehler", f"Schüler {entity1} existiert nicht.")

            else:
                # Normale Beziehung zwischen Schülern
                if entity1 in self.graph.nodes and entity2 in self.graph.nodes:
                    self.graph.add_edge(entity1, entity2)
                    self.edges_with_types[(entity1, entity2)] = relation_type
                else:
                    messagebox.showwarning(
                        "Fehler", "Beide Schüler müssen existieren oder Gruppen müssen korrekt angegeben werden."
                    )

            messagebox.showinfo(
                "Erfolg",
                f"Beziehung ({relation_type}) zwischen {entity1} und {entity2} hinzugefügt.",
            )

        except ValueError:
            messagebox.showwarning(
                "Fehler", "Bitte geben Sie zwei Entitäten, getrennt durch ein Komma, ein."
            )

    
    def add_group(self):
        group_name = self.group_entry.get().strip()
        if group_name:
            if group_name not in self.groups:
                self.groups[group_name] = []
                self.group_combobox["values"] = list(self.groups.keys())
                messagebox.showinfo("Erfolg", f"Gruppe '{group_name}' wurde hinzugefügt.")
            else:
                messagebox.showwarning("Fehler", f"Gruppe '{group_name}' existiert bereits.")
        else:
            messagebox.showwarning("Fehler", "Gruppenname darf nicht leer sein.")
    
    def add_student_to_group(self):
        group_name = self.group_combobox.get()
        student_name = self.student_combobox.get()
        if group_name and student_name:
            if student_name not in self.groups[group_name]:
                self.groups[group_name].append(student_name)
                messagebox.showinfo("Erfolg", f"Schüler {student_name} wurde zur Gruppe '{group_name}' hinzugefügt.")
            else:
                messagebox.showwarning("Fehler", f"Schüler {student_name} ist bereits in der Gruppe '{group_name}'.")
        else:
            messagebox.showwarning("Fehler", "Bitte wählen Sie eine Gruppe und einen Schüler aus.")
    
    def open_batch_import_window(self):
            # Neues Fenster für Batch-Import
            batch_window = tk.Toplevel(self.root)
            batch_window.title("Batch-Import von Beziehungen")
            
            tk.Label(batch_window, text="Mehrere Beziehungen (Format: Schüler1, Schüler2, Typ):").pack(padx=10, pady=10)
            
            batch_text = tk.Text(batch_window, height=15, width=50)
            batch_text.pack(padx=10, pady=10)
            
            def import_batch():
                batch_data = batch_text.get("1.0", tk.END).strip()
                if not batch_data:
                    messagebox.showwarning("Fehler", "Das Eingabefeld ist leer.")
                    return
                
                errors = []
                for line in batch_data.splitlines():
                    try:
                        student1, student2, relation_type = map(str.strip, line.split(","))
                        if student1 not in self.graph.nodes:
                            self.graph.add_node(student1)
                        if student2 not in self.graph.nodes:
                            self.graph.add_node(student2)
                        if relation_type not in self.relation_colors:
                            errors.append(f"Unbekannter Beziehungstyp: {relation_type}")
                            continue
                        self.graph.add_edge(student1, student2)
                        self.edges_with_types[(student1, student2)] = relation_type
                    except ValueError:
                        errors.append(f"Ungültiges Format: {line}")
                
                if errors:
                    messagebox.showwarning("Fehler beim Import", "\n".join(errors))
                else:
                    messagebox.showinfo("Erfolg", "Alle Beziehungen erfolgreich importiert.")
                    batch_window.destroy()  # Fenster schließen nach erfolgreichem Import
            
            tk.Button(batch_window, text="Beziehungen importieren", command=import_batch).pack(padx=10, pady=10)

    def open_group_import_window(self):
        # Neues Fenster für Batch-Import von Gruppen
        group_window = tk.Toplevel(self.root)
        group_window.title("Batch-Import von Gruppen")
        
        tk.Label(group_window, text="Mehrere Gruppen (Format: Gruppenname: Schüler1, Schüler2, ...):").pack(padx=10, pady=10)
        
        group_text = tk.Text(group_window, height=15, width=50)
        group_text.pack(padx=10, pady=10)
        
        def import_groups():
            group_data = group_text.get("1.0", tk.END).strip()
            if not group_data:
                messagebox.showwarning("Fehler", "Das Eingabefeld ist leer.")
                return
            
            errors = []
            for line in group_data.splitlines():
                try:
                    group_name, members = map(str.strip, line.split(":"))
                    members = [member.strip() for member in members.split(",")]
                    
                    if group_name in self.groups:
                        errors.append(f"Gruppe '{group_name}' existiert bereits.")
                        continue
                    
                    # Gruppe erstellen
                    self.groups[group_name] = []
                    for member in members:
                        if member not in self.graph.nodes:
                            self.graph.add_node(member)  # Schüler hinzufügen, falls noch nicht existierend
                        self.groups[group_name].append(member)
                    
                    self.group_combobox["values"] = list(self.groups.keys())  # Dropdown aktualisieren
                    
                except ValueError:
                    errors.append(f"Ungültiges Format: {line}")
            
            if errors:
                messagebox.showwarning("Fehler beim Import", "\n".join(errors))
            else:
                messagebox.showinfo("Erfolg", "Alle Gruppen erfolgreich importiert.")
                group_window.destroy()  # Fenster schließen nach erfolgreichem Import
        
        tk.Button(group_window, text="Gruppen importieren", command=import_groups).pack(padx=10, pady=10)


    def show_network(self):
        if len(self.graph.nodes) == 0:
            messagebox.showwarning("Fehler", "Das Netzwerk ist leer.")
            return

        fig, ax = plt.subplots(figsize=(8, 8))
        pos = {}  # Positionen der Knoten

        # Layout für Gruppen: Anordnung in Kreisen
        group_center_step = 2 * 3.14 / max(1, len(self.groups))  # Schrittweite für Gruppenkreise
        group_centers = {}  # Speichert die zentralen Positionen der Gruppen
        radius = 2  # Radius für Gruppenkreise
        angle = 0

        for group_name, members in self.groups.items():
            group_center = (radius * 3 * np.cos(angle), radius * 3 * np.sin(angle))
            group_centers[group_name] = group_center
            angle += group_center_step

            # Anordnung der Mitglieder der Gruppe in einem Kreis
            num_members = len(members)
            if num_members == 0:
                continue

            member_angle_step = 2 * 3.14 / num_members
            member_angle = 0
            for member in members:
                pos[member] = (
                    group_center[0] + radius * np.cos(member_angle),
                    group_center[1] + radius * np.sin(member_angle),
                )
                member_angle += member_angle_step

        # Positionierung von Schülern, die nicht in Gruppen sind
        ungrouped_students = set(self.graph.nodes) - set(
            [student for group in self.groups.values() for student in group]
        )
        ungrouped_pos = nx.spring_layout(
            self.graph.subgraph(ungrouped_students), center=(0, 0)
        )
        pos.update(ungrouped_pos)

        # Knoten zeichnen
        nx.draw_networkx_nodes(
            self.graph, pos, node_color="lightblue", ax=ax, edgecolors="black"
        )
        nx.draw_networkx_labels(self.graph, pos, ax=ax)

        # Kanten basierend auf Beziehungstyp zeichnen
        for (student1, student2), relation_type in self.edges_with_types.items():
            color = self.relation_colors.get(relation_type, "gray")
            nx.draw_networkx_edges(
                self.graph, pos, edgelist=[(student1, student2)], edge_color=color, ax=ax
            )

        # Kreise um die Gruppen zeichnen
        for group_name, members in self.groups.items():
            if members:
                group_member_positions = [pos[member] for member in members]
                circle = plt.Circle(
                    group_centers[group_name],
                    radius * 1.5,
                    color="blue",
                    fill=False,
                    linestyle="dotted",
                    label=group_name,
                )
                ax.add_patch(circle)

        # Legende erstellen
        legend_items = [
            plt.Line2D([0], [0], color=color, lw=2, label=rel)
            for rel, color in self.relation_colors.items()
        ]
        ax.legend(handles=legend_items, loc="best")

        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().grid(row=8, column=0, columnspan=3, pady=10)


# Hauptanwendung starten
if __name__ == "__main__":
    root = tk.Tk()
    app = SocialNetworkApp(root)
    root.mainloop()
