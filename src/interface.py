# === Etape 1 : Affichage des livres existants dans un tableau (onglet Livres) ===

import tkinter as tk
from tkinter import ttk, messagebox
from bibliotheque import Livre, Membre, Bibliotheque
import visualisations

# === Fenêtre principale ===
root = tk.Tk()
root.title("Gestion Bibliothèque")
root.geometry("900x600")

# === Instance de la bibliothèque ===
biblio = Bibliotheque()
biblio.charger_donnees()

# === Création des onglets ===
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

frame_livres = ttk.Frame(notebook)
frame_membres = ttk.Frame(notebook)
frame_emprunts = ttk.Frame(notebook)
frame_stats = ttk.Frame(notebook)

notebook.add(frame_livres, text="📚 Livres")
notebook.add(frame_membres, text="👤 Membres")
notebook.add(frame_emprunts, text="🔁 Emprunts")
notebook.add(frame_stats, text="📊 Statistiques")

# === Table des livres (Treeview) ===
colonnes = ("ISBN", "Titre", "Auteur", "Année", "Genre", "Disponible")
tree_livres = ttk.Treeview(frame_livres, columns=colonnes, show="headings")

for col in colonnes:
    tree_livres.heading(col, text=col)
    tree_livres.column(col, width=130)

tree_livres.pack(fill="both", expand=True, padx=10, pady=10)

# === Remplissage du tableau avec les livres existants ===
def charger_livres():
    for item in tree_livres.get_children():
        tree_livres.delete(item)
    for livre in biblio.livres.values():
        dispo = "Oui" if livre.disponible else "Non"
        tree_livres.insert("", "end", values=(livre.isbn, livre.titre, livre.auteur, livre.annee, livre.genre, dispo))

charger_livres()

# === Formulaire d'ajout de livre ===
form_frame = ttk.LabelFrame(frame_livres, text="Ajouter un livre")
form_frame.pack(padx=10, pady=10, fill="x")

labels = ["ISBN", "Titre", "Auteur", "Année", "Genre"]
entries = {}
for i, label in enumerate(labels):
    ttk.Label(form_frame, text=label).grid(row=i, column=0, sticky="w", padx=5, pady=2)
    entry = ttk.Entry(form_frame)
    entry.grid(row=i, column=1, sticky="ew", padx=5, pady=2)
    entries[label] = entry

form_frame.columnconfigure(1, weight=1)

# === Bouton pour ajouter le livre ===
def ajouter_livre():
    isbn = entries["ISBN"].get().strip()
    titre = entries["Titre"].get().strip()
    auteur = entries["Auteur"].get().strip()
    annee = entries["Année"].get().strip()
    genre = entries["Genre"].get().strip()

    if not (isbn and titre and auteur and annee and genre):
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
        return

    if isbn in biblio.livres:
        messagebox.showerror("Erreur", f"Un livre avec l'ISBN {isbn} existe déjà.")
        return

    livre = Livre(isbn, titre, auteur, annee, genre)
    biblio.ajouter_livre(livre)
    biblio.sauvegarder_donnees()
    charger_livres()
    messagebox.showinfo("Succès", f"Livre '{titre}' ajouté.")
    for entry in entries.values():
        entry.delete(0, tk.END)

btn_ajouter = ttk.Button(form_frame, text="Ajouter le livre", command=ajouter_livre)
btn_ajouter.grid(row=len(labels), column=0, columnspan=2, pady=10)

# === Lancement de la fenêtre ===
root.mainloop()
