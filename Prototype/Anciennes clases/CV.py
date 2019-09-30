from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QFrame, QPushButton
from ClassWidget import LigneBat


class CV(QWidget):
    "Classe permettant de creer le widget du centre-Ville"

    def __init__(self, largeur, hauteur, viewer, parent=None):
        super(CV, self).__init__(parent=parent)
        self.parent = parent
        self.viewer = viewer
        self.setGeometry(0, 0, largeur, hauteur)
        self.fond = QFrame(self)

        # hauteur et largeur de l'ecran, ne pas confondre avec hauteur et largeur du Widget(meme si se sont les meme)
        self.hauteur = hauteur
        self.largeur = largeur
        self.fond.setStyleSheet("QFrame {background-color:white}")
        self.fond.setGeometry(100, 100, largeur - 200, hauteur - 200)  # a modifier (emplacement meilleur)
        self.ville = self.parent.parent.joueurEnCour.listeVilles[0]

        # On cree les interfaces du widget
        self.creationInterfaceBat()
        self.creationInterfaceDecret()

        # On cree les boutons pour voyager entre les interfaces
        self.ongletBat = QPushButton(self)
        self.ongletBat.setGeometry(100, 100, 50, 50)
        self.ongletBat.clicked.connect(self.afficheBat)
        self.ongletDecret = QPushButton(self)
        self.ongletDecret.setGeometry(150, 100, 50, 50)
        self.ongletDecret.clicked.connect(self.afficheDecret)

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

        listeNom = ["Niveau du quartier", "Poste de gardes", "Prison", "Tour de guet", "Réserves", "Douves", "Puit", "Remparts intérieurs"]
        for i in range(0, len(listeNom)):
            self.listeBat.append(LigneBat(listeNom[i], i, self.widgetBat, "CV", self))

    def creationInterfaceDecret(self):
        "Methode pour creer l'interface du deuxieme onglet (celui des decrets), ce sera le widgetDecret"

        # Widget pour l'interface des decrets
        self.widgetDecret = QWidget(self)
        self.widgetDecret.setGeometry(100, 150, self.largeur - 200, self.hauteur - 250)

        largeurItem = (self.largeur - 220) / 4 - 20
        hauteurItem = (self.hauteur - 270) / 2 - 20

        self.decret1 = Decret(20, 20, largeurItem, hauteurItem, self.widgetDecret, self)
        self.decret2 = Decret(20 * 2 + largeurItem * 1, 20, largeurItem, hauteurItem, self.widgetDecret, self)
        self.decret3 = Decret(20 * 3 + largeurItem * 2, 20, largeurItem, hauteurItem, self.widgetDecret, self)
        self.decret4 = Decret(20 * 4 + largeurItem * 3, 20, largeurItem, hauteurItem, self.widgetDecret, self)
        self.decret5 = Decret(20 * 1 + largeurItem * 0, 20 * 2 + hauteurItem, largeurItem, hauteurItem, self.widgetDecret, self)
        self.decret6 = Decret(20 * 2 + largeurItem * 1, 20 * 2 + hauteurItem, largeurItem, hauteurItem, self.widgetDecret, self)
        self.decret7 = Decret(20 * 3 + largeurItem * 2, 20 * 2 + hauteurItem, largeurItem, hauteurItem, self.widgetDecret, self)
        self.decret8 = Decret(20 * 4 + largeurItem * 3, 20 * 2 + hauteurItem, largeurItem, hauteurItem, self.widgetDecret, self)

    def afficheBat(self):
        "Methode pour afficher le widget des batiments"
        self.widgetDecret.hide()
        self.widgetBat.show()
        self.widgetBat.setFocus()

    def afficheDecret(self):
        "Methode pour afficher le widget des decret"
        self.widgetBat.hide()
        self.widgetDecret.show()
        self.widgetDecret.setFocus()

    def majBat(self):
        "Methode pour mettre a jour l'onglet des batiments (cacher et montrer ceux qui peuvent etre construit ou non)"
        nvQuart = self.ville.batCV[0]
        for i in range(1, len(self.ville.batCV)):
            self.ville.bdd.execute("""SELECT nvQuart FROM Ville WHERE Quartier == "CV" AND Batiment == %s AND Niveau == 1""" % (i))
            nv = self.ville.bdd.fetchall()[0][0]
            if nvQuart < nv:
                self.listeBat[i].hide()
            else:
                self.listeBat[i].show()

    def majDecret(self):
        "Methode pour mettre a jour l'onglet des decrets"

    def show(self):
        "Methode reimplementant show, permettant d'actualiser les elmt du widget en fonction de la ville"
        super(CV, self).show()
        self.afficheBat()

    def setVille(self, ville):
        "Methode permettant de mettre a jour le widget CV en fonction de la ville"
        self.ville = ville
        for i in self.listeBat:
            i.setVille()
        self.majBat()
        self.majDecret()


class Decret(QWidget):
    "Classe permettant de creer un widget dans l'onglet decret"

    def __init__(self, posX, posY, largeur, hauteur, widget, parent=None):
        super(Decret, self).__init__(widget)
        self.setGeometry(posX, posY, largeur, hauteur)
        self.bouton = QPushButton(self)
        self.bouton.setGeometry(0, 0, largeur, hauteur)
        self.bouton.setText("Mettre en place un decret")
        self.bouton.clicked.connect(self.nouveauDecret)

    def nouveauDecret(self):
        print("Mise en place d'un nouveau decret")
