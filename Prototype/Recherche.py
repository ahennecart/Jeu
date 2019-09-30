from PyQt5.QtWidgets import QWidget, QFrame, QPushButton
from PyQt5.QtCore import Qt


class Recherche(QWidget):
    "Classe servant a l'affichage de l'onglet recherche de la ville"

    def __init__(self, largeur, hauteur, parent=None):
        super(Recherche, self).__init__(parent=parent)
        self.parent = parent
        self.setGeometry(100, 150, largeur, hauteur - 100)
        self.fond = QFrame(self)

        # hauteur et largeur de l'ecran, ne pas confondre avec hauteur et largeur du Widget(meme si se sont les meme)
        self.hauteur = hauteur - 100
        self.largeur = largeur
        self.fond.setStyleSheet("QFrame {background-color:white}")
        self.fond.setGeometry(0, 0, self.largeur, self.hauteur)

        largeurItem = (self.largeur - 20) / 2 - 20
        hauteurItem = (self.hauteur - 20) / 2 - 20

        self.rech1 = Rech(20, 20, largeurItem, hauteurItem, self)
        self.rech2 = Rech(40 + largeurItem, 20, largeurItem, hauteurItem, self)
        self.rech3 = Rech(20, hauteurItem + 40, largeurItem, hauteurItem, self)
        self.rech4 = Rech(largeurItem + 40, hauteurItem + 40, largeurItem, hauteurItem, self)

        self.hide()

    def mousePressEvent(self, event):
        "Methode pour annuler le mousePress de la ville"

    def keyPressEvent(self, event):
        "Methode pour les racourcis clavier de l'interfaces"

        key = event.key()
        if key == Qt.Key_Escape:  # Permet de fermer le menus quand on clique sur esc
            self.hide()
            # Redonne ensuite le focus au viewer
            self.parent.hide()
            self.parent.viewer.setFocus()
        else:
            print(key)

    def setVille(self, ville):
        "Methode pour mettre a jour le widget en fonction de la ville"


class Rech(QWidget):
    "Classe permettant de creer un widget dans l'onglet Recherche"

    def __init__(self, posX, posY, largeur, hauteur, parent):
        super(Rech, self).__init__(parent)
        self.setGeometry(posX, posY, largeur, hauteur)
        self.bouton = QPushButton(self)
        self.bouton.setGeometry(0, 0, largeur, hauteur)
        self.bouton.setText("Lancer une recherche")
        self.bouton.clicked.connect(self.nouvelleRecherche)

    def nouvelleRecherche(self):
        "Methode pour lancer une nouvelle recherche"

        print("Recherche d'une nouvelle technologie")
