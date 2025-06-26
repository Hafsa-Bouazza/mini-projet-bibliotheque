from exceptions import (
    LivreInexistantError,
    MembreInexistantError,
    LivreIndisponibleError,
    QuotaEmpruntDepasseError
)
import os
import csv
from datetime import datetime

class Livre:
    def __init__(self, isbn, titre, auteur, annee, genre):
        self.isbn = isbn
        self.titre = titre
        self.auteur = auteur
        self.annee = annee
        self.genre = genre
        self.disponible = True  

    def __str__(self):
        statut = "Disponible" if self.disponible else "Emprunté"
        return f"{self.titre} ({self.annee}) - {self.auteur} [{self.genre}] - {statut}"


class Membre:
    def __init__(self, id_membre, nom):
        self.id_membre = id_membre
        self.nom = nom
        self.livres_empruntes = []  

    def emprunter_livre(self, isbn):
        if isbn not in self.livres_empruntes:
            self.livres_empruntes.append(isbn)

    def rendre_livre(self, isbn):
        if isbn in self.livres_empruntes:
            self.livres_empruntes.remove(isbn)

    def __str__(self):
        return f"Membre {self.nom} (ID: {self.id_membre}) - {len(self.livres_empruntes)} livre(s) emprunté(s)"


class Bibliotheque:
    def __init__(self):
        self.livres = {}     
        self.membres = {}    

    def ajouter_livre(self, livre):
        if livre.isbn in self.livres:
            print(f"Livre avec ISBN {livre.isbn} existe déjà.")
        else:
            self.livres[livre.isbn] = livre
            print(f"Livre '{livre.titre}' ajouté.")

    def inscrire_membre(self, membre):
        if membre.id_membre in self.membres:
            print(f"Membre avec ID {membre.id_membre} existe déjà.")
        else:
            self.membres[membre.id_membre] = membre
            print(f"Membre '{membre.nom}' inscrit.")

    def enregistrer_historique(self, action, id_membre, isbn):
        basedir = os.path.dirname(__file__)
        historique_path = os.path.join(basedir, "..", "data", "historique.csv")
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(historique_path, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow([now, action, id_membre, isbn])

    def emprunter_livre(self, isbn, id_membre):
        if isbn not in self.livres:
            raise LivreInexistantError()

        if id_membre not in self.membres:
            raise MembreInexistantError()

        livre = self.livres[isbn]
        membre = self.membres[id_membre]

        if not livre.disponible:
            raise LivreIndisponibleError()

        if len(membre.livres_empruntes) >= 3:
            raise QuotaEmpruntDepasseError()

        livre.disponible = False
        membre.emprunter_livre(isbn)
        print(f"Livre '{livre.titre}' emprunté par {membre.nom}.")
        self.enregistrer_historique("emprunt", id_membre, isbn)

    def rendre_livre(self, isbn, id_membre):
        if isbn not in self.livres:
            print("Livre inexistant.")
            return
        if id_membre not in self.membres:
            print("Membre inexistant.")
            return

        livre = self.livres[isbn]
        membre = self.membres[id_membre]

        if isbn in membre.livres_empruntes:
            livre.disponible = True
            membre.rendre_livre(isbn)
            print(f"Livre '{livre.titre}' rendu par {membre.nom}.")
            self.enregistrer_historique("retour", id_membre, isbn)
        else:
            print(f"Ce membre n'a pas emprunté ce livre.")

    def lister_livres(self):
        if not self.livres:
            print("Aucun livre enregistré.")
        for livre in self.livres.values():
            print(livre)

    def sauvegarder_donnees(self):
        basedir = os.path.dirname(__file__)

        # 📚 Sauvegarder les livres
        livres_path = os.path.join(basedir, "..", "data", "livres.txt")
        with open(livres_path, "w", encoding="utf-8") as f:
            for livre in self.livres.values():
                ligne = f"{livre.isbn};{livre.titre};{livre.auteur};{livre.annee};{livre.genre};{livre.disponible}\n"
                f.write(ligne)
        print("✅ Livres sauvegardés dans :", os.path.abspath(livres_path))

        # 👤 Sauvegarder les membres
        membres_path = os.path.join(basedir, "..", "data", "membres.txt")
        with open(membres_path, "w", encoding="utf-8") as f:
            for membre in self.membres.values():
                livres_str = ",".join(membre.livres_empruntes)
                ligne = f"{membre.id_membre};{membre.nom};{livres_str}\n"
                f.write(ligne)
        print("✅ Membres sauvegardés dans :", os.path.abspath(membres_path))

    def charger_donnees(self):
        # Charger les livres
        if os.path.exists("data/livres.txt"):
            with open("data/livres.txt", "r", encoding="utf-8") as f:
                for ligne in f:
                    isbn, titre, auteur, annee, genre, dispo = ligne.strip().split(";")
                    livre = Livre(isbn, titre, auteur, annee, genre)
                    livre.disponible = dispo == "True"
                    self.livres[isbn] = livre

        # Charger les membres
        if os.path.exists("data/membres.txt"):
            with open("data/membres.txt", "r", encoding="utf-8") as f:
                for ligne in f:
                    parts = ligne.strip().split(";")
                    id_membre = parts[0]
                    nom = parts[1]
                    livres_empruntes = parts[2].split(",") if len(parts) > 2 and parts[2] else []
                    membre = Membre(id_membre, nom)
                    membre.livres_empruntes = livres_empruntes
                    self.membres[id_membre] = membre
