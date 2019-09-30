import Affichage_de_la_map
import Affichage_des_menus
from Villes import Ville
from Joueurs import Joueur
from PyQt5.QtWidgets import QMainWindow, QApplication
import sys
import mss  # permet de connaitre la resolution de l'ecran (et des prendre des screens)
import sqlite3

# 1 tour = environs 1 an


class Main(QMainWindow):

    def __init__(self, app, parent=None):
        super(Main, self).__init__(parent=parent)
        mon = mss.mss().monitors[1]
        self.app = app
        self.hauteur = mon["height"]
        self.largeur = mon["width"]
        self.setWindowTitle("Prototype")

        # Liste de toutes les variables globales du jeu
        self.nbTour = 1
        self.nbJoueur = 1

    def quitter(self):
        "Pour quitter vers le bureau"

        sys.exit(self.app.exec_())


# Fonction de test pour creer des villes de test a partir d'un tableau de noms
def creationVilles(noms, joueur, bdd):
    listeVilles = [''] * len(noms)
    i = 0
    for nom in noms:
        listeVilles[i] = Ville(nom, 0, 0, 1000, [200000, 200000, 200000, 200000, 200000, 200000, 200000, 200000, 200000, 200000], joueur)  # Les valeur de ressources sont a ajuster bien evidement
        print(listeVilles[i].nom)
        i = i + 1
    return listeVilles


# Fonction de test pour creer des joueurs de test a partir d'un tableau de noms
def creationJoueurs(noms, fenetre):
    debut = Joueur(None, -1, None, fenetre)
    joueur2 = Joueur(noms[1], 1, debut, fenetre)
    joueur1 = Joueur(noms[0], 1, joueur2, fenetre)
    debut.suivant = joueur1
    fenetre.nbJoueur = 2
    return(joueur1, joueur2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    fenetre = Main(app)

    bdd = sqlite3.connect("Test.db").cursor()

    fenetre.listeJoueurs = creationJoueurs(["Misselia", "Tremor"], fenetre)
    fenetre.joueurEnCour = fenetre.listeJoueurs[0]

    # tableau des villes
    villes = [Ville("Misselia", -2, -6, 10000, [300000, 300000, 300000, 300000, 300000, 300000, 300000, 300000, 300000, 300000], fenetre.listeJoueurs[0], bdd, fenetre), Ville("Tremor", 10, -12, 2000, [200000, 200000, 200000, 200000, 200000, 200000, 200000, 200000, 200000, 200000], fenetre.listeJoueurs[1], bdd, fenetre), Ville("Misselia2", -1, -5, 1000, [300000, 300000, 300000, 300000, 300000, 300000, 300000, 300000, 300000, 300000], fenetre.listeJoueurs[0], bdd, fenetre)]

    tableauCarte = Affichage_de_la_map.TableauCarte("Prototype2.txt")
    tableauRessource = Affichage_de_la_map.TableauRessources("Ressource du prototype.txt", len(tableauCarte.structure))
    fenetre.viewer = Affichage_de_la_map.ViewerCarte(tableauCarte, tableauRessource, "tileset V1.png", fenetre)
    # Affichage des 3 villes du prototype
    fenetre.viewer.addVille(villes[0])
    fenetre.viewer.addVille(villes[1])
    fenetre.viewer.addVille(villes[2])
    # et ajouter 1 village a la ville 1 (donc celle en 0 :/)
    villes[0].addVillage("Village 1", "C", "Pierre", -1, -7)

    # affichage de la gui
    fenetre.boutons = Affichage_des_menus.ConnectionBoutons(fenetre, fenetre.viewer)
    fenetre.showFullScreen()  # On met en full screen pour faire plus joli (et eviter les problemes du a la taille de l'ecrant aussi... ^^')

    fenetre.joueurEnCour.jouer()  # On lance la structure chainee qui represente les joueurs
    sys.exit(app.exec_())
