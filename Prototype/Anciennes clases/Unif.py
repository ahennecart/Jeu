from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QFrame, QPushButton
from ClassWidget import LigneBat


class Unif(QWidget):
    "Classe permettant de creer le widget du centre-Ville"

    def __init__(self, largeur, hauteur, viewer, parent=None):
        super(Unif, self).__init__(parent=parent)
        self.parent = parent
        self.viewer = viewer
        self.setGeometry(0, 0, largeur, hauteur)
        self.fond = QFrame(self)

        # hauteur et largeur de l'ecran, ne pas confondre avec hauteur et largeur du Widget(meme si se sont les meme)
        self.hauteur = hauteur
        self.largeur = largeur
        self.fond.setStyleSheet("QFrame {background-color:white; color:darkblue}")
        self.fond.setGeometry(100, 100, largeur - 200, hauteur - 200)  # a modifier (emplacement meilleur)
        self.ville = self.parent.parent.joueurEnCour.listeVilles[0]

        # On cree les interfaces du widget
        self.creationInterfaceBat()
        self.creationInterfaceRecherche()

        # On cree les boutons pour voyager entre les interfaces
        self.ongletBat = QPushButton(self)
        self.ongletBat.setGeometry(100, 100, 50, 50)
        self.ongletBat.clicked.connect(self.afficheBat)

        self.ongletRech = QPushButton(self)
        self.ongletRech.setGeometry(150, 100, 50, 50)
        self.ongletRech.clicked.connect(self.afficheRech)

        self.hide()

    def mousePressEvent(self, event):
        "Methode pour quitter la fenetre si on clique a cote"

        if (event.x() > 100 and event.x() < self.largeur - 100 and event.y() > 100 and event.y() < self.hauteur - 100):  # Ne fait rien si on clique dans la zone
            return None
        self.hide()
        # Redonne ensuite le focus au widget de la ville
        self.parent.setFocus()

    def keyPressEvent(self, event):
        "Methode pour les racourcis clavier de l'interfaces"

        key = event.key()
        if key == QtCore.Qt.Key_Escape:  # Permet de fermer le menus quand on clique sur esc
            self.hide()
            # Redonne ensuite le focus au widget de la ville
            self.parent.setFocus()
        else:
            print(key)

    def creationInterfaceBat(self):
        "Methode pour creer l'interfaces du premier onglet (celui des batiments), ce sera le widgetBat"

        # Widget pour l'interface des batiments
        self.widgetBat = QWidget(self)
        self.widgetBat.parent = self
        self.widgetBat.setGeometry(100, 150, self.largeur - 200, self.hauteur - 250)
        self.listeBat = []

        listeNom = ["Niveau du quartier", "Bibliothèque", "Aile des sciences mécaniques", "Aile des sciences naturelles", "Aile des sciences militaires", "Tour d'astronomie"]
        for i in range(0, len(listeNom)):
            self.listeBat.append(LigneBat(listeNom[i], i, self.widgetBat, "Unif", self))

    def creationInterfaceRecherche(self):
        "Methode pour creer l'interface du deuxieme onglet (celui des recherches), ce sera la widgetRech"

        self.widgetRech = QWidget(self)
        self.widgetRech.perent = self
        self.widgetRech.setGeometry(100, 150, self.largeur - 200, self.hauteur - 250)

        largeurItem = (self.largeur - 220) / 2 - 20
        hauteurItem = (self.hauteur - 270) / 2 - 20

        self.rech1 = Recherche(20, 20, largeurItem, hauteurItem, self.widgetRech, self)
        self.rech2 = Recherche(40 + largeurItem, 20, largeurItem, hauteurItem, self.widgetRech, self)
        self.rech3 = Recherche(20, hauteurItem + 40, largeurItem, hauteurItem, self.widgetRech, self)
        self.rech4 = Recherche(largeurItem + 40, hauteurItem + 40, largeurItem, hauteurItem, self.widgetRech, self)

    def afficheBat(self):
        "Methode pour afficher le widget des batiments"
        self.widgetRech.hide()
        self.widgetBat.show()
        self.widgetBat.setFocus()

    def afficheRech(self):
        "Methode pour afficher le widget des recherches"
        self.widgetBat.hide()
        self.widgetRech.show()
        self.widgetRech.setFocus()

    def majBat(self):
        "Methode pour mettre a jour l'onglet des batiments (cacher et montrer ceux qui peuvent etre construit ou non)"
        nvQuart = self.ville.batUnif[0]
        for i in range(1, len(self.ville.batUnif)):
            self.ville.bdd.execute("""SELECT nvQuart FROM Ville WHERE Quartier == "Unif" AND Batiment == %s AND Niveau == 1""" % (i))
            nv = self.ville.bdd.fetchall()[0][0]
            if nvQuart < nv:
                self.listeBat[i].hide()
            else:
                self.listeBat[i].show()

    def show(self):
        "Methode reimplementant show, permettant d'actualiser les elmt du widget en fonction de la ville"
        super(Unif, self).show()
        self.afficheBat()

    def setVille(self, ville):
        "Methode permettant de mettre a jour le widget Unif en fonction de la ville"
        self.ville = ville
        for i in self.listeBat:
            i.setVille()
        self.majBat()


class Recherche(QWidget):
    "Classe permettant de creer un widget dans l'onglet Recherche"

    def __init__(self, posX, posY, largeur, hauteur, widget, parent):
        super(Recherche, self).__init__(widget)
        self.setGeometry(posX, posY, largeur, hauteur)
        self.bouton = QPushButton(self)
        self.bouton.setGeometry(0, 0, largeur, hauteur)
        self.bouton.setText("Lancer une recherche")
        self.bouton.clicked.connect(self.nouvelleRecherche)

    def nouvelleRecherche(self):
        "Methode pour lancer une nouvelle recherche"

        print("Recherche d'une nouvelle technologie")
