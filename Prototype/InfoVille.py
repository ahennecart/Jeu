from PyQt5.QtWidgets import QWidget, QFrame, QLabel, QLCDNumber
from PyQt5.QtCore import Qt


class InfoVille(QWidget):
    "Classe servant a l'affichage des informations sur la ville"

    def __init__(self, largeur, hauteur, parent=None):
        super(InfoVille, self).__init__(parent=parent)
        self.parent = parent
        self.setGeometry(100, 150, largeur, hauteur - 100)
        self.fond = QFrame(self)

        # hauteur et largeur de l'ecran, ne pas confondre avec hauteur et largeur du Widget(meme si se sont les meme)
        self.hauteur = hauteur - 100
        self.largeur = largeur
        self.fond.setStyleSheet("QFrame {background-color:white}")
        self.fond.setGeometry(0, 0, self.largeur, self.hauteur)

        # Creation des info sur la ville :

        # Creation des indicateurs de ressources :

        hauteurLab = (self.hauteur - 20 * 11) / 10

        self.labBois = QLabel(self)
        self.labBois.setText("Bois :")
        self.labBois.setGeometry(self.largeur / 2 + 50, 20, 200, hauteurLab)
        self.ressBois = QLCDNumber(self)
        self.ressBois.setGeometry(self.largeur - 340, 20, 150, hauteurLab)
        self.ressBois.setDigitCount(6)
        self.revBois = QLCDNumber(self)
        self.revBois.setGeometry(self.largeur - 170, 20, 150, hauteurLab)
        self.revBois.setDigitCount(6)

        self.labPierre = QLabel(self)
        self.labPierre.setText("Pierre :")
        self.labPierre.setGeometry(self.largeur / 2 + 50, hauteurLab + 2 * 20, 200, hauteurLab)
        self.ressPierre = QLCDNumber(self)
        self.ressPierre.setGeometry(self.largeur - 340, 1 * hauteurLab + 2 * 20, 150, hauteurLab)
        self.ressPierre.setDigitCount(6)
        self.revPierre = QLCDNumber(self)
        self.revPierre.setGeometry(self.largeur - 170, 1 * hauteurLab + 2 * 20, 150, hauteurLab)
        self.revPierre.setDigitCount(6)

        self.labFer = QLabel(self)
        self.labFer.setText("Fer :")
        self.labFer.setGeometry(self.largeur / 2 + 50, 2 * hauteurLab + 3 * 20, 200, hauteurLab)
        self.ressFer = QLCDNumber(self)
        self.ressFer.setGeometry(self.largeur - 340, 2 * hauteurLab + 3 * 20, 150, hauteurLab)
        self.ressFer.setDigitCount(6)
        self.revFer = QLCDNumber(self)
        self.revFer.setGeometry(self.largeur - 170, 2 * hauteurLab + 3 * 20, 150, hauteurLab)
        self.revFer.setDigitCount(6)

        self.labOr = QLabel(self)
        self.labOr.setText("Or :")
        self.labOr.setGeometry(self.largeur / 2 + 50, 3 * hauteurLab + 4 * 20, 200, hauteurLab)
        self.ressOr = QLCDNumber(self)
        self.ressOr.setGeometry(self.largeur - 340, 3 * hauteurLab + 4 * 20, 150, hauteurLab)
        self.ressOr.setDigitCount(6)
        self.revOr = QLCDNumber(self)
        self.revOr.setGeometry(self.largeur - 170, 3 * hauteurLab + 4 * 20, 150, hauteurLab)
        self.revOr.setDigitCount(6)

        self.labCharbon = QLabel(self)
        self.labCharbon.setText("Charbon :")
        self.labCharbon.setGeometry(self.largeur / 2 + 50, 4 * hauteurLab + 5 * 20, 200, hauteurLab)
        self.ressCharbon = QLCDNumber(self)
        self.ressCharbon.setGeometry(self.largeur - 340, 4 * hauteurLab + 5 * 20, 150, hauteurLab)
        self.ressCharbon.setDigitCount(6)
        self.revCharbon = QLCDNumber(self)
        self.revCharbon.setGeometry(self.largeur - 170, 4 * hauteurLab + 5 * 20, 150, hauteurLab)
        self.revCharbon.setDigitCount(6)

        self.labMarbre = QLabel(self)
        self.labMarbre.setText("Marbre :")
        self.labMarbre.setGeometry(self.largeur / 2 + 50, 5 * hauteurLab + 6 * 20, 200, hauteurLab)
        self.ressMarbre = QLCDNumber(self)
        self.ressMarbre.setGeometry(self.largeur - 340, 5 * hauteurLab + 6 * 20, 150, hauteurLab)
        self.ressMarbre.setDigitCount(6)
        self.revMarbre = QLCDNumber(self)
        self.revMarbre.setGeometry(self.largeur - 170, 5 * hauteurLab + 6 * 20, 150, hauteurLab)
        self.revMarbre.setDigitCount(6)

        self.labAcier = QLabel(self)
        self.labAcier.setText("Acier :")
        self.labAcier.setGeometry(self.largeur / 2 + 50, 6 * hauteurLab + 7 * 20, 200, hauteurLab)
        self.ressAcier = QLCDNumber(self)
        self.ressAcier.setGeometry(self.largeur - 340, 6 * hauteurLab + 7 * 20, 150, hauteurLab)
        self.ressAcier.setDigitCount(6)
        self.revAcier = QLCDNumber(self)
        self.revAcier.setGeometry(self.largeur - 170, 6 * hauteurLab + 7 * 20, 150, hauteurLab)
        self.revAcier.setDigitCount(6)

        self.labNourriture = QLabel(self)
        self.labNourriture.setText("Nourriture :")
        self.labNourriture.setGeometry(self.largeur / 2 + 50, 7 * hauteurLab + 8 * 20, 200, hauteurLab)
        self.ressNourriture = QLCDNumber(self)
        self.ressNourriture.setGeometry(self.largeur - 340, 7 * hauteurLab + 8 * 20, 150, hauteurLab)
        self.ressNourriture.setDigitCount(6)
        self.revNourriture = QLCDNumber(self)
        self.revNourriture.setGeometry(self.largeur - 170, 7 * hauteurLab + 8 * 20, 150, hauteurLab)
        self.revNourriture.setDigitCount(6)

        self.labBetail = QLabel(self)
        self.labBetail.setText("Betail :")
        self.labBetail.setGeometry(self.largeur / 2 + 50, 8 * hauteurLab + 9 * 20, 200, hauteurLab)
        self.ressBetail = QLCDNumber(self)
        self.ressBetail.setGeometry(self.largeur - 340, 8 * hauteurLab + 9 * 20, 150, hauteurLab)
        self.ressBetail.setDigitCount(6)
        self.revBetail = QLCDNumber(self)
        self.revBetail.setGeometry(self.largeur - 170, 8 * hauteurLab + 9 * 20, 150, hauteurLab)
        self.revBetail.setDigitCount(6)

        self.labChevaux = QLabel(self)
        self.labChevaux.setText("Chevaux :")
        self.labChevaux.setGeometry(self.largeur / 2 + 50, 9 * hauteurLab + 10 * 20, 200, hauteurLab)
        self.ressChevaux = QLCDNumber(self)
        self.ressChevaux.setGeometry(self.largeur - 340, 9 * hauteurLab + 10 * 20, 150, hauteurLab)
        self.ressChevaux.setDigitCount(6)
        self.revChevaux = QLCDNumber(self)
        self.revChevaux.setGeometry(self.largeur - 170, 9 * hauteurLab + 10 * 20, 150, hauteurLab)
        self.revChevaux.setDigitCount(6)

        # Creation du reste (partie droite)

        self.labNom = QLabel(self)
        self.labNom.setGeometry(20, 0 * hauteurLab + 1 * 20, 300, hauteurLab)
        self.labNv = QLabel(self)
        self.labNv.setGeometry(20, 1 * hauteurLab + 2 * 20, 300, hauteurLab)
        self.labType = QLabel(self)
        self.labType.setGeometry(20, 2 * hauteurLab + 3 * 20, 300, hauteurLab)
        self.labPop = QLabel(self)
        self.labPop.setGeometry(20, 3 * hauteurLab + 4 * 20, 300, hauteurLab)
        self.labTC = QLabel(self)  # Label pour le taux de crime
        self.labTC.setGeometry(20, 4 * hauteurLab + 5 * 20, 300, hauteurLab)
        self.labStab = QLabel(self)
        self.labStab.setGeometry(20, 5 * hauteurLab + 6 * 20, 300, hauteurLab)

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

    def show(self):
        "Methode reimplementant le show pour y ajouter un maj"

        self.maj()
        super(InfoVille, self).show()

    def maj(self):
        "Methode pour mettre a jour le widget en fonction de la ville"

        self.majRess()
        self.labNom.setText("Nom de la ville : " + self.parent.ville.nom)
        self.labNv.setText("Niveau de la ville : " + str(self.parent.ville.niveauVille))
        self.labType.setText("Type de la ville : militaire")
        self.labPop.setText("Population de la ville : " + str(self.parent.ville.pop))
        self.labTC.setText("Taux de crime dans la ville : " + str(self.parent.ville.tauxCrime))
        self.labStab.setText("Stabilite de la ville : " + str(self.parent.ville.stabilite))

    def majRess(self):
        "Methode pour mettre a jour les LCD de ressources"

        self.ressBois.display(self.parent.ville.ressources[0])
        self.ressPierre.display(self.parent.ville.ressources[1])
        self.ressFer.display(self.parent.ville.ressources[2])
        self.ressOr.display(self.parent.ville.ressources[3])
        self.ressCharbon.display(self.parent.ville.ressources[4])
        self.ressMarbre.display(self.parent.ville.ressources[5])
        self.ressAcier.display(self.parent.ville.ressources[6])
        self.ressNourriture.display(self.parent.ville.ressources[7])
        self.ressBetail.display(self.parent.ville.ressources[8])
        self.ressChevaux.display(self.parent.ville.ressources[9])
