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
form_frame = ttk.LabelFrame(frame_livres, text="Ajouter / Modifier un livre")
form_frame.pack(padx=10, pady=10, fill="x")

labels = ["ISBN", "Titre", "Auteur", "Année", "Genre"]
entries = {}
for i, label in enumerate(labels):
    ttk.Label(form_frame, text=label).grid(row=i, column=0, sticky="w", padx=5, pady=2)
    entry = ttk.Entry(form_frame)
    entry.grid(row=i, column=1, sticky="ew", padx=5, pady=2)
    entries[label] = entry

form_frame.columnconfigure(1, weight=1)

# === Ajouter un livre ===
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

# === Supprimer un livre ===
def supprimer_livre():
    selection = tree_livres.selection()
    if not selection:
        messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un livre à supprimer.")
        return

    item = tree_livres.item(selection[0])
    isbn = item['values'][0]
    if messagebox.askyesno("Confirmation", f"Supprimer le livre avec ISBN {isbn} ?"):
        del biblio.livres[isbn]
        biblio.sauvegarder_donnees()
        charger_livres()
        messagebox.showinfo("Supprimé", "Livre supprimé avec succès.")

# === Modifier un livre ===
def modifier_livre():
    selection = tree_livres.selection()
    if not selection:
        messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un livre à modifier.")
        return

    entries["ISBN"].config(state="normal")  # Active temporairement
    isbn = entries["ISBN"].get().strip()
    entries["ISBN"].config(state="disabled")  # Réactive la désactivation

    if isbn not in biblio.livres:
        messagebox.showerror("Erreur", "Livre non trouvé dans la base.")
        return

    titre = entries["Titre"].get().strip()
    auteur = entries["Auteur"].get().strip()
    annee = entries["Année"].get().strip()
    genre = entries["Genre"].get().strip()

    if not (titre and auteur and annee and genre):
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs (sauf ISBN).")
        return

    livre = biblio.livres[isbn]
    livre.titre = titre
    livre.auteur = auteur
    livre.annee = annee
    livre.genre = genre
    biblio.sauvegarder_donnees()
    charger_livres()
    messagebox.showinfo("Succès", "Livre modifié.")

# === Remplir le formulaire en cliquant sur un livre ===
def remplir_formulaire(event):
    selection = tree_livres.selection()
    if not selection:
        return

    item = tree_livres.item(selection[0])
    valeurs = item["values"]

    entries["ISBN"].config(state="normal")
    entries["ISBN"].delete(0, tk.END)
    entries["ISBN"].insert(0, valeurs[0])
    entries["ISBN"].config(state="disabled")

    entries["Titre"].delete(0, tk.END)
    entries["Titre"].insert(0, valeurs[1])
    entries["Auteur"].delete(0, tk.END)
    entries["Auteur"].insert(0, valeurs[2])
    entries["Année"].delete(0, tk.END)
    entries["Année"].insert(0, valeurs[3])
    entries["Genre"].delete(0, tk.END)
    entries["Genre"].insert(0, valeurs[4])

tree_livres.bind("<<TreeviewSelect>>", remplir_formulaire)

# === Boutons ===
btn_frame = ttk.Frame(form_frame)
btn_frame.grid(row=len(labels), column=0, columnspan=2, pady=10)

ttk.Button(btn_frame, text="Ajouter le livre", command=ajouter_livre).grid(row=0, column=0, padx=5)
ttk.Button(btn_frame, text="Modifier le livre", command=modifier_livre).grid(row=0, column=1, padx=5)
ttk.Button(btn_frame, text="Supprimer le livre", command=supprimer_livre).grid(row=0, column=2, padx=5)

# === Lancement de la fenêtre ===
root.mainloop()
