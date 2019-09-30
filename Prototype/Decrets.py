from PyQt5.QtWidgets import QWidget, QFrame, QPushButton
from PyQt5.QtCore import Qt


class Decrets(QWidget):
    "Classe servant a l'affichage de l'onglet decret de la ville"

    def __init__(self, largeur, hauteur, parent=None):
        super(Decrets, self).__init__(parent=parent)
        self.parent = parent
        self.setGeometry(100, 150, largeur, hauteur - 100)
        self.fond = QFrame(self)

        # hauteur et largeur de l'ecran, ne pas confondre avec hauteur et largeur du Widget(meme si se sont les meme)
        self.hauteur = hauteur - 100
        self.largeur = largeur
        self.fond.setStyleSheet("QFrame {background-color:white}")
        self.fond.setGeometry(0, 0, self.largeur, self.hauteur)

        largeurItem = (self.largeur - 20) / 4 - 20
        hauteurItem = (self.hauteur - 20) / 2 - 20

        self.decret1 = Dec(20, 20, largeurItem, hauteurItem, self)
        self.decret2 = Dec(20 * 2 + largeurItem * 1, 20, largeurItem, hauteurItem, self)
        self.decret3 = Dec(20 * 3 + largeurItem * 2, 20, largeurItem, hauteurItem, self)
        self.decret4 = Dec(20 * 4 + largeurItem * 3, 20, largeurItem, hauteurItem, self)
        self.decret5 = Dec(20 * 1 + largeurItem * 0, 20 * 2 + hauteurItem, largeurItem, hauteurItem, self)
        self.decret6 = Dec(20 * 2 + largeurItem * 1, 20 * 2 + hauteurItem, largeurItem, hauteurItem, self)
        self.decret7 = Dec(20 * 3 + largeurItem * 2, 20 * 2 + hauteurItem, largeurItem, hauteurItem, self)
        self.decret8 = Dec(20 * 4 + largeurItem * 3, 20 * 2 + hauteurItem, largeurItem, hauteurItem, self)

        self.hide()

    def mousePressEvent(self, event):
        "Methode pour annuler le mouse press du wville"

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


class Dec(QWidget):
    "Classe permettant de creer un widget dans l'onglet decret"

    def __init__(self, posX, posY, largeur, hauteur, parent=None):
        super(Dec, self).__init__(parent)
        self.setGeometry(posX, posY, largeur, hauteur)
        self.bouton = QPushButton(self)
        self.bouton.setGeometry(0, 0, largeur, hauteur)
        self.bouton.setText("Mettre en place un decret")
        self.bouton.clicked.connect(self.nouveauDecret)

    def nouveauDecret(self):
        print("Mise en place d'un nouveau decret")
