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
'''def supprimer_livre():
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
        messagebox.showinfo("Supprimé", "Livre supprimé avec succès.")'''
def supprimer_livre():
    selection = tree_livres.selection()
    if not selection:
        messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un livre à supprimer.")
        return

    item = selection[0]
    isbn = str(tree_livres.item(item)["values"][0]).strip()  # ✅ assure string

    if isbn not in biblio.livres:
        messagebox.showerror("Erreur", f"Le livre ISBN {isbn} n'existe pas dans la base.")
        charger_livres()
        return

    titre = biblio.livres[isbn].titre
    if messagebox.askyesno("Confirmation", f"Supprimer le livre '{titre}' (ISBN {isbn}) ?"):
        del biblio.livres[isbn]
        biblio.sauvegarder_donnees()
        charger_livres()
        messagebox.showinfo("Succès", "Livre supprimé.")


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

# === Onglet Membres ===
colonnes_m = ("ID", "Nom", "Nb Livres Empruntés")
tree_membres = ttk.Treeview(frame_membres, columns=colonnes_m, show="headings")
for col in colonnes_m:
    tree_membres.heading(col, text=col)
    tree_membres.column(col, width=150)
tree_membres.pack(fill="both", expand=True, padx=10, pady=(0, 10))

# === Barre de recherche ===
search_frame = ttk.Frame(frame_membres)
search_frame.pack(padx=10, pady=(10, 0), fill="x")

search_var = tk.StringVar()
ttk.Label(search_frame, text="🔍 Rechercher :").pack(side="left", padx=5)
entry_search = ttk.Entry(search_frame, textvariable=search_var)
entry_search.pack(side="left", fill="x", expand=True)

def filtrer_membres(*args):
    terme = search_var.get().lower()
    for item in tree_membres.get_children():
        tree_membres.delete(item)
    for membre in biblio.membres.values():
        if terme in membre.nom.lower() or terme in membre.id_membre.lower():
            tree_membres.insert("", "end", values=(membre.id_membre, membre.nom, len(membre.livres_empruntes)))

search_var.trace("w", filtrer_membres)

def charger_membres():
    filtrer_membres()

charger_membres()

form_membre = ttk.LabelFrame(frame_membres, text="Ajouter / Modifier un membre")
form_membre.pack(padx=10, pady=10, fill="x")

entry_nom = ttk.Entry(form_membre)
entry_id = ttk.Entry(form_membre)

ttk.Label(form_membre, text="ID :").grid(row=0, column=0, sticky="w", padx=5, pady=2)
entry_id.grid(row=0, column=1, padx=5, pady=2)

ttk.Label(form_membre, text="Nom :").grid(row=1, column=0, sticky="w", padx=5, pady=2)
entry_nom.grid(row=1, column=1, padx=5, pady=2)

form_membre.columnconfigure(1, weight=1)

def ajouter_membre():
    id_membre = entry_id.get().strip()
    nom = entry_nom.get().strip()

    if not (id_membre and nom):
        messagebox.showerror("Erreur", "Tous les champs sont requis.")
        return

    if id_membre in biblio.membres:
        messagebox.showerror("Erreur", "ID déjà utilisé.")
        return

    membre = Membre(id_membre, nom)
    biblio.inscrire_membre(membre)
    biblio.sauvegarder_donnees()
    charger_membres()
    entry_id.delete(0, tk.END)
    entry_nom.delete(0, tk.END)
    messagebox.showinfo("Succès", "Membre ajouté.")

def remplir_formulaire_membre(event):
    selection = tree_membres.selection()
    if not selection:
        return
    valeurs = tree_membres.item(selection[0])["values"]
    entry_id.config(state="normal")
    entry_id.delete(0, tk.END)
    entry_id.insert(0, valeurs[0])
    entry_id.config(state="disabled")
    entry_nom.delete(0, tk.END)
    entry_nom.insert(0, valeurs[1])

def modifier_membre():
    id_membre = entry_id.get().strip()
    nom = entry_nom.get().strip()

    if id_membre not in biblio.membres:
        messagebox.showerror("Erreur", "ID introuvable.")
        return

    biblio.membres[id_membre].nom = nom
    biblio.sauvegarder_donnees()
    charger_membres()
    entry_id.config(state="normal")
    entry_id.delete(0, tk.END)
    entry_nom.delete(0, tk.END)
    messagebox.showinfo("Succès", "Membre modifié.")

'''def supprimer_membre():
    selection = tree_membres.selection()
    if not selection:
        messagebox.showwarning("Aucune sélection", "Sélectionnez un membre.")
        return
    item = selection[0]
    id_membre = tree_membres.item(item)["values"][0]

    if id_membre not in biblio.membres:
        messagebox.showerror("Erreur", f"Le membre ID {id_membre} n'existe plus.")
        charger_membres()  # recharge proprement la table
        return

    nom = biblio.membres[id_membre].nom
    if messagebox.askyesno("Confirmation", f"Supprimer le membre {id_membre} ({nom}) ?"):
        del biblio.membres[id_membre]
        biblio.sauvegarder_donnees()
        charger_membres()  # recharge la table complète
        entry_id.config(state="normal")
        entry_id.delete(0, tk.END)
        entry_nom.delete(0, tk.END)
        messagebox.showinfo("Supprimé", "Membre supprimé.")'''

def supprimer_membre():
    selection = tree_membres.selection()
    if not selection:
        messagebox.showwarning("Aucune sélection", "Sélectionnez un membre.")
        return

    item = selection[0]
    id_membre = str(tree_membres.item(item)["values"][0]).strip()  # ✅ forcer str

    if id_membre not in biblio.membres:
        messagebox.showerror("Erreur", f"Le membre ID {id_membre} n'existe plus.")
        charger_membres()
        return

    nom = biblio.membres[id_membre].nom
    if messagebox.askyesno("Confirmation", f"Supprimer le membre {id_membre} ({nom}) ?"):
        del biblio.membres[id_membre]
        biblio.sauvegarder_donnees()
        charger_membres()
        entry_id.config(state="normal")
        entry_id.delete(0, tk.END)
        entry_nom.delete(0, tk.END)
        messagebox.showinfo("Supprimé", "Membre supprimé.")


btn_frame_m = ttk.Frame(form_membre)
btn_frame_m.grid(row=2, column=0, columnspan=2, pady=10)

for i, (lbl, cmd) in enumerate([
    ("Ajouter", ajouter_membre),
    ("Modifier", modifier_membre),
    ("Supprimer", supprimer_membre),
]):
    ttk.Button(btn_frame_m, text=lbl, command=cmd).grid(row=0, column=i, padx=5)

tree_membres.bind("<<TreeviewSelect>>", remplir_formulaire_membre)

# === Onglet Emprunts ===
form_emprunt = ttk.LabelFrame(frame_emprunts, text="Emprunter / Rendre un livre")
form_emprunt.pack(padx=10, pady=10, fill="x")

entry_id_membre = ttk.Entry(form_emprunt)
entry_isbn_livre = ttk.Entry(form_emprunt)

ttk.Label(form_emprunt, text="ID Membre :").grid(row=0, column=0, sticky="w", padx=5, pady=2)
entry_id_membre.grid(row=0, column=1, padx=5, pady=2)

ttk.Label(form_emprunt, text="ISBN Livre :").grid(row=1, column=0, sticky="w", padx=5, pady=2)
entry_isbn_livre.grid(row=1, column=1, padx=5, pady=2)

form_emprunt.columnconfigure(1, weight=1)

def emprunter_livre():
    id_membre = str(entry_id_membre.get()).strip()
    isbn = str(entry_isbn_livre.get()).strip()

    if id_membre not in biblio.membres:
        messagebox.showerror("Erreur", f"Membre ID {id_membre} introuvable.")
        return
    if isbn not in biblio.livres:
        messagebox.showerror("Erreur", f"Livre ISBN {isbn} introuvable.")
        return

    try:
        biblio.emprunter_livre(isbn, id_membre)  # corriger l'ordre des paramètres
        biblio.sauvegarder_donnees()
        messagebox.showinfo("Succès", "Livre emprunté.")
        entry_id_membre.delete(0, tk.END)
        entry_isbn_livre.delete(0, tk.END)
        charger_livres()
        charger_membres()
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def rendre_livre():
    id_membre = entry_id_membre.get().strip()
    isbn = entry_isbn_livre.get().strip()

    if id_membre not in biblio.membres:
        messagebox.showerror("Erreur", f"Membre ID {id_membre} introuvable.")
        return
    if isbn not in biblio.livres:
        messagebox.showerror("Erreur", f"Livre ISBN {isbn} introuvable.")
        return

    try:
        biblio.rendre_livre(isbn, id_membre)  # corriger l'ordre des paramètres
        biblio.sauvegarder_donnees()
        messagebox.showinfo("Succès", "Livre rendu.")
        entry_id_membre.delete(0, tk.END)
        entry_isbn_livre.delete(0, tk.END)
        charger_livres()
        charger_membres()
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

btn_frame_emprunt = ttk.Frame(form_emprunt)
btn_frame_emprunt.grid(row=2, column=0, columnspan=2, pady=10)

ttk.Button(btn_frame_emprunt, text="📥 Emprunter", command=emprunter_livre).grid(row=0, column=0, padx=5)
ttk.Button(btn_frame_emprunt, text="📤 Rendre", command=rendre_livre).grid(row=0, column=1, padx=5)

# === Onglet Statistiques ===

label_stats = ttk.Label(frame_stats, text="📈 Visualisations statistiques", font=("Arial", 14))
label_stats.pack(pady=20)

btn_genre = ttk.Button(frame_stats, text="📘 Répartition des livres par genre", command=lambda: visualisations.livres_par_genre(biblio))
btn_genre.pack(pady=10)

btn_emprunts = ttk.Button(frame_stats, text="👤 Nombre d'emprunts par membre", command=visualisations.emprunts_par_membre)
btn_emprunts.pack(pady=10)

# === Lancement de la fenêtre ===
root.mainloop()
