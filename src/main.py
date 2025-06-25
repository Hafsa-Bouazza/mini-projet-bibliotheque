from bibliotheque import Livre, Membre, Bibliotheque

def afficher_menu():
    print("\n=== GESTION BIBLIOTHÈQUE ===")
    print("1. Ajouter un livre")
    print("2. Inscrire un membre")
    print("3. Emprunter un livre")
    print("4. Rendre un livre")
    print("5. Lister tous les livres")
    print("6. Quitter")

def main():
    biblio = Bibliotheque()
    biblio.charger_donnees()

    while True:
        afficher_menu()
        choix = input("Choisissez une option (1-6) : ")

        if choix == "1":
            isbn = input("ISBN : ")
            titre = input("Titre : ")
            auteur = input("Auteur : ")
            annee = input("Année : ")
            genre = input("Genre : ")
            livre = Livre(isbn, titre, auteur, annee, genre)
            biblio.ajouter_livre(livre)
            biblio.sauvegarder_donnees()  # ✅ sauvegarde après ajout

        elif choix == "2":
            id_membre = input("ID du membre : ")
            nom = input("Nom : ")
            membre = Membre(id_membre, nom)
            biblio.inscrire_membre(membre)
            biblio.sauvegarder_donnees()  # ✅ sauvegarde après inscription

        elif choix == "3":
            isbn = input("ISBN du livre à emprunter : ")
            id_membre = input("ID du membre : ")
            try:
                biblio.emprunter_livre(isbn, id_membre)
                biblio.sauvegarder_donnees()  # ✅ sauvegarde après emprunt
            except Exception as e:
                print(f"Erreur : {e}")

        elif choix == "4":
            isbn = input("ISBN du livre à rendre : ")
            id_membre = input("ID du membre : ")
            biblio.rendre_livre(isbn, id_membre)
            biblio.sauvegarder_donnees()  # ✅ sauvegarde après retour

        elif choix == "5":
            biblio.lister_livres()

        elif choix == "6":
            biblio.sauvegarder_donnees()
            print("Fermeture du programme. À bientôt !")
            break

        else:
            print("Option invalide. Réessayez.")

if __name__ == "__main__":
    main()
