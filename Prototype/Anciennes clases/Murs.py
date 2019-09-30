from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QFrame, QPushButton
from ClassWidget import LigneBat


class Murs(QWidget):
    "Classe permettant de creer le widget du centre-Ville"

    def __init__(self, largeur, hauteur, viewer, parent=None):
        super(Murs, self).__init__(parent=parent)
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

        # On cree les boutons pour voyager entre les interfaces
        self.ongletBat = QPushButton(self)
        self.ongletBat.setGeometry(100, 100, 50, 50)
        self.ongletBat.clicked.connect(self.afficheBat)

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

        listeNom = ["Niveau du quartier", "Douves", "Pont-levis", "Chemin de ronde", "Tours", "Crénaux", "Meurtières", "Catapultes", "Balistes"]
        for i in range(0, len(listeNom)):
            self.listeBat.append(LigneBat(listeNom[i], i, self.widgetBat, "Murs", self))

    def afficheBat(self):
        "Methode pour afficher le widget des batiments"
        self.widgetBat.show()
        self.widgetBat.setFocus()

    def majBat(self):
        "Methode pour mettre a jour l'onglet des batiments (cacher et montrer ceux qui peuvent etre construit ou non)"
        nvQuart = self.ville.batMurs[0]
        for i in range(1, len(self.ville.batMurs)):
            self.ville.bdd.execute("""SELECT nvQuart FROM Ville WHERE Quartier == "Murs" AND Batiment == %s AND Niveau == 1""" % (i))
            nv = self.ville.bdd.fetchall()[0][0]
            if nvQuart < nv:
                self.listeBat[i].hide()
            else:
                self.listeBat[i].show()

    def show(self):
        "Methode reimplementant show, permettant d'actualiser les elmt du widget en fonction de la ville"
        super(Murs, self).show()
        self.afficheBat()

    def setVille(self, ville):
        "Methode permettant de mettre a jour le widget Murs en fonction de la ville"
        self.ville = ville
        for i in self.listeBat:
            i.setVille()
        self.majBat()
