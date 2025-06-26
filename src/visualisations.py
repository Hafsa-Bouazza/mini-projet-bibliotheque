import matplotlib.pyplot as plt
import csv
import os
from collections import Counter
from datetime import datetime, timedelta

# === Chemins des fichiers ===
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # remonte d’un niveau au-dessus de src/
DATA_DIR = os.path.join(BASE_DIR, "data")  # data est à côté de src
LIVRES_PATH = os.path.join(DATA_DIR, "livres.txt")
HISTORIQUE_PATH = os.path.join(DATA_DIR, "historique.csv")

# === 1. Diagramme circulaire : % de livres par genre ===
def diagramme_genres():
    genres = []

    with open(LIVRES_PATH, encoding="utf-8") as f:
        for ligne in f:
            parts = ligne.strip().split(";")
            if len(parts) >= 5:
                genres.append(parts[4])

    compteur = Counter(genres)
    plt.figure(figsize=(6, 6))
    plt.pie(compteur.values(), labels=compteur.keys(), autopct="%1.1f%%", startangle=140)
    plt.title("Répartition des livres par genre")
    plt.axis("equal")
    plt.show()


# === 2. Histogramme : Top 10 des auteurs les plus populaires ===
def top_auteurs():
    auteurs = []

    with open(LIVRES_PATH, encoding="utf-8") as f:
        for ligne in f:
            parts = ligne.strip().split(";")
            if len(parts) >= 3:
                auteurs.append(parts[2])

    top = Counter(auteurs).most_common(10)
    noms = [auteur for auteur, _ in top]
    valeurs = [count for _, count in top]

    plt.figure(figsize=(10, 6))
    plt.bar(noms, valeurs, color="skyblue")
    plt.xticks(rotation=45, ha="right")
    plt.title("Top 10 des auteurs les plus présents")
    plt.ylabel("Nombre de livres")
    plt.tight_layout()
    plt.show()


# === 3. Courbe temporelle : activité des emprunts (30 derniers jours) ===
def activite_emprunts():
    dates = []

    with open(HISTORIQUE_PATH, encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            # row = [date_heure, action, id_membre, isbn]
            if len(row) >= 4 and row[1] == "emprunt":  # action est à l'indice 1
                try:
                    date = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S").date()
                    dates.append(date)
                except ValueError:
                    pass

    fin = datetime.today().date()
    debut = fin - timedelta(days=29)
    jours = [debut + timedelta(days=i) for i in range(30)]
    compte_par_jour = Counter(dates)

    valeurs = [compte_par_jour.get(jour, 0) for jour in jours]

    plt.figure(figsize=(10, 4))
    plt.plot(jours, valeurs, marker="o", linestyle="-", color="green")
    plt.title("Emprunts sur les 30 derniers jours")
    plt.xlabel("Date")
    plt.ylabel("Nombre d'emprunts")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
